from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class DensMap(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(DensMap, self).__init__(simnum, system, cosmo, allboxes=True)
    
    def write_config(self, opath, boxl):
        # setup
        pars = {}
        plane_width = 25.0
        last_box = self.cosmoparams['Simulation']['BoxL'][-1]
        pars['RMax'] = self.cosmoparams['PixLC']['RMax'][last_box]        
        num_planes = int(pars['RMax']/plane_width)
        jobbase = os.path.join(self.getJobBaseDir(),
                               (self.__class__.__name__).lower())        
        if num_planes % 2 == 1:
            num_to_do = num_planes - 1
        else:
            num_to_do = num_planes

        self.num_cores = num_to_do//2
        
        pars['Nside'] = 2048 #FIXME hard coded!
        pars['LensPlanePath'] = os.path.join(self.getOutputBaseDir(),'pixlc')
        pars['LensPlaneName'] = 'snapshot_Lightcone'
        
        # write jobs to a file
        jobbase = os.path.join(self.getJobBaseDir(),
                               (self.__class__.__name__).lower())  
        with open('{0}/densmap.cmds'.format(jobbase), 'w') as fp:
            for i in xrange(num_to_do//2):
                pstr1 = '_%d' % (i*2)
                pstr2 = '_%d' % (i*2+1)                
                cmd = "%s/bin/pixLC-viz --verbose %d %s %s %s\n" % \
                    (self.getExecDir(),
                     pars['Nside'],
                     os.path.join(opath,'densmap%d.fits' % i),
                     os.path.join(pars['LensPlanePath'],pars['LensPlaneName']+pstr1),
                     os.path.join(pars['LensPlanePath'],pars['LensPlaneName']+pstr2))
                fp.write(cmd)

    def write_jobscript(self, opath, boxl):
        pars = {}
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['SimNum'] = self.simnum
        pars['ExecDir'] = self.getExecDir()
        pars['Repo'] = self.sysparams['Repo']
        pars['NCores'] = self.num_cores
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['Email'] = self.sysparams['Email']

        jobbase = os.path.join(self.getJobBaseDir(),
                               (self.__class__.__name__).lower())        
        jobscript = self.jobtemp.format(**pars)
        
        with open('{0}/job.densmap.sh'.format(jobbase), 'w') as fp:
            fp.write(jobscript)
