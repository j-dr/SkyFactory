from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
import os

from .basetemplate import BaseTemplate

class Rockstar(BaseTemplate):

    def __init__(self, simnum, system, cosmo):
        super(Rockstar, self).__init__(self, simnum, system, cosmo, outname='halos')

    def write_config(self,opath,bsize,mfdef='vir', w0=-1.0,wa=0.0,snap=False):
        ns = 1
        nb = self.cosmoparams['NumBlocks'][bsize]
        soft = self.cosmoparams['Soft'][bsize]
        nr = self.cosmoparams['ncores_rock']
        spath = os.path.join(self.sysparams['OutputBase'],
                             '{0}-{1}'.format(self.cosmoparams['SimName'],
                                              self.simnum),
                             "Lb%s" % bsize, 'output', 'lightcone')

        fp = open(os.path.join(opath,"rockstar_Lb%s.cfg" % bsize),'w')
        fp.write('#rockstar config file\n')
        fp.write('FILE_FORMAT = "LGADGET"\n')
        fp.write('GADGET_LENGTH_CONVERSION = 1\n')
        fp.write('GADGET_MASS_CONVERSION = 1e10\n')
        fp.write('INBASE="%s"\n' % spath)
        if snap:
            fp.write('FILENAME="snapdir_<snap>/snapshot_<snap>.<block>"\n')
        else:
            fp.write('FILENAME="lightcone<snap>/snapshot_Lightcone_<snap>.<block>"\n')
        fp.write('NUM_BLOCKS = %d\n' % nb)
        fp.write('FORCE_RES = %f\n' % soft)
        fp.write('NUM_SNAPS = %d\n' % ns)
        fp.write('\n')
        fp.write('#code configuration\n')
        fp.write('PARALLEL_IO = 1\n')
        fp.write('NUM_READERS = %d\n' % nr)
        fp.write('NUM_WRITERS = %d\n' % nr)
        fp.write('FORK_READERS_FROM_WRITERS = 1\n')
        fp.write('PARALLEL_IO_SERVER_INTERFACE = "ib0"\n')    
        fp.write('\n')
        fp.write('#halo finding\n')
        fp.write('STRICT_SO_MASSES = 1\n')
        fp.write('TEMPORAL_HALO_FINDING = 0\n')
        fp.write('MASS_DEFINITION = "%s"\n' % mfdef)
        fp.write('GADGET_SKIP_NON_HALO_PARTICLES = 1\n')
        fp.write('BOUND_PROPS = 1\n')
        if not snap:
            fp.write("LIGHTCONE = 1\n")
            fp.write("LIGHTCONE_ORIGIN = (0, 0, 0)\n")
            fp.write("LIGHTCONE_ALT_ORIGIN = (0, 0, 0)\n")
            
        fp.write('W0 = %0.20g\n' % w0)
        fp.write('WA = %0.20g\n' % wa)
        fp.write('\n')
        fp.write('#output\n')
        fp.write('OUTBASE = "./"\n')
        fp.write('OUTPUT_FORMAT = "BINARY"\n')
        fp.write('DELETE_BINARY_OUTPUT_AFTER_FINISHED = 1\n')
        fp.write('PRELOAD_PARTICLES = 0\n')
        fp.write('\n')
        fp.close()
        
        fp = open(os.path.join(opath,"snaps.txt"),'w')
        for i in xrange(ns):
            fp.write("%s\n" % i)
        fp.close()

    
    def write_jobscript(self, opath, boxl):
        
        pars = {}
        pars['SimName'] = self.cosmoparams['SimName']
        pars['BoxL'] = boxl
        pars['OPath'] = opath
        pars['NCores'] = self.cosmoparams['ncores_rock']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )/self.sysparams['CoresPerNode']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['Config'] = 'rockstar_Lb{0}.cfg'.format(boxl)
        pars['Email'] = self.sysparams['Email']
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],self.__class__.__name__)
        
        jobscript = self.jobtemp.format(**pars)
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), self.__class__.__name__)
                               
        with open('{0}/job.rockstar.{1}'.format(jobbase,self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
