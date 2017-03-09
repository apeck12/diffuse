import matplotlib, sys, time, glob
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cPickle as pickle
import numpy as np
import Indexer, os.path

"""
Wrapper for Indexer class. Things to add: 1. ability to parse cbf/h5 files.
Usage: python index.py [map directory] [image directory]

"""

def index_data(system, image_dir, output_dir):
    """ 
    Index images with Indexer class.
    Input parameters: system dictionary, image directory, directory for indexed .npy files
    Outputs: indexed .npy files, plot of average differences between Indexer results and INTEGRATE.HKL

    """
    
    num_images = system['n_batch']*system['batch_size']
    deltas = np.zeros((num_images, 3))

    # assume that file numbers are 1-indexed and prefaced by final underscore in file name
    file_glob = glob.glob(image_dir + "*")
    filelist = sorted(file_glob, key = lambda name: int(name.split('_')[-1].split('.')[0]))
    assert len(filelist) == num_images

    # set up instance of Indexer class
    indexer_obj = Indexer.Indexer(system)

    for img in range(num_images): 
        print "Indexing image %i" %img

        # index image and process intensities; save as hklI
        deltas[img] = indexer_obj.index(img + 1) # image suffixes should be 1-indexed
        imgI = np.load(filelist[img])
        indexer_obj.process_intensities(imgI, img + 1)
        np.save(output_dir + "hklI_%s.npy" %(file_glob[img].split('_')[-1].split('.')[0]), indexer_obj.hklI)

        # reset hklI per image and corrections per batch
        indexer_obj.clear_hklI()
        if (img % system['batch_size'] == 0) and (img != 0):
            indexer_obj.clear_corrections()
    
    return deltas

def plot_deltas(deltas, map_dir):
    """
    Plot per image average residual in h,k,l between results of Indexer class 
    and INTEGRATE.HKL.
    """

    f, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(8,8))

    ax1.plot(deltas[:,0])
    ax2.plot(deltas[:,1])
    ax3.plot(deltas[:,2])

    for ax in [ax1, ax2, ax3]:
        ax.set_ylim(0, 0.05)
        ax.set_xlim(0, deltas.shape[0])

    ax1.set_ylabel(r'$\Delta$ h')
    ax2.set_ylabel(r'$\Delta$ k')
    ax3.set_ylabel(r'$\Delta$ l')

    ax1.set_title("Comparison to INTEGRATE.HKL")
    ax3.set_xlabel("Image Number")

    f.savefig(map_dir + "checks/index.png", dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    
    start = time.time()
    system = pickle.load(open(sys.argv[1]+"system.pickle"))

    output_dir = sys.argv[1]+"indexed/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    deltas = index_data(system, sys.argv[2], output_dir)
    plot_deltas(deltas, sys.argv[1])

    print "elapsed time is %f" %((time.time() - start)/60.0)