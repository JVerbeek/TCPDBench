#!/bin/bash -e
#SBATCH --partition=icis
#SBATCH --account=icis
#SBATCH --gres=gpu:1
#SBATCH --mem=5G
#SBATCH --cpus-per-task=6
#SBATCH --time=6:00:00
#SBATCH --output=logs/tcpd-%j.out
#SBATCH --error=logs/tcpd-%j.err
#SBATCH --mail-type=BEGIN,END,FAIL


. $HOME/miniconda3/etc/profile.d/conda.sh 
conda activate tcpd
srun --mpi=pmix -n 4 abed local