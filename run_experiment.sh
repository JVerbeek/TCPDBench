#!/usr/bin/env bash
#SBATCH --partition=icis
#SBATCH --account=icis
#SBATCH --qos=das-normal
#SBATCH --account=das
#SBATCH --mem=10G
#SBATCH --cpus-per-task=4
#SBATCH --time=12:00:00
#SBATCH --output=logs/experiment1_%A_%a.out
#SBATCH --error=logs/experiment1_%A_%a.err
#SBATCH --mail-type=BEGIN,END,FAIL

# hyperparameters
. $HOME/miniconda3/etc/profile.d/conda.sh

conda activate gp
mpiexec -np 4 abed local

