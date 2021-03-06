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
        super(Rockstar, self).__init__(simnum, system, cosmo, outname='halos')

    def write_config(self,opath,bsize,mfdef='vir', w0=-1.0,wa=0.0,snap=False):
        ns = 1
        nb = self.cosmoparams['Simulation']['NumBlocks'][bsize] * self.cosmoparams['Simulation']['NumOctants']
        soft = self.cosmoparams['Simulation']['Soft'][bsize]
        nr = self.cosmoparams['Rockstar']['NCores']

        om = self.cosmoparams['Cosmology']['OmegaM']
        ol = self.cosmoparams['Cosmology']['OmegaL']
        h0 = self.cosmoparams['Cosmology']['h']
        
        spath = os.path.join(self.sysparams['OutputBase'],
                             '{0}-{1}'.format(self.cosmoparams['Simulation']['SimName'],
                                              self.simnum),
                             "Lb%s" % bsize, 'output', 'lightcone')

        fp = open(os.path.join(opath,"rockstar_Lb%s.cfg" % bsize),'w')
        fp.write('#rockstar config file\n')
        fp.write('FILE_FORMAT = "GADGET2"\n')
        fp.write('GADGET_LENGTH_CONVERSION = 1\n')
        fp.write('GADGET_MASS_CONVERSION = 1e10\n')
        fp.write('INBASE="%s"\n' % spath)
        if snap:
            fp.write('FILENAME="snapdir_<snap>/snapshot_<snap>.<block>"\n')
        else:
            fp.write('FILENAME="lightcone<snap>/snapshot_Lightcone_<snap>.<block>"\n')
        fp.write('NUM_BLOCKS = %d\n' % nb)
        fp.write('FORCE_RES = %f\n' % soft)
        fp.write('Om = %f\n' % om)
        fp.write('Ol = %f\n' % ol)
        fp.write('h0 = %f\n' % h0)        
        fp.write('NUM_SNAPS = %d\n' % ns)
        fp.write('STARTING_SNAP = %d\n' % 0)        
        fp.write('\n')
        fp.write('#code configuration\n')
        fp.write('PARALLEL_IO = 1\n')
        fp.write('NUM_READERS = %d\n' % nr)
        fp.write('NUM_WRITERS = %d\n' % nr)
        fp.write('FORK_READERS_FROM_WRITERS = 1\n')
        fp.write('PARALLEL_IO_SERVER_INTERFACE = "ib0"\n')    
        fp.write('\n')
        fp.write('#halo finding\n')
        fp.write('MASS_DEFINITION = "%s"\n' % mfdef)
        fp.write('GADGET_SKIP_NON_HALO_PARTICLES = 1\n')
        fp.write('BOUND_PROPS = 1\n')
        if not snap:
            fp.write("LIGHTCONE = 1\n")
            fp.write("LIGHTCONE_ALT_ORIGIN = (0, 0, 0)\n")
            fp.write('SNAPSHOT_NAMES = "snaps.txt"\n')
            fp.write('LIGHTCONE_ALT_SNAPS = "snaps2.txt"\n')
            
        fp.write('\n')
        fp.write('#output\n')
        fp.write('OUTBASE = "./"\n')
        fp.write('OUTPUT_FORMAT = "BINARY"\n')
        fp.write('DELETE_BINARY_OUTPUT_AFTER_FINISHED = 1\n')
        fp.write('PRELOAD_PARTICLES = 0\n')
        fp.write('\n')
        fp.close()
        
        fp = open(os.path.join(opath,"snaps.txt"),'w')
        for i in range(ns):
            fp.write("00%s\n" % i)

        fp = open(os.path.join(opath,"snaps2.txt"),'w')
        for i in range(ns):
            fp.write("00%s\n" % str(int(i)+1))
            
        fp.close()

    
    def write_jobscript(self, opath, boxl):
        
        pars = {}
        pars['Queue'] = self.sysparams['Queue']
        pars['QOS'] = self.sysparams['QOS']
        pars['SimName'] = self.cosmoparams['Simulation']['SimName']
        pars['BoxL'] = boxl
        pars['OPath'] = opath
        pars['NCores'] = self.cosmoparams['Rockstar']['NCores']
        pars['NNodes'] = (pars['NCores'] + self.sysparams['CoresPerNode'] - 1 )//self.sysparams['CoresPerNode']
        pars['TimeLimitHours'] = self.sysparams['TimeLimitHours']
        pars['SimNum'] = self.simnum
        pars['Repo'] = self.sysparams['Repo']
        pars['Config'] = 'rockstar_Lb{0}.cfg'.format(boxl)
        pars['Email'] = self.sysparams['Email']
        pars['ExecDir'] = os.path.join(self.sysparams['ExecDir'],(self.__class__.__name__).lower())
        
        jobscript = self.jobtemp.format(**pars)
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), (self.__class__.__name__).lower())
                               
        with open('{0}/job.rockstar.sh'.format(jobbase), 'w') as fp:
            fp.write(jobscript)
