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

srun -n {NCores} {ExecDir}/pixLC.py pixLC.cfg
{ExecDir}/bin/pixLC-symlink pixLC.cfg {ZLow} {ZHigh} {OBase}
{ExecDir}/bin/pixLC-halocut pixLC.cfg {HaloDir}/reform_out_0.list {HaloDir}/reform_out_0.parents
