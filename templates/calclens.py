from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

_base_config = \
"""
# calclens config

#CPU time limits in seconds
WallTimeLimit               {WallTimeSeconds}     #total time limit - 43 hours here
WallTimeBetweenRestart      {WallTimeRestart}     #time between writing restart files - 4 hours here

#cosmology/raytrace info
OmegaM                      {OmegaM}
maxComvDistance             {RMax}      #in Mpc/h
NumLensPlanes               {NumPlanes}

# lens plane info
LensPlanePath               {LensPlanePath}
LensPlaneName               {LensPlaneName}
LensPlaneType               pixLC

# ray output info
OutputPath                  {OutputPath}
NumRayOutputFiles           128 #number of files to split ray outputs into
NumFilesIOInParallel        128 # number of files to output in parallel - must be less than both NumRayOutputFiles and NumGalOutputFiles

# controls region of rays and spacing
bundleOrder                 5
rayOrder                    13
minRa                       0.0
maxRa                       180.0
minDec                      0.0
maxDec                      90.0
maxRayMemImbalance          0.75

# parameters related to poisson solver
HEALPixRingWeightPath       {healpix_weights}
SHTOrder                    13
ComvSmoothingScale          0.010      #in Mpc/h

#for doing galaxy grid search
GalsFileList                {galCatList}
GalOutputName               gal_images
NumGalOutputFiles           128 # will split image gals into this many files per plane

"""

class Calclens(BaseTemplate):
    def write_config(self, opath, boxl):
        pass

    def write_jobscript(self, opath, boxl):
        pass
    
    
