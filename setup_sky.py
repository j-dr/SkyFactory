#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import argparse
import templates
import os

default_tasks = ['UnarchivePreprocess', 'PixLC', 'CalcRnn', 'Addgals', 'Calclens', 'CalclensPostProcess', 'ErrorModel', 'Archive']
#default_tasks = ['Redmapper', 'SampleSelection', 'Sompz']


def main(cosmofile, num, system, tasks=default_tasks, only_all_sub=False):

    sscripts = []

    # setup the individual jobs
    for i, task in enumerate(tasks):
        print("Setting up {0}".format(task))
        task = getattr(templates, task)
        #task = getattr(taskmod, task)
        t = task(num, system, cosmofile)
        if not only_all_sub:
            t.setup()
        else:
            t.setup(nowrite=True)

        sscripts.append(t.getJobScriptName())

        # get a couple pieces of info we need to
        # write the general submission script
        if i == 0:
            sysparams = t.sysparams
            cosmoparams = t.cosmoparams
            jobbase = t.jobbase
            outputbase = t.getOutputBaseDir()

    # write the general submission script

    pars = {}
    pars['Queue'] = sysparams['Queue']
    pars['QOS'] = sysparams['QOS']
    pars['NCores'] = cosmoparams['Simulation']['NCores']
    pars['Repo'] = sysparams['Repo']
    pars['NNodes'] = (
        pars['NCores'] + sysparams['CoresPerNode'] - 1) // sysparams['CoresPerNode']
    pars['SimName'] = cosmoparams['Simulation']['SimName']
    pars['SimNum'] = num
    pars['Email'] = sysparams['Email']
    pars['TimeLimitHours'] = sysparams['TimeLimitHours']
    pars['OutputBase'] = outputbase

    with open(os.path.join('systems', system, 'all.sh'), 'r') as fp:
        gsubtemp = fp.readlines()
    gsubtemp = ''.join(gsubtemp)

    jobheader = gsubtemp.format(**pars)
    if 'Addgals' in tasks:
        aidx = tasks.index('Addgals')
    else:
        aidx = len(tasks)

    with open("{0}/job.all.sh".format(jobbase), "w") as fp:
        fp.write(jobheader)
        fp.write("\n")
        fp.write('umask 022 \n')
        # all tasks up to addgals reformatting must be done once
        # per box.
        for i, task in enumerate(tasks[:aidx]):
            if 'archive' in task.lower(): continue
            for i, boxl in enumerate(cosmoparams['Simulation']['BoxL']):
                fp.write("cd Lb{0}/{1}\n".format(boxl, task.lower()))
                fp.write(
                    'echo "------------- {0}.{1} -------------"\n'.format(task, boxl))
                fp.write("echo 'Beginning at'$( date +%T ) \n")
                fp.write("sh job.{0}.sh\n".format(task.lower()))
                fp.write("cd ../..\n")
                fp.write("\n")

        # everything afterwards is done once per suite
        for task in tasks[aidx:]:
            if 'archive' in task.lower(): continue
            fp.write("cd {0}\n".format(task.lower()))
            fp.write('echo "------------- {0} -------------"\n'.format(task))
            fp.write("echo 'Beginning at'$( date +%T ) \n")
            fp.write("sh job.{0}.sh\n".format(task.lower()))
            if task.lower() == 'calclens':
                fp.write("if [ $? -ne 0 ]\n")
                fp.write("then\n")
                fp.write("  sh job.calclens.restart.sh\n")
                fp.write("fi\n")

            fp.write("cd ..\n")
            fp.write("\n")

        fp.write('chgrp -R des {}/{}-{} \n'.format(sysparams['OutputBase'], pars['SimName'], pars['SimNum']))

        fp.write("echo 'Sky completed at '$( date +%T ) \n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Setup a mock sky simulation")
    parser.add_argument("cosmofile", type=str)
    parser.add_argument("num", type=int)
    parser.add_argument("system", type=str)
    parser.add_argument("--nowrite", dest='nowrite', action='store_true')
    parser.set_defaults(nowrite=False)

    args = parser.parse_args()

    main(args.cosmofile, args.num, args.system, only_all_sub=args.nowrite)
