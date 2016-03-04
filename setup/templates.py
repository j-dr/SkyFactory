from __future__ import print_function
from abc import ABCMeta, abstractmethod
import yaml
import os


def read_yaml(fname):
    with open(fname,'r') as fp:
        config = yaml.load(fp)
    return config


class Template(object):
    """
    Class from which all other templates inherit
    """

    __metaclass__ = ABCMeta

    def __init__(self, simnum, system, cosmo):
        
        self.simnum = simnum
        self.sysname = system
        self.cosmo = cosmo

    def readSysConfig(self):
        
        sysfile = os.path.join('systems', self.sysname,'%s.yaml' % self.sysname)
        self.sysparams = read_yaml(sysfile)

    def readCosmoFile(self):
        
        cosmofile = os.path.join('%s.yaml' % self.cosmo)
        self.cosmoparams = read_yaml(cosmofile)

    def readConfigTemplateFile(self):

        templatefile = os.path.join('config', '%s.cfg' % self.__class__.__name__)
        
        with open(templatefile, 'r') as fp:
            cfgtemp = fp.readlines()
        
        self.cfgtemp = "".join(cfgtemp)

    def readJobTemplateFile(self):

        templatefile = os.path.join('systems', self.sysname,'%s.%s' % 
                                    (self.__class__.__name__, self.sysparams['Sched']))
        
        with open(templatefile, 'r') as fp:
            jobtemp = fp.readlines()

        self.jobtemp = "".join(jobtemp)
                                    

    @abstractmethod
    def setup(self):
        pass


class Rockstar(Template):

    def write_config(self,opath,spath,ns,nb,soft,nr,bsize,
                     mfdef='vir', w0=-1.0,wa=0.0,snap=False):
        fp = open(os.path.join(opath,"rockstar_%s.cfg" % bsize),'w')
        fp.write('#rockstar config file\n')
        fp.write('FILE_FORMAT = "LGADGET"\n')
        fp.write('GADGET_LENGTH_CONVERSION = 1\n')
        fp.write('GADGET_MASS_CONVERSION = 1e10\n')
        fp.write('INBASE="%s"\n' % spath)
        if snap:
            fp.write('FILENAME="snapdir_<snap>/snapshot_<snap>.<block>"\n')
        else:
            fp.write('FILENAME="lightcone/lightcone<snap>/snapshot_Lightcone_<snap>.<block>"\n')
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


    def setup(self):
        
        self.readSysConfig()
        self.readCosmoFile()
        self.readConfigTemplateFile()
        self.readJobTemplateFile()
        
        for i, bsize in enumerate(self.cosmoparams['BoxL']):
            ns = 1
            nb = self.cosmoparams['NumBlocks'][i]
            soft = self.cosmoparams['Soft'][i]
            nr = 256
            base = os.path.join(self.sysparams['OutputBase'],
                                 '{0}-{1}'.format(self.cosmoparams['SimName'],
                                                  self.simnum),
                                 "Lb%s" % bsize, 'output')

            ebase = os.path.join(self.sysparams['JobBase'],
                                 '{0}-{1}'.format(self.cosmoparams['SimName'],
                                                  self.simnum),
                                 "Lb%s" % bsize, self.__class__.__name__)
            try:
                os.makedirs(ebase)
            except:
                pass
            opath = os.path.join(base, 'halos')
            try:
                os.makedirs(opath)
            except:
                pass

            spath = os.path.join(base, 'lightcone')

            self.write_config(opath,spath,ns,nb,soft,nr,bsize)
            self.write_jobscript(opath, bsize)
