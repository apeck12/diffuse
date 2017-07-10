# diffuse
While automated programs have been developed to reconstruct reciprocal space maps from Bragg diffraction data, there is minimal software that can process diffuse scattering data. Further, there are no established programs for modeling the diffuse signal. We aimed to develop a pipeline for generating three-dimensional diffuse scattering maps from experimental data that could be easily tuned to both accommodate various data collection choices and fit the evolving needs of downstream analysis. Thus, we emphasize flexibility and convenience rather than speed. This repository contains the result of that endeavor. User choices include degree of map oversampling relative to integral Miller indices and background subtraction strategies, and the scripts have been coded in Python for ease of use and adaptation. Currently only data collected by the rotation method are supported, but we hope in future iterations to enable processing of serial data. Please direct any questions and feedback to \url{apeck@stanford.edu}.
