# Authors and Sources
This documentation is a combination of Michael Falter's basic PACE instructions, Thuan Nguyen's training DLC on cichlid data on ICE node instructions, and my own notes. The majority of this is taken directly from Thuan Nguyen. Documentation, Google searches, and generative AI were also used.

# Purpose
This documentation is for researchers who are completely new to PACE and DLC. It is written for the Cichlid CV team's re-identification project.

# Documentation

## Download Gatech VPN (Required for Off Campus Researchers)
(1) Download GlobalProtect VPN Client from vpn.gatech.edu website. More details can be found at https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042139 if needed. The kb article has OS-specific VPN configuration instructions.

## Ensure the Higher Education Team has Requested PACE Access
(1) Students from CS 6999 and CS 8903 must be added every semester by helpdesk@cc.gatech.edu . The Higher Education team should be responsible for this. Additionally, to use the DropBox for McGrath Labs, an email request should be sent to support@arcs.gatech.edu and patrick.mcgrath@biology.gatech.edu .

## EVERY TIME: Use Gatech VPN
(1) Open GlobalConnect and enter vpn.gatech.edu , then click connect.
(2) Enter your gatech username (NOT email) and your password.
(3) Use your perferred 2FA. For phone call 2FA, enter "phone1" or "phone2," and press one on your phone when you are called.

## EVERY TIME: Connect to ICE Using Preferred Command Line
(1) In Windows, it would be recommended to use PowerShell or something with administration privileges.
(2) Use ssh <username>@login-ice.pace.gatech.edu and you password to connect to ICE clusters.
(3) To create Jobs and use GUI services, connect via https://ondemand-ice.pace.gatech.edu/ in your browser. See the following link for more details on OnDemand and links to other compute clusters: https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042133 .
(4) Click on "Interactive Apps" and choose your favorite. I will be using Jupyter Notebook. Choose your settings, especially the number of hours. It will take a few moments to connect to ICE.

## Install DLC
(1) In the Jupyter Notebook, there is an "ondemand" folder and a "scratch" folder. You want to put your code in "scratch" because this is persistant between sessions. In contrast, the "ondemand" folder is typically associated with web interface sessions and might not be there after your session ends. 
(2) Download or copy the content of `DEEPLABCUT.yaml` onto your desktop. The file can be found here: https://github.com/DeepLabCut/DeepLabCut/blob/main/conda-environments/DEEPLABCUT.yaml .
(3) Drag `DEEPLABCUT.yaml` into the scratch folder of your Jupyter Notebook. Make sure you press the "Upload" button after dragging it over. Otherwise, the file will not actually exist when you go to use it.
(4) In Jupyter Notebook, press "New" and then "Bash." Do NOT use "Bash [conda env:root]*," as this would make changes to the whole base environment.
(5) In Bash, run the following command: conda env create -f DEEPLABCUT.yaml .

## Download the Annotation Data
(1) The goal is to download the following folder onto the scratch folder of your ICE node: https://drive.google.com/drive/folders/1vH_g827bM39VrxGgzLm59u9qPR_9C0co (permission needed). However, the folder is very large, so an interactive desktop session can be used. Click "Interactive Apps" and then "Interactive Desktop," or click the following link: https://ondemand-ice.pace.gatech.edu/pun/sys/dashboard/batch_connect/sys/bc_desktop_rh9/session_contexts/new . Once inside the interactive desktop, open a browser and download the data folder from Google Drive.
(2) The interactive desktop might not have an unzip utility. Go back to Bash and use the command: unzip filename.zip . After unzipping the folders, you can delete the zips if desired. The folder structure should look like the following:
```.../dlc_model-student-2023-07-26
  ├── config.yaml
  ├── dlc-models
  ├── labeled-data
  ├── training-datasets
  └── videos
```

## Request a Compute Node with GPUs to Test `deeplabcut`
(1) End your current Jupyter Notebook session, and start a new one with "Node Type" as "NVIDIA GPU (first avail)." 
(2) Open your Bash file in the scratch folder and type the following command to use DLC: conda activate DEEPLABCUT .

## Call `deeplabcut.create_multianimaltraining_dataset`
(1) In your Bash file, run the following and copy the result: pwd .
(2) Go to the `config.yaml` from the downloaded data. 
(3) Update the project_path to the path you copied from Bash. Set the engine to pytorch. Review the rest of the YAML settings, which have also been set up for fish pose estimation (body parts, skeleton, etc.). See the example below:
```
  # Project path (change when moving around)
  project_path: /storage/ice1/7/1/tnguyen868/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26

  # Default DeepLabCut engine to use for shuffle creation (either pytorch or tensorflow)
  engine: pytorch
```
(4) Open a new notebook that is "Python [conda env:.conda-DEEPLABCUT]" .
(5) Run the following code. (Modify `config_path` to point to `config.yaml` that you have just downloaded.) If your notebook is in the same directory as dlc_model-student-2023-07-26, then it would look like the following:
```
  import deeplabcut

  config_path = "dlc_model-student-2023-07-26/config.yaml"

  deeplabcut.create_multianimaltraining_dataset(config_path)
```

## Call `deeplabcut.train_network`
(1) Run this code (be sure to modify `config_path`) to see if DLC gets to the first training step, then exit.
```
  import deeplabcut
  print(deeplabcut.__version__)
  config_path = "dlc_model-student-2023-07-26/config.yaml"

  # Execute the training function
  deeplabcut.train_network(config_path, shuffle=1, trainingsetindex=0,)
```
(2) If, with the `train_network()` function, DLC can get to the first training step, you should still monitor a few more training steps to ensure there are no memory errors.

## Modify Training Settings as Needed
(1) In dlc_model-student-2023-07-26/dlc-models-pytorch/iteration-0/dlc_modelJul26-trainset95shuffle1/train/pytorch_config.yaml, you can change the batch size to 16 or 32 so that its faster. You can also change the number of epochs, etc. to speed training. Note that this will change the performance of the model.

## Use SLURM to Train
(1) Create a file named dlc_training.sbatch in the same directory where your training script (test_training_script.py) is located.
In Jupyter Notebook, open new terminal.
'''
nano dlc_training.sbatch
'''
(2) Copy and paste the following content into dlc_training.sbatch:
'''
#!/bin/bash
#SBATCH -J DLC_model_training1
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --gres=gpu:H100:1            # Requesting 1 GPU (e.g., H100)
#SBATCH --cpus-per-task=4            # Requesting 4 CPUs
#SBATCH --mem=64GB                   # Requesting 64GB of memory
#SBATCH -t 0-10:00:00                # Requesting 10 hours
#SBATCH -o DLC_Training_Test1_Report-%j.out   # Output file
#SBATCH --mail-type=BEGIN,END,FAIL   # Notifications on job start/end/fail
#SBATCH --mail-user=your-email@example.com

cd $SLURM_SUBMIT_DIR                 # Change to working directory

source /home/hice1/tnguyen868/anaconda3/bin/activate /path/to/DLC/environment/folder
export PATH="/path/to/DLC/environment/folder/bin:$PATH"

srun python test_training_script.py   # Run your training script
'''
(3) Submit the Batch Job. In the terminal, navigate to the directory where the batch script (dlc_training.sbatch) and Python script (test_training_script.py) are located.
Submit the batch job using:
'''
sbatch dlc_training.sbatch
'''
(4) Monitor the job. SLURM will automatically handle the job scheduling, and the output will be written to a file (in this case, DLC_Training_Test1_Report-%j.out, where %j is the job ID).
You can check the job status with:
'''
squeue -u your-username
'''
You can cancel the job if needed with:
'''
scancel JOB_ID
'''
(5) Specifically, you can reconnect to the cluster later (open your interactive app again) and monitor the job using the following in Bash:
'''
squeue -u your-username         # To check if the job is still running
cat DLC_Training_Test1_Report-<job-id>.out  # To see the output logs
'''

## Running a SLURM Job
(1) In the terminal you ssh-ed into, type: conda activate DEEPLABCUT .
(2) Initiate the conda environment next: conda init .
(3) Use the following: nano dlc_training.sbatch . And copy this:
'''
#!/bin/bash
#SBATCH -J DLC_model_training
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --gres=gpu:H100:1            # Requesting 1 GPU (e.g., H100)
#SBATCH --cpus-per-task=4            # Requesting 4 CPUs
#SBATCH --mem=64GB                   # Requesting 64GB of memory
#SBATCH -t 0-10:00:00                # Requesting 10 hours
#SBATCH -o DLC_Training_Test1_Report-%j.out   # Output file
#SBATCH --mail-type=BEGIN,END,FAIL   # Notifications on job start/end/fail
#SBATCH --mail-user=kcozart6@gatech.edu # Replace with your email

cd $SLURM_SUBMIT_DIR                 # Change to working directory
#conda init bash
#source /usr/local/pace-apps/manual/packages/anaconda3/2023.03/etc/profile.d/conda.sh
#source /home/hice1/kcozart6/.conda/envs/DEEPLABCUT/
#export PATH="/home/hice1/kcozart6/.conda/envs/DEEPLABCUT/bin/:$PATH"
conda activate DEEPLABCUT
srun python /home/hice1/kcozart6/scratch/test_training_script.py   # Run your training script
'''
(4) Inside the scratch folder, use the following: nano test_training_script.py . And copy this:
'''
import deeplabcut

config_path = "/home/hice1/kcozart6/scratch/dlc_model-student-2023-07-26/config.yaml"
deeplabcut.create_multianimaltraining_dataset(config_path)
deeplabcut.train_network(config_path, shuffle=1, trainingsetindex=0,)
'''
(5) In the ssh terminal, use the following: sbatch dlc_training.sbatch . Error logs can be read in the top-level folder of your username.

## Training for an extended period
(1) Once you're convinced that the model can be trained properly, there are options for running the training to completion: using interactive VS Code or terminal session or a batch job.
(2) On an interactive session, you can use `tmux` to launch the training script above and have `tmux` keep track of the process such that you can temporarily close the interactive session or exit the VS Code browser window and later go back into the training process that `tmux` still manages. Create a new `tmux` session by running this command in the terminal:
```
  tmux new-session -t dlc-training
```
Then launch any script you want as in any terminal. `Ctrl + B`, then `D` to detach from `tmux` while the script is still running. Later, attach again to view the script by running in the terminal:
```
  tmux attach-session -t dlc-training
```
If using a batch job, here's an SBATCH request that you can use. Assuming `test_training_script.py` is the name of the Python script that contains `.train_network()` function call above. Create the file `dlc_training.sbatch` with this content:
```
  #!/bin/bash
  #SBATCH -JDLC_model_training1
  #SBATCH -N1 --ntasks-per-node=1
  #SBATCH --gres=gpu:H100:1
  #SBATCH --cpus-per-task=4
  #SBATCH --mem=64GB
  #SBATCH -t0-08:00:00     # Requesting 8 hours, which seems to be enough to run 90 epochs
  #SBATCH -oDLC_Training_Test1_Report-%j.out                
  #SBATCH --mail-type=BEGIN,END,FAIL

  cd $SLURM_SUBMIT_DIR                     # Change to working directory

  source /home/hice1/tnguyen868/anaconda3/bin/activate /path/to/DLC/environment/folder
  export PATH="/path/to/DLC/environment/folder/bin:$PATH"

  srun python test_training_script.py

```
Then request the batch job by changing to the same folder where `test_training_script.py` is located, and run:
```
  sbatch dlc_training.sbatch
```
Please refer to [PACE Documentation](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042503) for details on `.sbatch` syntax.

## Troubleshooting Notes
If the script could not get to a first training step and threw error, inspect this YAML file that controls some training settings: `.../dlc_model-student-2023-07-26/dlc-models-pytorch/iteration-0/dlc_modelJul26-trainset95shuffle1/train/pytorch_config.yaml`. The folder structure looks like this. It seems that DLC re-created the `dlc-models-pytorch` folder, since its latest version supports a PyTorch engine.
```.
  ├── config.yaml
  ├── dlc-models-pytorch
  ├── labeled-data
  ├── training-datasets
  └── videos
```

### Labeled Data Corrupted On DLC Dataset Build or Training
If the dataset build step runs into an error (or the next step), it might be because some of the folders in `labeled-data` are corrupted (according to Adam Thomas). In order to tell DLC to ignore these files, edit the `config.yaml` file and comment out these data files within the `video_sets` field:
```
# Annotation data set configuration (and individual video cropping parameters)
video_sets:
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc21_3_Tk53_021220_0004_vid
  # : crop: 0, 1296, 0, 972
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc21_6_Tk53_030320_0002_vid
  # : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc23_1_Tk33_021220_0004_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc23_8_Tk33_031720_0001_vid
  : crop: 0, 1296, 0, 972
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc24_4_Tk47_030320_0002_vid
  # : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc26_2_Tk63_022520_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc28_1_Tk3_022520_0004_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc29_3_Tk9_030320_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc32_5_Tk65_030920_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc34_3_Tk43_030320_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc35_11_Tk61_051220_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc36_2_Tk3_030320_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc37_2_Tk17_030320_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc40_2_Tk3_030920_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc41_2_Tk9_030920_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc43_11_Tk41_060220_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc44_7_Tk65_050720_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc45_7_Tk47_050720_0002_vid
  : crop: 0, 1296, 0, 972
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc46_2_Tk53_030920_0002_vid
  # : crop: 0, 1296, 0, 972
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc51_2_Tk53_031720_0001_vid
  # : crop: 0, 1296, 0, 972
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc54_5_Tk53_051220_0002_vid
  # : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc55_2_Tk47_051220_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc56_2_Tk65_051220_0002_vid
  : crop: 0, 1296, 0, 972
  # ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc58_4_Tk53_060220_0001_vid
  # : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc59_4_Tk61_060220_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc62_3_Tk65_060220_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc63_1_Tk9_060220_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc64_1_Tk51_060220_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc65_4_Tk9_072920_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc76_3_Tk47_072920_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc80_1_Tk41_072920_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc81_1_Tk51_072920_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc82_b2_Tk63_073020_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc86_b1_Tk47_073020_0002_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc90_b1_Tk3_081120_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc91_b1_Tk9_081120_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc94_b1_Tk31_081120_0001_vid
  : crop: 0, 1296, 0, 972
  ? /home/hice1/tnguyen868/scratch/dlc_dataset/dlc_test1/dlc_model-student-2023-07-26/labeled-data/MC_singlenuc96_b1_Tk41_081120_0001_vid
  : crop: 0, 1296, 0, 972
```
### Module Error for Tensorflow Appears on Training, but Pytorch is being Used
(1) From the project folder ` dlc_model-student-2023-07-26`, erase the dlc model pytorch folder or dlc-model folder and the training datasets folder. Keep labeled-data and config.yaml and videos.
(2) Remove the corrupted videos mentioned in the above troubleshooting step.
(3) Run the dataset creation code again: 
```
  import deeplabcut
  config_path = "dlc_model-student-2023-07-26/config.yaml"
  deeplabcut.create_multianimaltraining_dataset(config_path)
```
(4) Run the train dataset code again:
```
  import deeplabcut
  config_path = "dlc_model-student-2023-07-26/config.yaml"
  deeplabcut.train_network(config_path, shuffle=1, trainingsetindex=0,)
```
(5) If you are running into malformed dataset errors, ensure that you erase existing training shuffles from the training datasets folder, create the dataset, and then train the network in that order.

### CUDA OutOfMemory Error Occurs
If there is the CUDA OutOfMemory error, you need to request a compute node with larger GPU memory, or reduce the batch size by half.
```
  ...
  train_settings:
  batch_size: 16
  dataloader_workers: 0
  dataloader_pin_memory: false
  display_iters: 100
  epochs: 100
  seed: 42
```
The `eval_interval` setting under `Runner` controls how many epochs will the model attempts an evaluation after:
```
  runner:
  type: PoseTrainingRunner
  gpus:
  - 0
  key_metric: test.mAP
  key_metric_asc: true
  eval_interval: 10
  optimizer:
      type: AdamW
      params:
      lr: 0.0001
```
Initially it is set to 10. However, evaluating DLC too early seems to always lead the program to crash. My theory is that internally, DLC's neural network outputs one "heatmap" for each of the body parts (tail fin, etc.) that we have defined for the cichlid. The heatmap, which represents the video frame being processed, indicates the probability that a given point in that video frame could be the corresponding body part. In other words, the local "peaks" in a heatmap likely indicate where a body part (keypoint) should be. At the beginning, the model has not been trained very well, so the heatmaps look more or less random, and there will be too many possible keypoint locations, leading to a crash. One workaround is to postpone evaluation until after training, hoping that by that time, the model will have learned to produce good heatmaps with only few local maxima. For example, we could set the `eval_interval` to a larger number than the `epochs` settings to ensure that evaluation is never done while training.
```
  runner:
  type: PoseTrainingRunner
  gpus:
  - 0
  key_metric: test.mAP
  key_metric_asc: true
  eval_interval: 300
  optimizer:
      type: AdamW
      params:
      lr: 0.0001
```
The training code does not appear to automatically use all available GPUs. I raise a GitHub issue with DeepLabCut - please refer for further details, if you want to force `deeplabcut` to use all available GPUs: https://github.com/DeepLabCut/DeepLabCut/issues/2744. Otherwise, it defaults to using one GPU. Oddly enough, I found that multi-GPU training did not seem to result in a boost in training speed, so I trained with one GPU.
