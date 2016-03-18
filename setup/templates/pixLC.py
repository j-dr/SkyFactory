from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class PixLC(BaseTemplate):

    def write_config(self, opath, boxl):

        for lcnum in ['000', '001']:
            pars = {}
            pars['SimName'] = self.cosmoparams['SimName']
            pars['SimNum'] = self.simnum
            jobbase = os.path.join(self.sysparams['JobBase'], 
                                   '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                                   'Lb{0}'.format(boxl), self.__class__.__name__)
            pars['NameFile'] = '{0}/{1}-{2}_Lb{3}_{4}.txt'.format(jobbase, pars['SimName'],
                                                                  pars['SimNum'], boxl, 
                                                                  lcnum)
            pars['RMin'] = self.cosmoparams['RMin'][boxl]
            pars['RMax'] = self.cosmoparams['RMax'][boxl]
            pars['LFileNside'] = 1 #self.cosmoparams['LFileNside'][boxl]
            pars['RR0'] = self.cosmoparams['RR0'][boxl]
            pars['Prefix'] = '{0}_{1}'.format('snapshot_Lightcone', lcnum)
            pars['OPath'] = opath

            cfg = self.cfgtemp.format(**pars)

            with open('{0}/pixLC.{1}.cfg'.format(jobbase, lcnum), 'w') as fp:
                fp.write(cfg)


    def write_jobscript(self, opath, boxl):
        osp = opath.split('/')
        osp[-1] = 'lightcone/lightcone'
        lcpath = '/'.join(osp)

        for lcnum in ['000', '001']:

            pars = {}
            pars['BoxL'] = boxl
            pars['SimName'] = self.cosmoparams['SimName']
            pars['SimNum'] = self.simnum
            pars['Repo'] = self.sysparams['Repo']
            pars['NCores'] = self.cosmoparams['ncores_pixlc']
            pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
            jobbase = os.path.join(self.sysparams['JobBase'], 
                                   '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                                   'Lb{0}'.format(boxl), self.__class__.__name__)
            pars['NameFile{0}'.format(lcnum)] = '{0}/{1}-{2}_Lb{3}_{4}.txt'.format(jobbase, pars['SimName'],
                                                                                   pars['SimNum'], boxl, 
                                                                                   lcnum)
            pars['OPath'] = opath
            pars['Email'] = self.sysparams['Email']

            
            jobscript = self.jobtemp.format(**pars)

            #write the lightcone files to be read by pixlc
            lcfiles = glob('{0}{1}/snapshot_Lightcone*'.format(lcpath, lcnum))

            with open(pars['NameFile{0}'.format(lcnum)], 'w') as fp:
                fbuff = '\n'.join(lcfiles)
                fp.write(fbuff)

        with open('{0}/job.pl.{1}'.format(jobbase, self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
