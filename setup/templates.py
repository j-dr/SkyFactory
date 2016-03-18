from __future__ import print_function
from abc import ABCMeta, abstractmethod
from glob import glob
import shutil
import yaml
import stat
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

    def __init__(self, simnum, system, cosmo, **kwargs):
        
        self.simnum = simnum
        self.sysname = system
        self.cosmo = cosmo
        if 'outname' not in kwargs.keys():
            self.outname = (self.__class__.__name__).lower()
        else:
            self.outname = kwargs['outname']

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
                                    

    def setup(self):
        
        self.readSysConfig()
        self.readCosmoFile()
        self.readConfigTemplateFile()
        self.readJobTemplateFile()
        
        for i, bsize in enumerate(self.cosmoparams['BoxL']):

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

            opath = base+'/{0}'.format(self.outname)

            try:
                os.makedirs(opath)
            except:
                pass

            self.write_jobscript(opath, bsize)
            self.write_config(opath, bsize)

class Rockstar(Template):

    def __init__(self, simnum, system, cosmo):
        Template.__init__(self, simnum, system, cosmo, outname='halos')

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


class UnarchiveLightcone(Template):

    def __init__(self, simnum, system, cosmo):
        Template.__init__(self, simnum, system, cosmo, outname='lightcone')

    def readConfigTemplateFile(self):
        pass

    def write_config(self, opath, boxl):
        pass

    def write_jobscript(self, opath, boxl):
        
        pars = {}
        pars['SimName'] = self.cosmoparams['SimName']
        pars['BoxL'] = boxl
        pars['OPath'] = opath
        pars['SimNum'] = self.simnum
        pars['Email'] = self.sysparams['Email']
        if self.sysname=='edison':
            pars['Cluster'] = "esedison"

        elif self.sysname=="cori":
            pars['Cluster'] = "escori"

        if pars["SimName"] == "Chinchilla":
            pars['Group'] = "Herd"

        jobscript = self.jobtemp.format(**pars)
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}-{1}'.format(pars['SimName'], pars['SimNum']),
                               'Lb{0}'.format(boxl), self.__class__.__name__)
                               
        with open('{0}/job.unarchive.{1}'.format(jobbase,self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)


class PixLC(Template):

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


class CalcRnn(Template):

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


class Addgals(Template):

    def write_config(self, opath, boxl):
        pars = {}
        bopath = '/'.join(opath.split('/')[:-1])
        bsbase = bopath.split('Lb{0}'.format(boxl))
        sn = '{0}-{1}'.format(self.cosmoparams['SimName'], self.simnum)
        pars['SimName'] = "'{0}'".format(sn)
        pars['SimNum'] = self.simnum
        pars['Boxl' ] = "'{0}'".format(boxl)
        pars['Halos'] = "'{0}/{1}'".format(bopath, 'halos/out_0.parents')
        pars['HaloRnn'] = "'{0}/{1}'".format(bopath, 'rnn/rnn_out_0.parents')
        pars['LCDir'] = "'{0}/{1}/'".format(bopath, 'pixlc')
        pars['SDir'] = "'{0}'".format(os.path.join(self.sysparams['ExecDir'],self.__class__.__name__))
        pars['OmegaM'] = self.cosmoparams['OmegaM']
        pars['OmegaL'] = self.cosmoparams['OmegaL']
        pars['ZMin'] = self.cosmoparams['SimZmin'][boxl]
        pars['ZMax'] = self.cosmoparams['SimZmax'][boxl]
        pars['NZbins'] = self.cosmoparams['NZbins'][boxl]
        pars['BCGMassLim'] = "'{0}'".format(self.cosmoparams['BCGMassLim'][boxl])
        
        jobbase = os.path.join(self.sysparams['JobBase'], 
                               '{0}'.format(sn),
                               'Lb{0}'.format(boxl), self.__class__.__name__)
        pars['OPath'] = "'{0}'".format(opath)
        pars['PFile'] = "'{0}'".format(self.cosmoparams['ParamFile'])
        cfg = self.cfgtemp.format(**pars)

        shutil.copyfile("{0}/scripts/make_buzzard_flock.pro".format(pars['SDir'][1:-1]),
                        "{0}/make_buzzard_flock.pro".format(jobbase))
        shutil.copyfile("{0}/scripts/make_params_files_buzzard.sh".format(pars['SDir'][1:-1]),
                        "{0}/make_params_files_buzzard.sh".format(jobbase))
        shutil.copyfile("{0}/scripts/make_l-addgals_submission_files.sh".format(pars['SDir'][1:-1]),
                        "{0}/make_l-addgals_submission_files.sh".format(jobbase))
        os.chmod("{0}/make_params_files_buzzard.sh".format(jobbase), 0o777)
        os.chmod("{0}/make_l-addgals_submission_files.sh".format(jobbase), 0o777)
        with open('{0}/setup_addgals.idl'.format(jobbase), 'w') as fp:
            fp.write(cfg)


    def write_jobscript(self, opath, boxl):
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
        pars['Email'] = self.sysparams['Email']
        
        jobscript = self.jobtemp.format(**pars)
        
        with open('{0}/job.adg.{1}'.format(jobbase, self.sysparams['Sched']), 'w') as fp:
            fp.write(jobscript)
    
