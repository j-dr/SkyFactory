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

srun -n {NCores} shifter python3 /pyaddgals/bin/skyfactory/concat.py calclensconcat.yaml

echo "*****Done combining lensing files*****"

ls {OPath}/* > lensgalslist.txt
ls {TGDir}/*[0-9].fits > truthgalslist.txt
ls {HDir}/*[0-9].fits &> truthgalslist.txt

srun -n {NCores} -c {NCoresPerTask} shifter python3 /pyaddgals/bin/skyfactory/add_lensing.py calclensconcat.yaml
