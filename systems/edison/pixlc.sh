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
#SBATCH --exclusive

module load python/2.7-anaconda 

ls {LCPath} > {NameFile}

srun -n {NCores} {ExecDir}/pixLC.py pixLC.cfg

{ExecDir}/bin/pixLC-symlink pixLC.cfg {ZLow} {ZHigh} {OBase}
srun -n {NNodes} -c {CoresPerNode} {ExecDir}/bin/pixLC-halocut pixLC.cfg {MMin} {HaloDir}/out_0.list {HaloDir}/reform_out_0.parents

{ExecDir}/bin/pixLC-socts pixLC.cfg 0 1 > haloassoc_pix.txt
srun -n {NTasks} -c {NCoresPerTask} {ExecDir}/bin/pixLC-haloassoc haloassoc_pix.txt {HaloDir}/cut_reform_out_0.parents 
