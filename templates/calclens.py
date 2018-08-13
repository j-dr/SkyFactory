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
maxRa                       360.0
minDec                      -90.0
maxDec                      90.0
maxRayMemImbalance          0.75

# parameters related to poisson solver
HEALPixRingWeightPath       {healpix_weights}
SHTOrder                    13
ComvSmoothingScale          0.010      #in Mpc/h

#for doing galaxy grid search
GalsFileList                {GalCatList}
GalOutputName               gal_images
NumGalOutputFiles           128 # will split image gals into this many files per plane

#map parameters
MapRedshiftList             {SFConfigDir}/Calclens/mapzlist.txt
MaxResMap                   1
RayOutputName               Rays_8192

"""

class Calclens(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(Calclens, self).__init__(simnum, system, cosmo, allboxes=True)
    
    def write_config(self, opath, boxl):        
        pars = {}
        
        # run times
        wt = self.sysparams['TimeLimitHours']*3600 # convert to seconds
        pars['WallTimeSeconds'] = wt
        pars['WallTimeRestart'] = 2.0*3600.0 # two hours, hard coded
        
        # cosmology
        pars['OmegaM'] = self.cosmoparams['Cosmology']['OmegaM']
        
        # lens plane config - rmax and number
        plane_width = 25.0
        last_box = self.cosmoparams['Simulation']['BoxL'][-1]
        pars['RMax'] = self.cosmoparams['PixLC']['RMax'][last_box]        
        num_planes = pars['RMax']/plane_width
        assert num_planes*plane_width == pars['RMax']
        pars['NumPlanes'] = int(num_planes)
        
        # lens plane paths
        pars['LensPlanePath'] = os.path.join(self.getOutputBaseDir(),'pixlc')
        pars['LensPlaneName'] = 'snapshot_Lightcone'

        try:
            os.makedirs(pars['LensPlanePath'])
        except:
            pass
        
        # outputs
        pars['OutputPath'] = opath
        pars['healpix_weights'] = os.path.join(self.sysparams['ExecDir'],
                                               self.__class__.__name__.lower(),
                                               'healpix_weights')
        # galaxies
        pars['GalCatList'] = os.path.join(self.getJobBaseDir(),'calclens','galcatlist.txt')
        pars['SFConfigDir'] = self.sysparams['SFConfigBase']
                
        # write to correct spot on disk
        jobbase = os.path.join(self.getJobBaseDir(),self.__class__.__name__.lower())
        config = _base_config.format(**pars)
        with open('{0}/raytrace.cfg'.format(jobbase), 'w') as fp:
            fp.write(config)
        
    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['NCores'] = self.cosmoparams['Calclens']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )//self.sysparams['CoresPerNode']
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],
                                       self.__class__.__name__.lower())
        pars['OPath'] = opath
        pars['Email'] = self.sysparams['Email']
        pars['LDir']  = '%s/addgalspostprocess/lens/' % self.getOutputBaseDir()
        pars['GalCatListCMD'] = 'ls -1 -d %s/addgalspostprocess/truth/*lens* > galcatlist.txt' % self.getOutputBaseDir()
        pars['Restart'] = ''
        pars['OmegaM']  = self.cosmoparams['Cosmology']['OmegaM']
        pars['w0']      = self.cosmoparams['Cosmology']['w0']
        pars['wa']      = self.cosmoparams['Cosmology']['wa']
        pars['h']      = self.cosmoparams['Cosmology']['h']
        pars['octs']   = " ".join([str(o) for o in
                                   range(self.cosmoparams['Simulation']['NumOctants'])])

        jobbase = os.path.join(self.getJobBaseDir(),self.__class__.__name__.lower())

        jobscript = self.jobtemp.format(**pars)        
        with open('{0}/job.{1}.{2}'.format(jobbase,
                                           self.__class__.__name__.lower(),
                                           'sh'), 'w') as fp:
            fp.write(jobscript)

        pars['GalCatListCMD'] = ''
        pars['Restart'] = '1'
        jobscript = self.jobtemp.format(**pars)        
        with open('{0}/job.{1}.restart.{2}'.format(jobbase,
                                                   self.__class__.__name__.lower(),
                                                   'sh'), 'w') as fp:
            fp.write(jobscript)


        spath = '{0}/job.{1}.{2}'.format(jobbase,
                                         self.__class__.__name__.lower(),
                                         'sh')
        return spath
