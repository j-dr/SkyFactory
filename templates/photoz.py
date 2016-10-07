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
        pars['ExecPath'] = self.sysparams['ExecDir']

        jbase = os.path.join(self.getJobBaseDir(), "photoz")

        for i in range(len(pars['Catalogs'])):
            pars['OPath'] = os.path.join(self.getOutputBaseDir(), 'photoz', pars['Catalogs'][i]

            with open("{0}/photoz.{1}.cfg".format(jbase, i), 'w') as fp:
                yaml.dump(fp, pars)


    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['NCatalogs'] = self.cosmoparams['Photoz']['NCatalogs']
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
