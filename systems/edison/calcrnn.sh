#!/bin/bash
#SBATCH -p regular
#SBATCH -t 12:00
#SBATCH -J {SimName}{SimNum}-plc-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-plc-Lb{BoxL}.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

{SysExecDir}/pixlc/bin/pixLC-socts {JDir}/pixlc/pixLC.cfg 0 1 > {NameFile}

srun -n {NCores} {ExecDir}/calcrnn calcrnn_parts.cfg
srun -n {NCores} {ExecDir}/calcrnn calcrnn_halos.cfg