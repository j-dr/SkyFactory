#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-plc-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-plc-Lb{BoxL}.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load py-numpy

{SysExecDir}/pixlc/bin/pixLC-socts {JDir}/pixlc/pixLC.cfg 0 1 > {NameFile}

srun -n {NCores} {ExecDir}/calcrnn calcrnn_parts.cfg {NCores}
srun -n {NCores} {ExecDir}/calcrnn calcrnn_halos.cfg {NCores}
