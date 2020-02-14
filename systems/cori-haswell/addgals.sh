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
#SBATCH --image=docker:jderose/addgals-stack:latest
#SBATCH --volume="/global/project/projectdirs/des/jderose/SkyFactory-config:/SkyFactory-config;{OutputBase}:/output"

srun -n {NTasks} -c {NCoresPerTask} shifter python3 /pyaddgals/bin/addgals addgals.cfg

srun -n 1 -c 32 shifter python3 /pyaddgals/bin/make_halo_files.py addgals.cfg {HaloPath}

srun -n {NTasksShuffle} -c {NCoresPerTaskShuffle} shifter python3 /pyaddgals/bin/shuffle_colors.py "{GalPath}" {HaloPath} addgals.cfg {MHalo} {Scatter} {BuzzardRedSequenceModel} {DataRedSequenceModel} {NBands} {MStarPath}
