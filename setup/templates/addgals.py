from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class Addgals(Template):

    def write_config(self, opath, boxl):
        pars = {}
        bopath = '/'.join(opath.split('/')[:-1])
        bsbase = bopath.split('Lb{0}'.format(boxl))
        adgcfg = self.cosmoparams['Addgals']

        sn = '{0}-{1}'.format(self.cosmoparams['SimName'], self.simnum)
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}'.format(sn),
                               'Lb{0}'.format(boxl), self.__class__.__name__)

        with open('{0}/setup_addgals.idl'.format(jobbase), 'w') as fp:
            pf.write("sim_zmin = {0}".format(adgcfg['SimZmin'][boxl]))
            pf.write("sim_zmax = {0}".format(self.cosmoparams['SimZmax'][boxl]))                     
            pf.write("nproc = {0}".format(self.cosmoparams['NZbins'][boxl]))
            pf.write("omegam = {0}".format(self.cosmoparams['NZbins'][boxl]))
            pf.write("omegal = {0}".format(self.cosmoparams[

        pars['SimName'] = "'{0}'".format(sn)
        pars['SimNum'] = self.simnum
        pars['Boxl' ] = "'{0}'".format(boxl)
        pars['Halos'] = "'{0}/{1}'".format(bopath, 'halos/out_0.parents')
        pars['HaloRnn'] = "'{0}/{1}'".format(bopath, 'rnn/rnn_out_0.parents')
        pars['LCDir'] = "'{0}/{1}/'".format(bopath, 'pixlc')
        pars['SDir'] = "'{0}'".format(os.path.join(self.sysparams['ExecDir'],self.__class__.__name__))
        pars['OmegaM'] = self.cosmoparams['OmegaM']
        pars['OmegaL'] = self.cosmoparams['OmegaL']
        pars['ZMin'] = self.cosmoparams['SimZmin'][boxl]
        pars['ZMax'] = self.cosmoparams['SimZmax'][boxl]
        pars['NZbins'] = self.cosmoparams['NZbins'][boxl]
        pars['BCGMassLim'] = "'{0}'".format(self.cosmoparams['BCGMassLim'][boxl])


        pars['OPath'] = "'{0}'".format(opath)
        pars['PFile'] = "'{0}'".format(self.cosmoparams['ParamFile'])
        cfg = self.cfgtemp.format(**pars)

        shutil.copyfile("{0}/scripts/make_buzzard_flock.pro".format(pars['SDir'][1:-1]),
                        "{0}/make_buzzard_flock.pro".format(jobbase))
        shutil.copyfile("{0}/scripts/make_params_files_buzzard.sh".format(pars['SDir'][1:-1]),
                        "{0}/make_params_files_buzzard.sh".format(jobbase))
        shutil.copyfile("{0}/scripts/make_l-addgals_submission_files.sh".format(pars['SDir'][1:-1]),
                        "{0}/make_l-addgals_submission_files.sh".format(jobbase))
        os.chmod("{0}/make_params_files_buzzard.sh".format(jobbase), 0o777)
        os.chmod("{0}/make_l-addgals_submission_files.sh".format(jobbase), 0o777)
        with open('{0}/setup_addgals.idl'.format(jobbase), 'w') as fp:
            fp.write(cfg)


    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['BoxL'] = boxl
        pars['SimName'] = self.cosmoparams['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.cosmoparams['ncores_rnn']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), self.__class__.__name__)
        pars['Email'] = self.sysparams['Email']

        jobscript = self.jobtemp.format(**pars)

        with open('{0}/job.adg.{1}'.format(jobbase, self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
