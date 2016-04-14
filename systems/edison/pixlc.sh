#!/bin/bash -l
#SBATCH -p regular
#SBATCH -t 12:00
#SBATCH -J {SimName}{SimNum}-plc-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-plc-Lb{BoxL}.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

srun -n {NCores} {ExecDir}/pixLC.py pixLC.cfg
{ExecDir}/bin/pixLC-symlink pixLC.cfg {ZLow} {ZHigh} {OBase} 
