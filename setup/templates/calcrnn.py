from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class CalcRnn(BaseTemplate):

    def readConfigTemplateFile(self):

        templatefile = os.path.join('config', '%s.cfg' % self.__class__.__name__)
        
        with open(templatefile, 'r') as fp:
            halocfgtemp = fp.readlines()

        cfgtemp = []
        
        for l in halocfgtemp:
            if 'Halo' not in l:
                cfgtemp.append(l)
        
        self.cfgtemp = "".join(cfgtemp)
        self.halocfgtemp = "".join(halocfgtemp)

    def write_config(self, opath, boxl):

        osp = opath.split('/')
        osp[-1] = 'halos/out_0.parents'
        halopath = '/'.join(osp)

        pars = {}
        pars['SimType'] = self.cosmoparams['SimType']
        pars['SimName'] = self.cosmoparams['SimName']
        pars['SimNum'] = self.simnum
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), self.__class__.__name__)
        pars['NameFile'] = '{0}/{1}-{2}_Lb{3}.txt'.format(jobbase, pars['SimName'],
                                                              pars['SimNum'], boxl)

        pars['NCores'] = self.cosmoparams['ncores_rnn']
        pars['NRnn'] = self.cosmoparams['NRnn'][boxl]
        pars['OPath'] = opath
        pars['BBoxFile'] = '{0}/bboxindex.txt'.format(opath)
        pars['HFile'] = halopath
        cfg = self.cfgtemp.format(**pars)
        hcfg = self.halocfgtemp.format(**pars)

        with open('{0}/calcrnn_parts.cfg'.format(jobbase), 'w') as fp:
            fp.write(cfg)

        with open('{0}/calcrnn_halos.cfg'.format(jobbase), 'w') as fp:
            fp.write(hcfg)



    def write_jobscript(self, opath, boxl):
        osp = opath.split('/')
        osp[-1] = 'pixlc/'
        lcpath = '/'.join(osp)
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
        pars['NameFile'] = '{0}/{1}-{2}_Lb{3}.txt'.format(jobbase, pars['SimName'],
                                                          pars['SimNum'], boxl)
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],self.__class__.__name__)
        pars['OPath'] = opath
        pars['Email'] = self.sysparams['Email']
        pars['LPath'] = '{0}/*'.format(lcpath)
        
        jobscript = self.jobtemp.format(**pars)
        
        #write the lightcone files to be read by pixlc


        with open('{0}/job.rnn.{1}'.format(jobbase, self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
