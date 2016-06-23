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
            pars['RotOutDir'] = os.path.join(self.getOutputBaseDir(),
                                            'addgalspostprocess',
                                            'truth_rotated_{0}'.format(pars['Model']))
            pars['RotBase']   = "{0}-{1}{2}_{3}_truth.fits".format(
                self.cosmoparams['Simulation']['SimName'], self.simnum,
                pars['Model'],
                self.cosmoparams['Simulation']['ModelVersion'])
            pars['MatPath'] = self.cosmoparams['ErrorModel']['MatPath'][i].format(**self.sysparams)
            pars['OutputDir']  = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', pars['Model'])
            pars['OutputBase'] = "{0}-{1}{2}_{3}".format(
                self.cosmoparams['Simulation']['SimName'], self.simnum,
                pars['Model'],
                self.cosmoparams['Simulation']['ModelVersion'])
            pars['DepthFile'] = self.cosmoparams['ErrorModel']['DepthFile'][i].format(**self.sysparams)
            pars['Nest'] = self.cosmoparams['ErrorModel']['Nest'][i]

            if ('MagType' in self.cosmoparams['ErrorModel'].keys()) & (self.cosmoparams['ErrorModel']['MagType'] is not None):
                pars['MagPath']  = os.path.join(self.getOutputBaseDir(),
                                            'addgalspostprocess', 'mags',
                                            "*"+self.cosmoparams['ErrorModel']['MagType'][i]+"*")
                pars['UseMags']  = '[0,1,2,3,4]'
            else:
                pars['MagPath']  = None
                pars['UseMags']  = None

            pars['DataBaseStyle'] = True
            if 'Y1' in pars['Model']:
                pars['Bands'] = '[g, r, i, z, y]'
            elif 'DR8' in pars['Model']:
                pars['Bands'] = '[u, g, r, i, z]'
            else:
                raise(ValueError("No bands specified for model {0}".format(pars["Model"])))

            pars['UseLMAG'] = True

            with open("{0}/errormodel.{1}.cfg".format(jbase, i), 'w') as fp:
                fp.write("GalPath  : {GalPath}\n".format(**pars))
                fp.write("Model    : {Model}\n".format(**pars))
                fp.write("OutputDir  : {OutputDir}\n".format(**pars))
                fp.write("OutputBase : {OutputBase}\n".format(**pars))
                fp.write("DepthFile: {DepthFile}\n".format(**pars))
                fp.write("Nest: {Nest}\n".format(**pars))
                fp.write("DataBaseStyle: {DataBaseStyle}\n".format(**pars))
                fp.write("Bands: {Bands}\n".format(**pars))
                fp.write("UseLMAG: {UseLMAG}\n".format(**pars))
                fp.write("MagPath  : {MagPath}\n".format(**pars))
                fp.write("UseMags  : {UseMags}\n".format(**pars))
                fp.write("RotOutDir: {RotOutDir}\n".format(**pars))
                fp.write("RotBase: {RotBase}\n".format(**pars))
                fp.write("MatPath: {MatPath}\n".format(**pars))


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
