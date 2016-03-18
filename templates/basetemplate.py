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
        self.cosmo = cosmo
        if 'outname' not in kwargs.keys():
            self.outname = (self.__class__.__name__).lower()
        else:
            self.outname = kwargs['outname']

    def readSysConfig(self):
        
        sysfile = os.path.join('systems', self.sysname,'%s.yaml' % self.sysname)
        self.sysparams = read_yaml(sysfile)

    def readCosmoFile(self):
        
        cosmofile = os.path.join('%s.yaml' % self.cosmo)
        self.cosmoparams = read_yaml(cosmofile)

    def readJobTemplateFile(self):

        templatefile = os.path.join('../systems', self.sysname,'%s.%s' % 
                                    (self.__class__.__name__, self.sysparams['Sched']))
        
        with open(templatefile, 'r') as fp:
            jobtemp = fp.readlines()

        self.jobtemp = "".join(jobtemp)
                                    

    def setup(self):
        
        self.readSysConfig()
        self.readCosmoFile()
        self.readConfigTemplateFile()
        self.readJobTemplateFile()
        
        for i, bsize in enumerate(self.cosmoparams['BoxL']):

            base = os.path.join(self.sysparams['OutputBase'],
                                 '{0}-{1}'.format(self.cosmoparams['SimName'],
                                                  self.simnum),
                                 "Lb%s" % bsize, 'output')

            ebase = os.path.join(self.sysparams['JobBase'],
                                 '{0}-{1}'.format(self.cosmoparams['SimName'],
                                                  self.simnum),
                                 "Lb%s" % bsize, self.__class__.__name__)
            try:
                os.makedirs(ebase)
            except:
                pass

            opath = base+'/{0}'.format(self.outname)

            try:
                os.makedirs(opath)
            except:
                pass

            self.write_jobscript(opath, bsize)
            self.write_config(opath, bsize)
