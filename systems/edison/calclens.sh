#!/bin/bash
#SBATCH -p regular
#SBATCH -A {Repo}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rt
#SBATCH -o {SimName}{SimNum}-rt.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load PrgEnv-gnu cfitsio hdf5 fftw gsl

{GalCatListCMD}

srun -n {NCores} {ExecDir}/raytrace raytrace.cfg {Restart}
