from __future__ import print_function
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class SurveyMags(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(SurveyMags, self).__init__(simnum, system, cosmo, allboxes=True)

    def write_config(self, opath, boxl):

        mpars = self.cosmoparams['SurveyMags']
        spars = self.cosmoparams['Simulation']
        cpath = os.path.join(self.getJobBaseDir(), self.__class__.__name__.lower(), 'magcommands.txt')
        cmd   = os.path.join(self.sysparams['ExecDir'], 'addgals', 'kcorrect_utils')
        opath = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'mags')
        obase = "{0}-{1}".format(spars['SimName'], self.simnum)
        inpath = os.path.join(self.getOutputBaseDir(), 'addgalspostprocess', 'truth',
                              '{0}-{1}_lensed.*.fits'.format(spars['SimName'], self.simnum))
        infiles = glob(inpath)

        try:
            os.makedirs(opath)
        except Exception as e:
            print(e)
            pass
        
        with open(cpath, 'w') as fp:
            for f in infiles:
                print("{0} {1} {2} {3} {4} {5}".format(cmd, f, opath, obase, self.sysparams['SFConfigBase']+'/Addgals', " ".join(mpars['Surveys'])), file=fp)


    def write_jobscript(self, opath, boxl):

        pars = {}
        pars['NTasks'] = self.cosmoparams['SurveyMags']['NTasks']
        pars['NCoresPerTask'] = self.cosmoparams['SurveyMags']['NCoresPerTask']
        pars['NNodes'] = (int(pars['NTasks'])*int(pars['NCoresPerTask']) + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['Email'] = self.sysparams['Email'] 
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']

        jobscript = self.jobtemp.format(**pars)

        spath = self.getJobScriptName()

        with open(spath, 'w') as fp:
            fp.write(jobscript)

        return spath
        

