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
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
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
            fp.write("namefile   : {NameFile}\n".format(**pars))
            fp.write("outpath    : {OPath}\n".format(**pars))
            fp.write("rmin       : {RMin}\n".format(**pars))
            fp.write("rmax       : {RMax}\n".format(**pars))
            fp.write("lfilenside : {LFileNside}\n".format(**pars))
            fp.write("rr0        : {RR0}\n".format(**pars))
            fp.write("prefix     : {Prefix}\n".format(**pars))

    def write_jobscript(self, opath, boxl):
        osp = opath.split('/')
        osp[-1] = 'lightcone/lightcone'
        lcpath = '/'.join(osp)
        pars = {}
        pars['BoxL'] = boxl
        pars['HaloDir'] = "{0}/Lb{1}/output/halos/".format(self.getOutputBaseDir(), boxl)
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['ExecDir'] = self.getExecDir()
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.cosmoparams['PixLC']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['ZLow'] = self.cosmoparams['Addgals']['SimZmin'][boxl]
        pars['ZHigh'] = self.cosmoparams['Addgals']['SimZmax'][boxl]
        pars['OBase'] = self.getOutputBaseDir()+'/pixlc'
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

        with open('{0}/job.pixlc.sh'.format(jobbase), 'w') as fp:
            fp.write(jobscript)
