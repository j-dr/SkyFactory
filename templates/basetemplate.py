from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

def read_yaml(fname):
    with open(fname,'r') as fp:
        config = yaml.load(fp)
    return config


class BaseTemplate(object):
    """
    Class from which all other templates inherit
    """

    __metaclass__ = ABCMeta

    def __init__(self, simnum, system, cosmo, **kwargs):
        
        self.simnum = simnum
        self.sysname = system
        self.cosmofile = cosmo
        if 'outname' not in kwargs.keys():
            self.outname = (self.__class__.__name__).lower()
        else:
            self.outname = kwargs['outname']

        if 'allboxes' not in kwargs.keys():
            self.allboxes = False
        else:
            self.allboxes = kwargs["allboxes"]

    def readSysConfig(self):
        
        sysfile = os.path.join('systems', self.sysname,'%s.yaml' % self.sysname)
        self.sysparams = read_yaml(sysfile)

    def readCosmoFile(self):
        
        self.cosmoparams = read_yaml("{0}/{1}.yaml".format(self.sysparams['SFConfigBase'],self.cosmofile))

    def readJobTemplateFile(self):

        templatefile = os.path.join('systems', self.sysname,'%s.sh' % 
                                    ((self.__class__.__name__).lower()))
        
        with open(templatefile, 'r') as fp:
            jobtemp = fp.readlines()

        self.jobtemp = "".join(jobtemp)

    def getJobScriptName(self):
        
        return "{0}/{1}/job.{1}.sh".format(self.jobbase, (self.__class__.__name__).lower())

    def getOutputBaseDir(self):
        return os.path.join(self.sysparams['OutputBase'],
                            '{0}-{1}'.format(self.cosmoparams['Simulation']['SimName'],
                                             self.simnum))

    def getJobBaseDir(self):
        return  os.path.join(self.sysparams['JobBase'],
                             '{0}-{1}'.format(self.cosmoparams['Simulation']['SimName'],
                                              self.simnum))

    def getExecDir(self):
        return os.path.join(self.sysparams['ExecDir'], (self.__class__.__name__).lower())
                            
    @abstractmethod
    def write_jobscript(opath, bsize):
        """
        Method which writes a job submission script based
        on a script template specific to the job. 

        *****MUST RETURN PATH TO JOB SUBMISSION SCRIPT*****
        """
        pass
    
    @abstractmethod
    def write_config(opath, bsize):
        """
        Method which writes the configuration file based
        on a config template specific to the task.
        """
        pass
        
    def setup(self):
        
        self.readSysConfig()
        self.readCosmoFile()
        self.readJobTemplateFile()

        self.jobbase = os.path.join(self.sysparams['JobBase'],'{0}-{1}'.format(self.cosmoparams['Simulation']['SimName'],self.simnum))

        if not self.allboxes:
        
            for i, bsize in enumerate(self.cosmoparams['Simulation']['BoxL']):
                
                obase = os.path.join(self.getOutputBaseDir(),
                                    "Lb%s" % bsize, 'output', self.outname)
                
                ebase = os.path.join(self.getJobBaseDir(),
                                     "Lb%s" % bsize, (self.__class__.__name__).lower())
                try:
                    os.makedirs(ebase)
                except:
                    pass
                
                try:
                    os.makedirs(obase)
                except:
                    pass
                
                self.write_jobscript(obase, bsize)
                self.write_config(obase, bsize)

        else:
            
            obase = os.path.join(self.getOutputBaseDir(), self.outname)
            ebase = os.path.join(self.getJobBaseDir(),
                                 (self.__class__.__name__).lower())

            try:
                os.makedirs(ebase)
            except:
                pass
            
            try:
                os.makedirs(obase)
            except:
                pass
            
            self.write_jobscript(obase, None)
            self.write_config(obase, None)
