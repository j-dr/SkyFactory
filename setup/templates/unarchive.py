from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class UnarchiveLightcone(Template):

    def __init__(self, simnum, system, cosmo):
        Template.__init__(self, simnum, system, cosmo, outname='lightcone')

    def readConfigTemplateFile(self):
        pass

    def write_config(self, opath, boxl):
        pass

    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['SimName'] = self.cosmoparams['SimName']
        pars['BoxL'] = boxl
        pars['OPath'] = opath
        pars['SimNum'] = self.simnum
        pars['Email'] = self.sysparams['Email']
        if self.sysname=='edison':
            pars['Cluster'] = "esedison"

        elif self.sysname=="cori":
            pars['Cluster'] = "escori"

        if pars["SimName"] == "Chinchilla":
            pars['Group'] = "Herd"

        jobscript = self.jobtemp.format(**pars)
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), self.__class__.__name__)

        with open('{0}/job.unarchive.{1}'.format(jobbase,self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
