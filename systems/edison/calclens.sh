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

module swap PrgEnv-intel PrgEnv-gnu
module swap fftw/2.1.5.9 fftw/3.3.4.9
module load cfitsio hdf5 gsl

{GalCatListCMD}

srun -n {NCores} {ExecDir}/raytrace raytrace.cfg {Restart}
