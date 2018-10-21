#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rt
#SBATCH -o {SimName}{SimNum}-rt.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive

module unload PrgEnv-gnu
module load PrgEnv-intel
module load cray-fftw
module load cfitsio cray-hdf5 gsl

{GalCatListCMD}

srun -n {NCores} {ExecDir}/raytrace raytrace.cfg {Restart}
