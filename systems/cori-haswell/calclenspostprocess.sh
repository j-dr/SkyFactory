#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rtpp
#SBATCH -o {SimName}{SimNum}-rtpp.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive

module load python/3.6-anaconda-4.4

srun -n {NCores} python {ExecDir}/scripts/concat.py calclensconcat.yaml

echo "*****Done combining lensing files*****"

ls {OPath}/* > lensgalslist.txt
ls {TGDir}/*[0-9].fits > truthgalslist.txt

srun -n {NCores} python {AExecDir}/scripts/add_lensing.py calclensconcat.yaml
