from __future__ import print_function
import os

from .basetemplate import BaseTemplate

_base_config = \
    """
# addgals config
Runtime :
  outpath : {OutputPath}
  nside_output : {nside_output}
  write_pos : True
NBody :
  Domain :
    fmt : BCCLightcone
    lbox : {lbox}
    rmin : {rmin}
    rmax : {rmax}
    nrbins : {nrbins}
    nside : {nside}
    nest : {nest}
  partpath :
    - /output/Lb1050/output/pixlc/
    - /output/Lb2600/output/pixlc/
    - /output/Lb4000/output/pixlc/
  denspath :
    - /output/Lb1050/output/calcrnn/
    - /output/Lb2600/output/calcrnn/
    - /output/Lb4000/output/calcrnn/
  hinfopath :
    - /output/Lb1050/output/pixlc/
    - /output/Lb2600/output/pixlc/
    - /output/Lb4000/output/pixlc/
  halofile :
    - /output/Lb1050/output/halos/cut_reform_out_0.parents
    - /output/Lb2600/output/halos/cut_reform_out_0.parents
    - /output/Lb4000/output/halos/cut_reform_out_0.parents
  halodensfile :
    - /output/Lb1050/output/halos/rnn_cut_reform_out_0.parents
    - /output/Lb2600/output/halos/rnn_cut_reform_out_0.parents
    - /output/Lb4000/output/halos/rnn_cut_reform_out_0.parents

Cosmology:
  omega_m : {OmegaM}
  omega_b : {OmegaB}
  h : 1.0
  n_s : {ns}
  sigma8 : {sigma8}
  w : {w}

GalaxyModel :
  ADDGALSModel :
    luminosityFunctionConfig :
      modeltype : {LuminosityFunctionModel}
      magmin : {magmin}
    rdelModelConfig :
      rdelModelFile : {rdelModelFile}
      lcenModelFile : {lcenModelFile}
      lcenMassMin : {lcenMassMin}
      useSubhalos : {useSubhalos}
      scatter: {scatter}
    colorModelConfig :
      redFractionModelFile : {redFractionModelFile}
      trainingSetFile : {trainingSetFile}
      filters : {filters}
      band_shift : {band_shift}
    shapeModelConfig :
      modeltype : GMMShapes
      n_components : {shapeNComponents}
      cov_file : {shapeCovFile}
      means_file : {shapeMeansFile}
      weights_file : {shapeWeightsFile}
      conditional_fields :
      - {shapeConditionalFields}
      conditional_field_mean : [{shapeConditionalMeans}]
      conditional_field_std : [{shapeConditionalStd}]
      size_mean : {sizeMean}
      size_std : {sizeStd}
      epsilon_mean : {epsilonMean}
      epsilon_std: {epsilonStd}

"""


class Addgals(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(Addgals, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):
        pars = {}

        # cosmology
        pars['OmegaM'] = self.cosmoparams['Cosmology']['OmegaM']
        pars['OmegaB'] = self.cosmoparams['Cosmology']['OmegaB']
        pars['ns'] = self.cosmoparams['Cosmology']['ns']
        pars['sigma8'] = self.cosmoparams['Cosmology']['sigma8']
        pars['w'] = self.cosmoparams['Cosmology']['w0']

        pars['lbox'] = self.cosmoparams['Simulation']['BoxL']

        for p in list(self.cosmoparams['Addgals']['ModelParams'].keys()):
            pars[p] = self.cosmoparams['Addgals']['ModelParams'][p]

        # outputs
        pars['OutputPath'] = '{}/addgalspostprocess/truth/{}-{}'.format(self.getOutputBaseDir(), self.cosmoparams['Simulation']['SimName'], self.simnum)

        config = _base_config.format(**pars)

        jobbase = os.path.join(self.getJobBaseDir(), self.__class__.__name__.lower())

        with open('{0}/addgals.cfg'.format(jobbase), 'w') as fp:
            fp.write(config)

    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['NTasks'] = self.cosmoparams['Addgals']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['Addgals']['NCoresPerTask']
        pars['NNodes'] = int((
            pars['NTasks'] * pars['NCoresPerTask'] + self.sysparams['CoresPerNode'] - 1) // self.sysparams['CoresPerNode'])
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],
                                       self.__class__.__name__.lower())
        pars['OPath'] = opath
        pars['Email'] = self.sysparams['Email']
        pars['OutputBase'] = self.getOutputBaseDir()

        jobbase = os.path.join(self.getJobBaseDir(),
                               self.__class__.__name__.lower())

        jobscript = self.jobtemp.format(**pars)
        with open('{0}/job.{1}.{2}'.format(jobbase,
                                           self.__class__.__name__.lower(),
                                           'sh'), 'w') as fp:
            fp.write(jobscript)

        spath = '{0}/job.{1}.{2}'.format(jobbase,
                                         self.__class__.__name__.lower(),
                                         'sh')
        return spath
