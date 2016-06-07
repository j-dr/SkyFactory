from __future__ import print_function
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class ErrorModel(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(ErrorModel, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        pars = {}
        pars['GalPath']  = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'truth', '*lensed*')
        jbase = os.path.join(self.getJobBaseDir(), "errormodel")
        for i in range(self.cosmoparams['ErrorModel']['NModels']):

            pars['Model']    = self.cosmoparams['ErrorModel']['Models'][i]
            pars['OutBase']  = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', pars['Model'])
            pars['DepthFile']= self.cosmoparams['ErrorModel']['DepthFile'][i].format(**self.sysparams)

        if 'MagType' in self.cosmoparams['ErrorModel']:
            pars['MagPath']  = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'mags',
                                            "*"+self.cosmoparams['ErrorModel']['MagType'][i]+"*")
            pars['UseMags']  = True
        else:
            pars['MagPath']  = None
            pars['UseMags']  = False

        if 'Rotation' in self.cosmoparams['ErrorModel']:
            pars['Rotation']  = self.cosmoparams['ErrorModel']['Rotation'][i].format(**self.sysparams)

        with open("{0}/errormodel.{1}.cfg".format(jbase, i), 'w') as fp:
            fp.write("Model    : {Model}\n".format(**pars))
            fp.write("OutBase  : {OutBase}\n".format(**pars))
            fp.write("DepthFile: {DepthFile}\n".format(**pars))
            fp.write("MagPath  : {MagPath}\n".format(**pars))
            fp.write("UseMags  : {UseMags}\n".format(**pars))
            if 'Rotation' in pars.keys():
                fp.write("Rotation : {Rotation}\n".format(**pars))


    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NTasks'] = self.cosmoparams['ErrorModel']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['ErrorModel']['NCoresPerTask']
        pars['NNodes'] = (pars['NTasks']*pars['NCoresPerTask'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        jobbase = os.path.join(self.getJobBaseDir(), self.__class__.__name__.lower())
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'], 'addgals', 'scripts')
        pars['Email'] = self.sysparams['Email']
        pars['NModels'] = self.cosmoparams['ErrorModel']['NModels']

        jobscript = self.jobtemp.format(**pars)

        jname = '{0}/job.{1}.sh'.format(jobbase, (self.__class__.__name__).lower())

        with open(jname, 'w') as fp:
            fp.write(jobscript)

        return jname
