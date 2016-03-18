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
        coscfg = self.cosmoparams['Cosmology']
        simcfg = self.cosmoparams['Simulation']

        sn = '{0}-{1}'.format(self.cosmoparams['SimName'], self.simnum)
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}'.format(sn),
                               'Lb{0}'.format(boxl), self.__class__.__name__)

        with open('{0}/setup_addgals.idl'.format(jobbase), 'w') as fp:
            pf.write("sim_zmin = {0}".format(adgcfg['SimZmin'][boxl]))
            pf.write("sim_zmax = {0}".format(adgcfg['SimZmax'][boxl]))                     
            pf.write("nproc = {0}".format(adgcfg['NZbins'][boxl]))
            pf.write("omegam = {0}".format(coscfg['OmegaM']))
            pf.write("omegal = {0}".format(coscfg['OmegaL']))
            pf.write("boxsize = {0}".format(boxl))
            pf.write("bcg_mass_lim = {0}".format(adgcfg['BCGMassLim'][boxl]))
            pf.write("simname = {0}".format(simcfg['SimName']))
            pf.write("halofile = '{0}/{1}'".format(bopath, 'halos/out_0.parents'))
            pf.write("rnn_halofile = '{0}/{1}'".format(bopath, 'rnn/rnn_out_0.parents'))
            pf.write("dir = '{0}'".format(opath))
            pf.write("ddir = '{0}/{1}/'".format(bopath, 'pixlc'))
            pf.write("execdir = '{0}'".format(opath))
            pf.write("srcdir = '{0}'".format(os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower())))
            pf.write("paramfile = '{0}'".format(adgcfg['ParamFile']))


        sdir = "'{0}'".format(os.path.join(self.sysparams['ExecDir'],self.__class__.__name__))

        shutil.copyfile("{0}/scripts/make_buzzard_flock.pro".format(pars['SDir'][1:-1]),
                        "{0}/make_buzzard_flock.pro".format(jobbase))
        shutil.copyfile("{0}/scripts/make_params_files_buzzard.sh".format(pars['SDir'][1:-1]),
                        "{0}/make_params_files_buzzard.sh".format(jobbase))
        shutil.copyfile("{0}/scripts/make_l-addgals_submission_files.sh".format(pars['SDir'][1:-1]),
                        "{0}/make_l-addgals_submission_files.sh".format(jobbase))
        os.chmod("{0}/make_params_files_buzzard.sh".format(jobbase), 0o777)
        os.chmod("{0}/make_l-addgals_submission_files.sh".format(jobbase), 0o777)


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
