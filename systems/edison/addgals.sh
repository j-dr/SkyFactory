#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adg-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-adg-Lb{BoxL}.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load idl
source ~/.bashrc.ext
module unload PrgEnv-intel
module load PrgEnv-gnu
module load gsl 

idl -queue setup_addgals.idl

sh submit_jobs.sh | srun -n {NTasks} -c {NCoresPerTask} minions
