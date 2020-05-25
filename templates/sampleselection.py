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

"""

_mastercat_config=\
"""
outfile: {outfile}_mastercat.h5
mcalfile: {outfile}_shape.h5
goldfile: {outfile}_gold.h5
bpzfile: {outfile}_bpz.h5
sompzfile : {somoutdir}/{outbase}_sompz_{somversion}.h5
rmfile : {outputbase}_run
redmagic_filebase: {redmagic_filebase}/
zmask_filebase: {zmask_filebase}
zmask_file: {zmask_file}
sys_weight_template : {sys_weight_template}
redmapper_filebase: None
regionfile: {regionfile}
footprint_maskfile: {footprint_maskfile}
mapfile: {mapfile}
x_opt : {xo_metacal}
x_opt_altlens : {xo_altlens}
zbins : {zbins_data}
sigma_e_data : {se_data}
do_id_sort : True
do_hpix_sort : True
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
            fpars['simname'] = 'Buzzard-{}_v2.0'.format(self.simnum)

            cpars = cpars.format(**fpars)

            with open("{0}/selectsamples.{1}.yaml".format(jbase, i), 'w') as fp:
                fp.write(cpars)


            cpars = copy(_mastercat_config)
            sname = '{}-{}_{}_{}'.format(pars['simname'], self.simnum,
                                                      self.cosmoparams['Simulation']['ModelVersion'],
                                                      cats[i])
            fpars['outfile'] = os.path.join(self.getOutputBaseDir(), 'sampleselection',
                                                        cats[i], sname)
            fpars['somoutdir'] = os.path.join(self.getOutputBaseDir(), 'sompz')
            fpars['outbase'] = sname
            fpars['outputbase'] = '{}-{}{}_{}'.format(pars['simname'], self.simnum,
                                                      cats[i], self.cosmoparams['Simulation']['ModelVersion'])
            fpars['somversion'] = self.cosmoparams['Sompz']['version']
            fpars['sys_weight_template'] = pars['sys_weight_template'][i]
            fpars['zmask_filebase'] = pars['zmask_filebase']
            fpars['zmask_file'] = pars['zmask_file']            
            fpars['simnum'] = self.simnum
            fpars['catalog'] = cats[i]
            fpars['redmagic_filebase'] = os.path.join(self.getOutputBaseDir(), 'redmapper')
            fpars['footprint_maskfile'] = pars['gold_footprint_fn'][i]
            fpars['mapfile'] = pars['mapfile'][i]
            fpars['regionfile'] = pars['regionfile'][i]
            fpars['xo_metacal'] = pars['xo_metacal']
            fpars['xo_altlens'] = pars['xo_altlens']
            fpars['zbins_data'] = pars['zbins_data']
            fpars['se_data'] = pars['se_data']

            cpars = cpars.format(**fpars)
            
            with open("{0}/mastercat.{1}.yaml".format(jbase, i), 'w') as fp:
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
