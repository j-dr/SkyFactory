from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

_base_config = \
"""
area: null
area_coarsebin: 0.005
area_finebin: 0.001
b:
- 3.27e-12
- 4.83e-12
- 6.0e-12
- 9.0e-12
bands:
- g
- r
- i
- z
bkg_chisqbinsize: 0.5
bkg_deepmode: false
bkg_refmagbinsize: 0.2
bkg_zbinsize: 0.02
bkg_zredbinsize: 0.01
bkgfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_run_bkg.fit
bkgfile_color: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_bkg_color.fit
border: 0.0
calib_color_maxnodes:
- 0.8
- -1.0
- -1.0
calib_color_nodesizes:
- 0.05
- 0.05
- 0.05
calib_color_nsig: 1.5
calib_color_pcut: 0.5
calib_colormem_beta: 0.0
calib_colormem_colormodes:
- 0
- 1
- 2
calib_colormem_minlambda: 10.0
calib_colormem_r0: 0.5
calib_colormem_sigint:
- 0.05
- 0.03
- 0.03
calib_colormem_smooth: 0.003
calib_colormem_zbounds:
- 0.35
- 0.8
calib_corr_nocorrslope: true
calib_corr_nodesize: 0.1
calib_corr_pcut: 0.8
calib_corr_slope_nodesize: 0.2
calib_covmat_constant: 0.9
calib_covmat_maxnodes:
- -1
- -1
- -1
calib_covmat_nodesize: 0.25
calib_lumfunc_alpha: -1.0
calib_make_full_bkg: true
calib_minlambda: 5.0
calib_niter: 3
calib_nproc: 8
calib_pcut: 0.3
calib_pivotmag_nodesize: 0.1
calib_redgal_template: bc03_colors_des.fit
calib_redspec_nsig: 2.0
calib_run_min_nside: 1
calib_run_nproc: 8
calib_slope_nodesizes:
- 0.1
- 0.1
- 0.1
calib_smooth: 0.003
calib_use_pcol: true
calib_zlambda_clean_nsig: 3.5
calib_zlambda_correct_niter: 3
calib_zlambda_minlambda: 5.0
calib_zlambda_nodesize: 0.1
calib_zlambda_slope_nodesize: 0.1
calib_zrange_cushion: 0.05
catfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_run_redmapper_v0.5.1_lgt20_vl50_catalog.fit
centerclass: CenteringWcenZred
chisq_max: 20.0
consolidate_lambda_cuts:
- 5.0
- 20.0
consolidate_vlim_lstars:
- 0.2
- 5.0
covmask_nside_default: 32
depthfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/y3a2_gold_1.0-10z_mofv02_depthstr.hs
dldr_gamma: 0.6
firstpass_beta: 0.0
firstpass_centerclass: CenteringBCG
firstpass_minlambda: 3.0
firstpass_niter: 2
firstpass_r0: 0.5
galfile: {OutputDir}/{OutputBase}_obs_rmp_master_table.fit
galfile_nside: 32
galfile_pixelized: true
halofile: null
has_truth: true
hpix: []
likelihoods_beta: 0.2
likelihoods_minlambda: 3.0
likelihoods_r0: 1.0
likelihoods_use_zred: true
limmag_catalog: 23.336650848388672
limmag_ref: 23.336650848388672
lnw_cen_mean: 0.22569153632267577
lnw_cen_sigma: 0.25740778231557493
lnw_fg_mean: -0.26852294785612363
lnw_fg_sigma: 0.2283744584329757
lnw_sat_mean: 0.03784476051657139
lnw_sat_sigma: 0.33711599932919534
lval_reference: 0.2
mask_mode: 3
maskfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/y3a2_gold_1.0-10z_mofv02_pixmask.hs
maskgal_dmag_extra: 0.3
maskgal_ngals: 6000
maskgal_nsamples: 100
maskgal_rad_stepsize: 0.1
maskgal_zred_err: 0.02
maskgalfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_maskgals.fit
max_maskfrac: 0.2
mstar_band: z03
mstar_survey: des
nmag: 4
npzbins: 21
nside: 0
outbase: {OutputBase}_run
outpath: ./
parfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_iter3_pars.fit
percolation_beta: 0.2
percolation_lmask: 0.1
percolation_maxcen: 5
percolation_memlum: null
percolation_memradius: null
percolation_minlambda: 3.0
percolation_niter: 2
percolation_pbcg_cut: 0.5
percolation_r0: 1.0
percolation_rmask_0: 1.5
percolation_rmask_beta: 0.2
percolation_rmask_gamma: 0.0
percolation_rmask_zpivot: 0.3
phi1_mmstar_m: -0.943192174244583
phi1_mmstar_slope: -0.943192174244583
phi1_msig_m: 0.38767833594707274
phi1_msig_slope: -0.08567591179713292
plotpath: plots
randfile: null
redgalfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_zspec_redgals.fit
redgalmodelfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_zspec_redgals_model.fit
redmagic_apply_afterburner_zsamp: true
redmagic_calib_buffer: 0.05
redmagic_calib_chisqcut: 20.0
redmagic_calib_corr_nodesize: 0.05
redmagic_calib_fractrain: 0.5
redmagic_calib_nodesize: 0.05
redmagic_calib_redshift_buffer: 0.05
redmagic_calib_zbinsize: 0.02
redmagic_etas:
- 0.5
- 1.0
- 1.5
redmagic_maxlum: 100.0
redmagic_mock_truthspec: false
redmagic_n0s:
- 10.0
- 4.0
- 1.0
redmagic_names:
- highdens
- highlum
- higherlum
redmagic_run_afterburner: true
redmagic_zmaxes:
- 0.7
- 0.95
- 0.95
redmagic_zrange:
- 0.1
- 0.95
redmagicfile: {SFConfigDir}/redmapper/buzzard_2.0/calfiles/buzzard_1.9.9_3y3a_rsshift_intersection_run_redmagic_calib.fit
ref_ind: 3
refmag: z
rsig: 0.05
seedfile: null
select_scaleval: false
specfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_spec.fit
specfile_train: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_spec.fit
survey_mode: 1
version: 0.5.1
vlim_bands:
- i
- r
- g
vlim_depthfiles:
- {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/y3a2_gold_1.0-10i_mofv02_depthstr.hs
- {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/y3a2_gold_1.0-10r_mofv02_depthstr.hs
- {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/y3a2_gold_1.0-10g_mofv02_depthstr.hs
vlim_lstar: 0.2
vlim_nsigs:
- 5.0
- 3.0
- 3.0
wcen_Delta0: -1.5587901449148744
wcen_Delta1: -0.2559426066384868
wcen_cal_zrange:
- 0.2
- 0.65
wcen_maxlambda: 100.0
wcen_minlambda: 10.0
wcen_pivot: 30.0
wcen_rsoft: 0.05
wcen_sigma_m: 0.3873533391289362
wcen_uselum: true
wcen_zred_chisq_max: 100.0
wcenfile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_iter3_wcen.fit
zeropoint: 22.5
zlambda_binsize: 0.002
zlambda_epsilon: 0.005
zlambda_maxiter: 20
zlambda_parab_step: 0.002
zlambda_pivot: 30.0
zlambda_tol: 0.0002
zlambda_topfrac: 0.7
zlambdafile: {SFConfigDir}/redmapper/buzzard_1.9.9/calfiles/buzzard_1.9.9_3y3a_rsshift_iter3_zlambda.fit
zmemfile: null
zrange:
- 0.1
- 0.95
zred_nsamp: 4
zredc_binsize_coarse: 0.005
zredc_binsize_fine: 0.0001
zredfile: {OutputDir}/zreds/{OutputBase}_zreds_master_table.fit

"""

class Redmapper(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(Redmapper, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):
        pars = {}

        jbase = os.path.join(self.getJobBaseDir(), "redmapper")

        for i in range(self.cosmoparams['ErrorModel']['NModels']):

            pars['Model']    = self.cosmoparams['ErrorModel']['Models'][i]
            pars['OutputDir']  = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', pars['Model'])
            pars['OutputBase'] = "{0}-{1}{2}_{3}".format(
                self.cosmoparams['Simulation']['SimName'], self.simnum,
                pars['Model'],
                self.cosmoparams['Simulation']['ModelVersion'])
            pars['SFConfigDir'] = self.sysparams['SFConfigBase']

            config = _base_config.format(**pars)
            with open('{0}/redmapper.{1}.cfg'.format(jbase, i), 'w') as fp:
                fp.write(config)
                
    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NTasks'] = 1
        pars['NCoresPerTask'] = self.sysparams['CoresPerNode']
        pars['NNodesRedmagic'] = 1
        pars['NNodesZred'] = self.cosmoparams['Redmapper']['NNodesZred']
        pars['NCores'] = self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = '1'
        jobbase = os.path.join(self.getJobBaseDir(), self.__class__.__name__.lower())        
        pars['JobBase'] = jobbase
        pars['Email'] = self.sysparams['Email']
        pars['NModels'] = self.cosmoparams['ErrorModel']['NModels']
        pars['RedmapperShifter'] = self.cosmoparams['Redmapper']['RedmapperShifter']
        pars['OPath'] = os.path.join(self.getOutputBaseDir(), "redmapper")
        pars['OutputBase'] = self.getOutputBaseDir()
        pars['NRandoms'] = self.cosmoparams['Redmapper']['NRandomsRedmagic']
        
        
        gen_jobscript_command = 'shifter --image={RedmapperShifter} /bin/bash -c ". /opt/redmapper/startup.sh && redmapper_batch.py -c {Config} -N {NNodesZred} -r 1 -b haswell-debug"'

        gen_jobscript_file = '{}/gen_zred_jobscripts.sh'.format(jobbase)

        with open(gen_jobscript_file, 'w') as fp:
            for i in range(pars['NModels']):
                pars['Config'] = '{}/redmapper.{}.cfg'.format(jobbase, i)
                js_command = gen_jobscript_command.format(**pars)
                fp.write('{}\n'.format(js_command))

        jobscript = self.jobtemp.format(**pars)

        jname = '{0}/job.{1}.sh'.format(jobbase, (self.__class__.__name__).lower())

        with open(jname, 'w') as fp:
            fp.write(jobscript)

        return jname
