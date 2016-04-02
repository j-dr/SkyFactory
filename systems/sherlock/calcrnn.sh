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

cd {OPath}
ls {LPath} > {NameFile}

srun -n {NCores} {ExecDir}/calcrnn calcrnn_parts.cfg
srun -n {NCores} {ExecDir}/calcrnn calcrnn_halos.cfg