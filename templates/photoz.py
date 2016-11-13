from __future__ import print_function
from glob import glob
from copy import copy
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

class PhotoZ(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(PhotoZ, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        pars = self.cosmoparams['PhotoZ']
        pars['ExecPath'] = self.sysparams['ExecDir']

        cpars = copy(pars)
        cats = cpars.pop('Catalogs')

        jbase = os.path.join(self.getJobBaseDir(), "photoz")

        for i in range(len(cats)):
            cpars['Catalogs'] = cats[i]
            cpars['OPath'] = os.path.join(self.getOutputBaseDir(), 'photoz', cats[i])
            cpars['FilePath'] = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', cats[i], '*fits')
            with open("{0}/photoz.{1}.cfg".format(jbase, i), 'w') as fp:
                yaml.dump(cpars, fp)

    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['NCatalogs'] = len(self.cosmoparams['PhotoZ']['Catalogs'])
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

        jname = self.getJobScriptName()

        with open(jname, 'w') as fp:
            fp.write(jobscript)
