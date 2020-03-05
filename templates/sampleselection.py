from __future__ import print_function
from glob import glob
from copy import copy
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

_config=\
"""
gold:
  gold_footprint_fn: {gold_footprint_fn}
merge:
  debug: {debug}
  merge: {merge}
  nzcut: {nzcut}
  obsdir: {obsname}/
  obsname: {obsname}
  simname: {simname}
  merge_with_bpz : False
samples:
  LSS:
    sys_maps:
      buzzard_mask: {mask}
    z_col: {zfield}
  WL:
    maglim_cut_factor: {maglim_cut_factor}
    rgrp_cut: {rgrp_cut}
    sys_maps:
      buzzard_mask: {mask}
      maglim_r: {maglim_r}
      psf_fwhm_r: {psf_fwhm_r}
    z_col: {zfield}
sim:
  obspath: {obspath}
  truthpath: {truthpath}
  pzpath : {pzpath}
"""

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

            cpars = copy(_config)
            fpars = {}

            fpars['obspath'] = "{}".format(os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', cats[i], '*obs.*[0-9].fits'))
            fpars['pzpath'] = "{}".format(os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', cats[i], '*BPZ*fits'))
            fpars['truthpath'] = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'truth_rotated_'+cats[i], '*truth.*fits')
            fpars['zfield'] = self.cosmoparams['SampleSelection']['z_col']
            fpars['psf_fwhm_r'] = pars['psf_fwhm_r'][i]
            fpars['maglim_r'] = pars['maglim_r'][i]
            fpars['mask'] = pars['buzzard_mask'][i]
            fpars['maglim_cut_factor'] = pars['maglim_cut_factor']
            fpars['rgrp_cut'] = pars['rgrp_cut']
            fpars['gold_footprint_fn'] = pars['gold_footprint_fn'][i]
            fpars['gold_badreg_fn'] = pars['gold_badreg_fn'][i]
            fpars['debug'] = True
            fpars['nzcut'] = True
            fpars['merge'] = True
            fpars['obsname'] = '{}'.format(cats[i])
            fpars['simname'] = 'Buzzard_v2.0'

            cpars = cpars.format(**fpars)

            with open("{0}/selectsamples.{1}.yaml".format(jbase, i), 'w') as fp:
                fp.write(cpars)

    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['NCatalogs'] = len(self.cosmoparams['SampleSelection']['Catalogs'])
        pars['NCoresPerTask'] = self.cosmoparams['SampleSelection']['NCoresPerTask']
        pars['CoresPerNode']  = self.sysparams['CoresPerNode']
        pars['NTasksPerNode'] = int(self.sysparams['CoresPerNode'] // pars['NCoresPerTask'])
        pars['NNodes'] = self.cosmoparams['SampleSelection']['NNodes']
        pars['NTasks'] = pars['NNodes'] * pars['NTasksPerNode']

        pars['JPath']  = '/'.join(self.getJobScriptName().split('/')[:-1])
        pars['JDir'] = self.getJobBaseDir() + '/sampleselection'
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
