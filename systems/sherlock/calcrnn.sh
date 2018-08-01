#!/bin/bash
#SBATCH -p iric,hns,normal
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-plc-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-plc-Lb{BoxL}.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

{SysExecDir}/pixlc/bin/pixLC-socts {JDir}/pixlc/pixLC.cfg 0 1 > {NameFile}
ls {OctPath}/lightcone00[0-1]/snap* > {HaloNameFile}

srun -n {NCores} {ExecDir}/calcrnn calcrnn_parts.cfg
srun -n {NCores} {ExecDir}/calcrnn calcrnn_halos.cfg

ln -s {OPath}/* {LCPath}/
