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
OutputPath: {OutputPath} # will be cleared w/ rm -rf so path should be unique
InputPath: {InputPath}   # usually a path to outputs of calclens
InputName: {InputName}   # basename of galaxy outputs from calclens (the GalOutputName parameter)
ConcatOutputName: {ConcatOutputName}  # basename of intermediate outputs from this script
GalsFileList: {GalsFileList} # same as parameter to calclens

"""

class CalclensPostProcess(BaseTemplate):
    def __init__(self, simnum, system, cosmo):
        super(CalclensPostProcess, self).__init__(simnum, system, cosmo, allboxes=True)
    
    def write_config(self, opath, boxl):        
        pars = {}
        
        # outputs
        pars['OutputPath'] = opath
        pars['ConcatOutputName'] = 'concat_gal_images'
        
        # inputs
        pars['InputPath'] = os.path.join(self.getOutputBaseDir(),'calclens')
        pars['InputName'] = 'gal_images'
        
        # galaxies
        pars['GalsFileList'] = os.path.join(self.getOutputBaseDir(),'calclens','galcatlist.txt')
                
        # write to correct spot on disk
        jobbase = os.path.join(self.getJobBaseDir(),self.__class__.__name__.lower())
        config = _base_config.format(**pars)
        with open('{0}/calclensconcat.yaml'.format(jobbase), 'w') as fp:
            fp.write(config)
        
    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['NCores'] = self.cosmoparams['Calclens']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],
                                       'calclens')
        pars['OPath'] = opath
        pars['Email'] = self.sysparams['Email']
        
        jobbase = os.path.join(self.getJobBaseDir(),self.__class__.__name__.lower())

        jobscript = self.jobtemp.format(**pars)        
        spath = '{0}/job.{1}.{2}'.format(jobbase,
                                         self.__class__.__name__.lower(),
                                         'sh')
        with open(spath,'w') as fp:
            fp.write(jobscript)
            
        return spath 

    
    
