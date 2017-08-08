#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rtpp
#SBATCH -o {SimName}{SimNum}-rtpp.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive


srun -n {NCores} python {ExecDir}/scripts/concat.py calclensconcat.yaml

echo "*****Done combining lensing files*****"

ls {OPath}/* > lensgalslist.txt
ls {TGDir}/* > truthgalslist.txt
ls {THDir}/*halo* >> truthgalslist.txt

srun -n {NCores} python {AExecDir}/scripts/add_lensing.py calclensconcat.yaml
