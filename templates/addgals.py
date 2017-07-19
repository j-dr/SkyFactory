from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import os

from .basetemplate import BaseTemplate

class Addgals(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(Addgals, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        opath = opath.split('addgals')[0]

        for boxl in [1050, 2600, 4000]:
            pars = {}
            bopath = '{}/Lb{}/output/'.format(opath,boxl)
            adgcfg = self.cosmoparams['Addgals']
            coscfg = self.cosmoparams['Cosmology']
            simcfg = self.cosmoparams['Simulation']

            ebase = os.path.join(self.getJobBaseDir(),
                                 "Lb%s" % boxl, (self.__class__.__name__).lower())
            try:
                os.makedirs(ebase)
            except:
                pass

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
                fp.write("boxsize = '{0}'\n".format(boxl))
                fp.write("bcg_mass_lim = '{0}'\n".format(adgcfg['BCGMassLim'][boxl]))
                fp.write("simname = '{0}-{1}'\n".format(simcfg['SimName'], self.simnum))
                fp.write("halofile = '{0}/{1}'\n".format(bopath, 'halos/cut_reform_out_0.parents'))
                fp.write("rnn_halofile = '{0}/{1}'\n".format(bopath, 'calcrnn/rnn_cut_reform_out_0.parents'))
                fp.write("dir = '{0}'\n".format(opath+'/Lb'+str(boxl)+'/'+'output/addgals/'))
                fp.write("ddir = '{0}/{1}/'\n".format(bopath, 'pixlc'))
                fp.write("execdir = '{0}'\n".format(opath+'/Lb'+str(boxl)+'/'+'output/addgals/'))
                fp.write("srcdir = '{0}'\n".format(os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower())))
                fp.write("paramfile = '{0}'\n".format(adgcfg['ParamFile']))
                fp.write("pardir = '{0}'\n".format(self.sysparams['SFConfigBase']+'/Addgals'))
                fp.write("cfgstr = '{0}'\n".format(self.cosmoparams['Addgals']['CfgStr']))
                fp.write("""make_buzzard_flock, dir=dir, $
                            sim_zmin=sim_zmin, sim_zmax=sim_zmax, $
                            nproc=nproc, $
                            omegam=omegam, omegal=omegal, $
                            simfile=simfile, rnnfile=rnnfile, $
                            halofile=halofile, rnn_halofile=rnn_halofile, $
                            simname=simname, boxsize=boxsize, $
                            hfile=hfile, bcg_mass_lim=bcg_mass_lim, paramfile=paramfile, $
                            catdir=catdir, ddir=ddir, execdir=execdir, srcdir=srcdir, $
                            pardir=pardir, cfgstr=cfgstr""")


            sdir = "'{0}'".format(os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower()))

            shutil.copyfile("{0}/scripts/make_buzzard_flock.pro".format(sdir[1:-1]),
                            "{0}/make_buzzard_flock.pro".format(jobbase))
            shutil.copyfile("{0}/scripts/make_params_files_buzzard.sh".format(sdir[1:-1]),
                            "{0}/make_params_files_buzzard.sh".format(jobbase))
            shutil.copyfile("{0}/scripts/make_l-addgals_submission_files.sh".format(sdir[1:-1]),
                            "{0}/make_l-addgals_submission_files.sh".format(jobbase))
            shutil.copyfile("{0}/scripts/run_cell.sh".format(sdir[1:-1]),
                            "{0}/run_cell.sh".format(jobbase))
            os.chmod("{0}/make_params_files_buzzard.sh".format(jobbase), 0o777)
            os.chmod("{0}/make_l-addgals_submission_files.sh".format(jobbase), 0o777)

        shutil.copyfile("{0}/scripts/submit_jobs_all.sh".format(sdir[1:-1]),
                        "{0}/addgals/submit_jobs_all.sh".format(self.getJobBaseDir()))

            
            
    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NTasks'] = self.cosmoparams['Addgals']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['Addgals']['NCoresPerTask']
        pars['NNodes'] = (int(pars['NTasks'])*int(pars['NCoresPerTask']) + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        jobbase = os.path.join(self.sysparams['JobBase'],
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               (self.__class__.__name__).lower())
        pars['Email'] = self.sysparams['Email']

        jobscript = self.jobtemp.format(**pars)

        spath = '{0}/job.{1}.sh'.format(jobbase, (self.__class__.__name__).lower())

        with open(spath, 'w') as fp:
            fp.write(jobscript)

        return spath
