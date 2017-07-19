#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adg
#SBATCH -o {SimName}{SimNum}-adg.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive

module load idl
source ~/.bashrc.ext
module unload PrgEnv-intel
module load PrgEnv-gnu
module load gsl 

idl -queue ../Lb1050/addgals/setup_addgals.idl
idl -queue ../Lb2600/addgals/setup_addgals.idl
idl -queue ../Lb4000/addgals/setup_addgals.idl

sh submit_jobs_all.sh | srun -n {NTasks} -c {NCoresPerTask} minions
