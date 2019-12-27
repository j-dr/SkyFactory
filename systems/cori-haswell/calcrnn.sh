#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-plc-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-plc-Lb{BoxL}.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive

#module load gsl

#{SysExecDir}/pixlc/bin/pixLC-socts {JDir}/pixlc/pixLC.cfg 0 1 > {NameFile}
#ls {OctPath}/lightcone00[0-1]/snap* > {HaloNameFile}

#srun -n {NCores} {ExecDir}/calcrnn calcrnn_parts.cfg 4
#srun -n {NCores} {ExecDir}/calcrnn calcrnn_halos.cfg 4

ln -s {OPath}/* {LCPath}/
ln -s {OPath}/rnn*out* {HaloPath}
