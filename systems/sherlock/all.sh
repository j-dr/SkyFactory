#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -J {SimName}{SimNum}-all-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-all-Lb{BoxL}.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive