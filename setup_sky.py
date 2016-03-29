#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import argparse
import templates
import os

default_tasks = ['UnarchiveLightcone', 'Rockstar', 'PixLC', 'CalcRnn', 'Addgals', 'CalcLens']

def main(num, system, cosmofile, tasks=default_tasks):

    sscripts = []

    #setup the individual jobs
    for i, task in enumerate(tasks):

        task = getattr(templates, task)
        task = getattr(task, task)
        t = task(num, system, cosmofile)
        t.setup()
        
        sscripts.append(t.getJobScriptName())

        #get a couple pieces of info we need to
        #write the general submission script
        if i==0:
            sysparams = t.sysparams
            cosmoparams = t.cosmoparams
            jobbase = t.jobbase
            
    #write the general submission script

    pars = {}
    pars['NCores'] = cosmoparams['Simulation']['NCores']
    pars['Repo'] = sysparams['Repo']
    pars['NNodes'] = cosmoparams['Simulation']['NNodes']
    pars['SimName'] = cosmoparams['Simulation']['SimName']
    pars['SimNum'] = num
    pars['Email'] = sysparams['Email']
    
    gsubtemp = read_yaml('systems', self.sysname, 'all.sh')
    jobheader = gsubtemp.format(**pars)
    if 'ReformatAddgals' in tasks:
        aidx = tasks.index('ReformatAddgals')
    else:
        aidx = len(tasks)

    with open("{0}/job.all.sh".format(jobbase, boxl), "w") as fp:
        fp.write(jobheader)

        #all tasks up to addgals reformatting must be done once
        #per box.
        for i, boxl in enumerate(cosmoparams['Simulation']['BoxL']):        
            for i, task in enumerate(tasks[:cidx]):
                fp.write("cd {0}/{1}".format(boxl, task))
                fp.write("------------- {0}.{1} -------------".format(task, boxl))
                fp.write("sh job.{0}.sh".format(task.lower()))
                fp.write("cd ../..")
                fp.write("\n")

        #everything afterwards is done once per suite
        for task in tasks[cidx:]:
            fp.write("cd {0}".format(task))
            fp.write("------------- {0} -------------".format(task))
            fp.write("sh job.{0}.sh".format(task.lower()))
            fp.write("cd ..")
            fp.write("\n")


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Setup a mock sky simulation")
    parser.add_argument("cosmofile", type=str)
    parser.add_argument("num", type=int)
    parser.add_argument("system", type=str)

    args = parser.parse_args()

    main(args.num, args.system, args.cosmofile)


