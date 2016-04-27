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

        templatefile = os.path.join('config', '%s.cfg' % (self.__class__.__name__).lower())
        
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
        osp[-1] = 'halos/cut_out_0.parents.reformat'
        halopath = '/'.join(osp)
        pars = {}
        pars['SimType'] = self.cosmoparams['Simulation']['SimType']
        if pars['SimType']=='LGADGETBCCLC':
            pars['HaloSimType'] = 'LGADGET'
        else:
            pars['HaloSimType'] = pars['SimType']
            
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['NCores'] = self.cosmoparams['CalcRnn']['NCores']
        pars['NRnn'] = self.cosmoparams['CalcRnn']['NRnn'][boxl]
        pars['OPath'] = opath
        pars['BBoxFile'] = '{0}/bboxindex.txt'.format(opath)
        pars['HaloBBoxFile'] = '{0}/bboxindex_halos.txt'.format(opath)
        pars['HFile'] = halopath

        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), (self.__class__.__name__).lower())

        pars['NameFile'] = '{0}/{1}-{2}_Lb{3}.txt'.format(jobbase, pars['SimName'],
                                                              pars['SimNum'], boxl)

        pars['HaloNameFile'] = '{0}/{1}-{2}_Lb{3}_halos.txt'.format(jobbase, pars['SimName'],
                                                          pars['SimNum'], boxl)
        
        with open('{0}/calcrnn_halos.cfg'.format(jobbase), 'w') as fp:
            fp.write("OutputPath              {0}\n".format(opath))
            fp.write("NumTasksIOInParallel    {0}\n".format(pars['NCores']))
            fp.write("SimulationType          {0}\n".format(pars['HaloSimType']))
            fp.write("SnapshotFileList        {0}\n".format(pars['HaloNameFile']))
            fp.write("BBoxOutputFile          {0}\n".format(pars['HaloBBoxFile']))
            fp.write("HaloFile                {0}\n".format(pars['HFile']))
            fp.write("HaloFileFormat          SKELETON\n")
            fp.write("HaloChunkSizeMB         500\n")
            fp.write("DomainBuffSize          25.0\n")
            fp.write("NRnn                    {0}\n".format(pars['NRnn']))
            fp.write("NDiv                    8\n")

        with open('{0}/calcrnn_parts.cfg'.format(jobbase), 'w') as fp:
            fp.write("OutputPath              {0}\n".format(opath))
            fp.write("NumTasksIOInParallel    {0}\n".format(pars['NCores']))
            fp.write("SimulationType          {0}\n".format(pars['SimType']))
            fp.write("SnapshotFileList        {0}\n".format(pars['NameFile']))
            fp.write("BBoxOutputFile          {0}\n".format(pars['BBoxFile']))
            fp.write("DomainBuffSize          25.0\n")
            fp.write("NRnn                    {0}\n".format(pars['NRnn']))
            fp.write("NDiv                    8\n")


    def write_jobscript(self, opath, boxl):
        osp = opath.split('/')
        osp[-1] = 'pixlc/'
        lcpath = '/'.join(osp)
        osp = opath.split('/')
        osp[-1] = 'lightcone/'
        octpath = '/'.join(osp)
        pars = {}
        pars['BoxL'] = boxl
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.cosmoparams['CalcRnn']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), (self.__class__.__name__).lower())
        pars['NameFile'] = '{0}/{1}-{2}_Lb{3}.txt'.format(jobbase, pars['SimName'],
                                                          pars['SimNum'], boxl)
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower())
        pars['SysExecDir'] = self.sysparams['ExecDir']
        pars['JDir'] = os.path.join(self.getJobBaseDir(),"Lb%s" % boxl)
        pars['OctPath'] = octpath
        pars['OPath'] = opath
        pars['Email'] = self.sysparams['Email']
        pars['LCPath'] = '{0}/'.format(lcpath)
        
        jobscript = self.jobtemp.format(**pars)
        
        #write the lightcone files to be read by pixlc


        with open('{0}/job.calcrnn.sh'.format(jobbase), 'w') as fp:
            fp.write(jobscript)
