from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class AddgalsPostProcess(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(AddgalsPostProcess, self).__init__(simnum, system, cosmo, allboxes=True)
    
    def write_config(self, opath, boxl):
        pars = {}
        halopaths = []
        pars['BasePath'] = self.getOutputBaseDir()
        pars['OutPath'] = "{0}/{1}/".format(pars['BasePath'], self.__class__.__name__.lower())
        for boxl in self.cosmoparams['Simulation']['BoxL']:
            halopaths.append("{0}/Lb{1}/output/halos/cut_reform_out_0.parents".format(pars['BasePath'], boxl))

        pars['Prefix'] = '{}-{}'.format(self.cosmoparams['Simulation']['SimName'], self.simnum)
        pars['ZBinFile'] = self.cosmoparams['Addgals']['ZBinFile']
        pars['OmegaM']  = self.cosmoparams['Cosmology']['OmegaM']
        pars['OmegaL']  = self.cosmoparams['Cosmology']['OmegaL']

        jobbase = os.path.join(self.getJobBaseDir(), self.__class__.__name__.lower())

        with open('{0}/{1}.cfg'.format(jobbase, self.__class__.__name__.lower()), 'w') as fp:
            fp.write("outpath    : {OutPath}\n".format(**pars))
            fp.write("basepath   : {BasePath}\n".format(**pars))
            fp.write("halopaths  :\n")
            for i, boxl in enumerate(self.cosmoparams['Simulation']['BoxL']):
                fp.write("  - {0}\n".format(halopaths[i]))
            
            fp.write("prefix     : {Prefix}\n".format(**pars))
            fp.write("suffix     : None\n")
            fp.write("zbinfile   : {ZBinFile}\n".format(**pars))
            fp.write("lensing_output: True\n")
            fp.write("skyfactory : True\n")
            fp.write("omega_m    : {OmegaM}\n".format(**pars))
            fp.write("omega_l    : {OmegaL}\n".format(**pars))

    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.cosmoparams['Addgals']['NTasks'] * self.cosmoparams['Addgals']['NCoresPerTask']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        jobbase = os.path.join(self.getJobBaseDir(), self.__class__.__name__.lower())
        pars['ExecDir'] = self.getExecDir()
        pars['PExecDir'] = os.path.join(self.sysparams['ExecDir'], 'pixlc')
        pars['Email'] = self.sysparams['Email']

        jobscript = self.jobtemp.format(**pars)

        with open('{0}/job.{1}.sh'.format(jobbase, (self.__class__.__name__).lower()), 'w') as fp:
            fp.write(jobscript)
        

                     
