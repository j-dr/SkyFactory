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

#module load python/2.7-anaconda 

#ls {LCPath} > {NameFile}

#srun -n {NCores} shifter {ExecDir}/pixLC.py pixLC.cfg

shifter python3 {ExecDir}/bin/pixLC-symlink pixLC.cfg {ZLow} {ZHigh} {OBase}
#srun -n {NNodes} -c {CoresPerNode} shifter {ExecDir}/bin/pixLC-halocut pixLC.cfg {HaloDir}/out_0.list {HaloDir}/reform_out_0.parents

shifter python3 {ExecDir}/bin/pixLC-socts pixLC.cfg 0 1 > haloassoc_pix.txt
srun -n {NTasks} -c {NCoresPerTask} shifter python3 {ExecDir}/bin/pixLC-haloassoc haloassoc_pix.txt {HaloDir}/cut_reform_out_0.parents {MMin}
