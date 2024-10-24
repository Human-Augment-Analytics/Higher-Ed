#!/bin/bash
#SBATCH -J DLC_model_training
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --gres=gpu:H100:1            # Requesting 1 GPU (e.g., H100)
#SBATCH --cpus-per-task=4            # Requesting 4 CPUs
#SBATCH --mem=64GB                   # Requesting 64GB of memory
#SBATCH -t 0-16:00:00                # Requesting n hours
#SBATCH -o DLC_Training_Test1_Report-%j.out   # Output file
#SBATCH --mail-type=BEGIN,END,FAIL   # Notifications on job start/end/fail
#SBATCH --mail-user=kcozart6@gatech.edu # Replace with your email

cd $SLURM_SUBMIT_DIR                 # Change to working directory
conda activate DEEPLABCUT
srun python /home/hice1/kcozart6/scratch/test_training_script.py   # Run your training script
