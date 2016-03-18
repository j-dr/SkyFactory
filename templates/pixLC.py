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

        pars = {}
        pars['SimName'] = self.cosmoparams['SimName']
        pars['SimNum'] = self.simnum
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), (self.__class__.__name__).lower())
        pars['NameFile'] = '{0}/{1}-{2}_Lb{3}.txt'.format(jobbase, pars['SimName'],
                                                                  pars['SimNum'], boxl)
        pars['RMin'] = self.cosmoparams['PixLC']['RMin'][boxl]
        pars['RMax'] = self.cosmoparams['PixLC']['RMax'][boxl]
        pars['LFileNside'] = 1
        pars['RR0'] = self.cosmoparams['PixLC']['RR0'][boxl]
        pars['Prefix'] = '{0}'.format('snapshot_Lightcone')
        pars['OPath'] = opath
        with open('{0}/pixLC.cfg'.format(jobbase), 'w') as fp:
            fp.write("namefile   : {NameFile}".format(**pars))
            fp.write("outpath    : {OPath}".foramt(**pars))
            fp.write("rmin       : {RMin}".format(**pars))
            fp.write("rmax       : {RMax}".format(**pars))
            fp.write("lfilenside : {LFileNside}".format(**pars))
            fp.write("rr0        : {RR0}".format(**pars))
            fp.write("prefix     : {Prefix}".format(**pars))

    def write_jobscript(self, opath, boxl):
        osp = opath.split('/')
        osp[-1] = 'lightcone/lightcone'
        lcpath = '/'.join(osp)
        pars = {}
        pars['BoxL'] = boxl
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.cosmoparams['PixLC']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), (self.__class__.__name__).lower())
        pars['NameFile'] = '{0}/{1}-{2}_Lb{3}.txt'.format(jobbase, pars['SimName'],
                                                          pars['SimNum'], boxl)
        pars['OPath'] = opath
        pars['Email'] = self.sysparams['Email']
        
        jobscript = self.jobtemp.format(**pars)

        #write the lightcone files to be read by pixlc
        lcfiles = glob('{0}*/snapshot_Lightcone*'.format(lcpath))
        
        with open(pars['NameFile'], 'w') as fp:
            fbuff = '\n'.join(lcfiles)
            fp.write(fbuff)

        with open('{0}/job.pixlc.{1}'.format(jobbase, self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
