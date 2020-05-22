from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class UnarchivePreprocess(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        BaseTemplate.__init__(self, simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):
        pass

    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['BoxL'] = boxl
        pars['OPath'] = '/'.join(opath.split('/')[:-1])
        pars['SimNum'] = self.simnum
        pars['Email'] = self.sysparams['Email']
        pars['Repo'] = self.sysparams['Repo']
        pars['lcnum'] = '{lcnum}'
        pars['cnum'] = self.simnum
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        if self.sysname=='edison':
            pars['Cluster'] = "esedison"

        elif self.sysname=="cori-haswell":
            pars['Cluster'] = "escori"

        if pars["SimName"] == "Chinchilla":
            pars['Group'] = "Herd"

        if pars["SimName"] == "Aardvark":
            pars['Group'] = ""

        jobscript = self.jobtemp.format(**pars)
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               (self.__class__.__name__).lower())

        with open('{0}/job.unarchivepreprocess.sh'.format(jobbase), 'w') as fp:
            fp.write(jobscript)
