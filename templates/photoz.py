from __future__ import print_function
from glob import glob
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

class PhotoZ(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(PhotoZ, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        pars = self.cosmoparams['PhotoZ']
        pars['FilePath'] = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'truth', '*lensed*')

        jbase = os.path.join(self.getJobBaseDir(), "errormodel")

        with open("{0}/photoz.cfg", 'w') as fp:
            yaml.dump(fp, pars)


    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['NTasks'] = self.cosmoparams['PhotoZ']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['PhotoZ']['NCoresPerTask']
        pars['NNodes'] = (int(pars['NTasks'])*int(pars['NCoresPerTask']) + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['Email'] = self.sysparams['Email']
        pars['ExecDir'] = self.getExecDir()
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']

        jobscript = self.jobtemp.format(**pars)

        jname = '{0}/job.{1}.sh'.format(jobbase, (self.__class__.__name__).lower())

        with open(jname, 'w') as fp:
            fp.write(jobscript)
