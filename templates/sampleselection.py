from __future__ import print_function
from glob import glob
from copy import copy
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

class SampleSelection(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(SampleSelection, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        pars = self.cosmoparams['SampleSelection']
        pars['ExecPath'] = self.sysparams['ExecDir']
        
        cpars = copy(pars)
        cats = cpars.pop('Catalogs')
        _ = cpars.pop('NCoresPerTask')
        _ = cpars.pop('NNodes')
        _ = cpars.pop('NTasks')
        _ = cpars.pop('ExecPath')
        bmasks = cpars.pop('buzzard_mask')
        
        jbase = os.path.join(self.getJobBaseDir(), "sampleselection")

        for i in range(len(cats)):
            cpars['sim']  = {'obspath':'"{}"'.format(os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', cats[i], '*obs.*[0-9].fits')),
                             'truthpath':os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'truth_rotated_'+cats[i], '*truth.*fits')}

            for sample in cpars['samples']:
                if 'sys_maps' in cpars['samples'][sample]:
                    cpars['samples'][sample]['sys_maps']['buzzard_mask'] = bmasks[i]
                else:
                    cpars['samples'][sample]['sys_maps'] = {'buzzard_mask': bmasks[i]}

            cpars['merge'] = { 'obsdir'  : '{}/'.format(cats[i]),
                               'simname' : 'Buzzard_v1.6',
                               'debug'   : False,
                               'nzcut'   : True,
                               'merge'   : True}
            
            with open("{0}/selectsamples.{1}.yaml".format(jbase, i), 'w') as fp:
                yaml.dump(cpars, fp)

    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['NCatalogs'] = len(self.cosmoparams['SampleSelection']['Catalogs'])
        pars['NTasks'] = self.cosmoparams['SampleSelection']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['SampleSelection']['NCoresPerTask']
        pars['NCores']        = pars['NTasks'] * pars['NCoresPerTask']
        pars['CoresPerNode']  = self.sysparams['CoresPerNode']
        pars['NTasksPerNode'] = int(self.sysparams['CoresPerNode'] / pars['NCoresPerTask'])
        pars['NNodes'] = self.cosmoparams['SampleSelection']['NNodes']
        pars['Email'] = self.sysparams['Email']
        pars['ExecDir'] = self.getExecDir()
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['OPath'] = os.path.join(self.getOutputBaseDir(), "sampleselection")

        jobscript = self.jobtemp.format(**pars)

        jname = self.getJobScriptName()

        with open(jname, 'w') as fp:
            fp.write(jobscript)
