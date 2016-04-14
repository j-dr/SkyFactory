from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

class Addgals(BaseTemplate):

    def write_config(self, opath, boxl):
        pars = {}
        bopath = '/'.join(opath.split('/')[:-1])
        bsbase = bopath.split('Lb{0}'.format(boxl))
        adgcfg = self.cosmoparams['Addgals']
        coscfg = self.cosmoparams['Cosmology']
        simcfg = self.cosmoparams['Simulation']

        sn = '{0}-{1}'.format(simcfg['SimName'], self.simnum)
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}'.format(sn),
                               'Lb{0}'.format(boxl), self.__class__.__name__.lower())

        with open('{0}/setup_addgals.idl'.format(jobbase), 'w') as fp:
            fp.write("sim_zmin = {0}\n".format(adgcfg['SimZmin'][boxl]))
            fp.write("sim_zmax = {0}\n".format(adgcfg['SimZmax'][boxl]))                     
            fp.write("nproc = {0}\n".format(adgcfg['NZbins'][boxl]))
            fp.write("omegam = {0}\n".format(coscfg['OmegaM']))
            fp.write("omegal = {0}\n".format(coscfg['OmegaL']))
            fp.write("boxsize = {0}\n".format(boxl))
            fp.write("bcg_mass_lim = {0}\n".format(adgcfg['BCGMassLim'][boxl]))
            fp.write("simname = {0}\n".format(simcfg['SimName']))
            fp.write("halofile = '{0}/{1}'\n".format(bopath, 'halos/out_0.parents'))
            fp.write("rnn_halofile = '{0}/{1}'\n".format(bopath, 'rnn/rnn_out_0.parents'))
            fp.write("dir = '{0}'\n".format(opath))
            fp.write("ddir = '{0}/{1}/'\n".format(bopath, 'pixlc'))
            fp.write("execdir = '{0}'\n".format(opath))
            fp.write("srcdir = '{0}'\n".format(os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower())))
            fp.write("paramfile = '{0}'\n".format(adgcfg['ParamFile']))
            fp.write("pardir = '{0}'\n".format(self.sysparams['SFConfigBase']+'/Addgals'))
            fp.write("""make_buzzard_flock, dir=dir, $
                        sim_zmin=sim_zmin, sim_zmax=sim_zmax, $
                        nproc=nproc, $
                        omegam=omegam, omegal=omegal, $
                        simfile=simfile, rnnfile=rnnfile, $
                        halofile=halofile, rnn_halofile=rnn_halofile, $
                        simname=simname, boxsize=boxsize, $
                        hfile=hfile, bcg_mass_lim=bcg_mass_lim, paramfile=paramfile, $
                        catdir=catdir, ddir=ddir, execdir=execdir, srcdir=srcdir, pardir=pardir""")


        sdir = "'{0}'".format(os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower()))

        shutil.copyfile("{0}/scripts/make_buzzard_flock.pro".format(sdir[1:-1]),
                        "{0}/make_buzzard_flock.pro".format(jobbase))
        shutil.copyfile("{0}/scripts/make_params_files_buzzard.sh".format(sdir[1:-1]),
                        "{0}/make_params_files_buzzard.sh".format(jobbase))
        shutil.copyfile("{0}/scripts/make_l-addgals_submission_files.sh".format(sdir[1:-1]),
                        "{0}/make_l-addgals_submission_files.sh".format(jobbase))
        os.chmod("{0}/make_params_files_buzzard.sh".format(jobbase), 0o777)
        os.chmod("{0}/make_l-addgals_submission_files.sh".format(jobbase), 0o777)


    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['BoxL'] = boxl
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.cosmoparams['Addgals']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), (self.__class__.__name__).lower())
        pars['Email'] = self.sysparams['Email']

        jobscript = self.jobtemp.format(**pars)

        with open('{0}/job.{1}.sh'.format(jobbase, (self.__class__.__name__).lower()), 'w') as fp:
            fp.write(jobscript)
