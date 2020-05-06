from __future__ import print_function
from glob import glob
from copy import copy
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

_cfg = \
"""
run_name : {somversion}
sompzh5_filename : {simname}_sompz_v{somversion}.h5
cellmap_filename : data_cellmap_10e6.h5
pcchat_filename : pcchat_som.npy
max_iter    : 10000000
nwide_train : 10000000

use_mpi : False

is_buzzard_run : True # buzzard
widebands : irz
deep_bands_file : /global/cscratch1/sd/jmyles/sompz_buzzard/deep_bands.txt # buzzard
wide_bands_file : /global/cscratch1/sd/jmyles/sompz_buzzard/wide_bands.txt # buzzard
fluxtypes : ['unsheared'] # buzzard
flux_tables : ['gold']    # buzzard
select_keys : ['index/select'] # buzzard
flux_errtype : ivar  # buzzard, inverse variance
somsize_wide : 32
somsize_deep : 64
nbins : 4
reuse_bins : False
usepz : False # buzzard
bin_on_mode : True # data binning on mode of redshift sample
zbins_max : 6.00
zbins_dz  : 0.01

zmax_pileup : 3.0
zmax_weight : 1.0
data_dir : {datadir}

deep_file : /global/cscratch1/sd/jmyles/sompz_buzzard/deep_buzzard.{dummy}.pkl #buzzard
balrog_file : '' # buzzard (not necessary for buzzard)

wide_file : {mastercat}
zp_catalog : 22.5 # the zero point of the catalog fluxes. NOT TO BE CONFUSED WITH zp (see below), the zero point used to interpret the depth map used to make noisy Buzzard fluxes.

diagnostic_plots : True
use_testing_chunks : False

buzzard_noisy_deep_pre_injection : False
buzzard_noisy_deep_post_injection : True
buzzard_noisy_deep_lim_mag: [ 24.96, 25.83, 25.44, 24.28, 24.78, 24.12, 23.93, 23.71, ]
buzzard_noisy_deep_multiplier : 2

buzzard_job_id : 0
buzzard_ndeep_realizations : 300 # number of mock deep catalogs we want to make (e.g. 300. Not the number of fields (e.g. 4) that make up a given deep catalog.)
buzzard_nbalrog_realizations : 10

indir : /global/cscratch1/sd/jderose/BCC/Chinchilla/Herd/Chinchilla-3/addgalspostprocess
posfiles : /global/project/projectdirs/des/jderose/Chinchilla/Herd/Chinchilla-3/v1.9.9/addgalspostprocess/truth/Chinchilla-3_lensed_rs_shift_rs_scat_cam.{dummy1}.fits
magfiles : /global/project/projectdirs/des/jderose/Chinchilla/Herd/Chinchilla-3/v1.9.9/surveymags/Chinchilla-3-v1.9.7-auxmag.{dummy1}.fits

bands_name_file : /global/cscratch1/sd/jmyles/sompz_buzzard/y3wlpz_filters_normed.txt
square_size_list : [3.32, 3.29, 1.94, 1.38] # E2, X3, C3, COSMOS
redshift_sample_bool : [False, False, False, True]

GalBaseName : TRUEY3_deep_fields
MagBaseName : DESY3PZ_deep_fields
DeepFieldOutputBase : Chinchilla-3Y3_v1.9.9_balrog_fullY3
fixed_n_gal_redshift_sample : 100000 #57285 #100000

som_tag : lupticolor_64x64_lupticolorluptitude_32x32
tag : pheno_z_scheme_uncertainty
data_tag : y3_mastercat

rmatrix_file : /global/project/projectdirs/des/jderose/SkyFactory-config/ErrorModel/desy3_irot.pkl
buzzard_CellNumHealPixCorrespondence : /global/homes/j/jmyles/repositories/des-science-sompz-buchs-et-al/test/uncertainty_characterization_buzzard_1.9.8/cellnum_pix_correspondence_1.9.8.h5

buzzard_fmap_file : '{mastercat}'
mag_shift_spline_file : /global/project/projectdirs/des/jderose/sompz/buzzard/buzzard_v199_mag_shift.txt
bal_error_model : True
Model : Y3
DepthFile : /project/projectdirs/des/jderose/SkyFactory-config/Addgals/y3a2_gold_2_2_1_sof_nside4096_nest_griz_depth.fits.gz
Nest : False
DataBaseStyle : True
Bands : [g, r, i, z]
UseLMAG : True
UseMags  : [1, 2, 3, 4]
RefBands : [z]
zp : 30
FilterObs : False
BlindObs : False
UseBalMags : [2, 3, 4]
BalrogBands : [r, i, z]
DetectionFile : /global/project/projectdirs/des/severett/Balrog/run2/stacked_catalogs/1.4/sof/balrog_detection_catalog_sof_run2_v1.4.fits
MatchedCatFile : /global/project/projectdirs/des/severett/Balrog/run2/stacked_catalogs/1.4/mcal/balrog_mcal_stack-y3v02-0-riz-noNB-mcal_run2_v1.4.h5
"""

class Sompz(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(Sompz, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        pars = self.cosmoparams['Sompz']
        spars = self.cosmoparams['SampleSelection']
        cpars = copy(pars)
        
        cats = cpars.pop('Catalogs')

        jbase = os.path.join(self.getJobBaseDir(), "sompz")


        for i in range(len(cats)):
            config = copy(_cfg)

            sname = '{}-{}_{}_{}'.format(spars['simname'], self.simnum,
                                          self.cosmoparams['Simulation']['ModelVersion'],
                                          cats[i])
            cpars['sim_version'] = self.cosmoparams['Simulation']['ModelVersion']
            cpars['simname'] = sname
            cpars['footprint'] = cats[i]

            cpars['somversion'] = pars['version']
            cpars['datadir'] = os.path.join(self.getOutputBaseDir(), 'sompz', cats[i])
            cpars['mastercat'] = os.path.join(self.getOutputBaseDir(), 'sampleselection', cats[i], sname + '_mastercat.h5')
            cpars['dummy'] ='{}'
            cpars['dummy1'] ='{0}'

            config = config.format(**cpars)

            with open("{0}/sompz.{1}.cfg".format(jbase, i), 'w') as fp:
                fp.write(config)

    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['NCatalogs'] = len(self.cosmoparams['PhotoZ']['Catalogs'])
        pars['NTasks'] = self.cosmoparams['PhotoZ']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['PhotoZ']['NCoresPerTask']
        pars['NCores']        = pars['NTasks'] * pars['NCoresPerTask']
        pars['CoresPerNode']  = self.sysparams['CoresPerNode']
        pars['NTasksPerNode'] = int(self.sysparams['CoresPerNode'] / pars['NCoresPerTask'])
        pars['NNodes'] = (int(pars['NTasks'])*int(pars['NCoresPerTask']) + self.sysparams['CoresPerNode'] - 1 )//self.sysparams['CoresPerNode']
        pars['Email'] = self.sysparams['Email']
        pars['ExecDir'] = self.getExecDir()
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['CatNames'] = "{}".format(" ".join(self.cosmoparams['PhotoZ']['Catalogs']))
        pars['SomVersion'] = self.cosmoparams['Sompz']['version']
        pars['OrigDir'] = self.cosmoparams['Sompz']['DataDir']
        pars['OutDir'] = os.path.join(self.getOutputBaseDir(), 'sompz')
        pars['Dummy'] = "${CatNames[@]}"
        jobscript = self.jobtemp.format(**pars)

        jname = self.getJobScriptName()

        with open(jname, 'w') as fp:
            fp.write(jobscript)
