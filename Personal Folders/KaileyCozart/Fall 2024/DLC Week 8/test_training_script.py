import deeplabcut
import os
import yaml

# Set the path to the configuration file
config_path = "/home/hice1/kcozart6/scratch/dlc_model-student-2023-07-26/config.yaml"
config_path_2 = "/home/hice1/kcozart6/scratch/dlc_model-student-2023-07-26/"

# Define a custom output directory to store evaluation results
output_dir = "/home/hice1/kcozart6/scratch/dlc_model-student-2023-07-26/results"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 1: Create the training dataset
deeplabcut.create_multianimaltraining_dataset(config_path)

# Function to modify the pose_cfg.yaml file before training
pose_cfg_path_global = "/home/hice1/kcozart6/scratch/dlc_model-student-2023-07-26/dlc-models-pytorch/iteration-0/dlc_modelJul26-trainset95shuffle1/train/pose_cfg.yaml"
def modify_pose_cfg(config_path, changes):
    # Locate the pose_cfg.yaml file in your DLC model directory
    # Replace 'iteration-XXXXX' and 'model_name' with actual names
    pose_cfg_path = os.path.join(os.path.dirname(config_path_2), 'dlc-models-pytorch', 'iteration-0', 'dlc_modelJul26-trainset95shuffle1', 'train', 'pose_cfg.yaml')
    
    # Load the YAML configuration
    with open(pose_cfg_path, 'r') as file:
        cfg = yaml.safe_load(file)
    
    # Apply the changes provided in the `changes` dictionary
    for key, value in changes.items():
        cfg[key] = value
    
    # Write the updated configuration back to the file
    with open(pose_cfg_path, 'w') as file:
        yaml.safe_dump(cfg, file)
        
    pose_cfg_path_global = pose_cfg_path

# Modify pose_cfg.yaml to set eval_interval to 300 and batch_size to 16
modify_pose_cfg(config_path, {'eval_interval': 300, 'batch_size': 16, 'epochs': 180, 'save_iters': 15000, 'maxiters': 20000})

# Verify that the changes were saved
with open(pose_cfg_path_global, 'r') as file:
    updated_cfg = yaml.safe_load(file)

# Print updated configuration
print("Updated Configuration:")
print(yaml.dump(updated_cfg, default_flow_style=False))

# Step 2: Train the network with custom parameters
deeplabcut.train_network(
    config_path, 
    shuffle=1, 
    trainingsetindex=0, 
    maxiters=50000, 
    saveiters=15000
)

# Step 3: Create the test dataset for evaluation (trainIndices=False creates test data)
deeplabcut.create_multianimaltraining_dataset(config_path, trainIndices=None)

# Step 4: Evaluate the trained network and save evaluation metrics
evaluation_file = os.path.join(output_dir, 'evaluation_results.csv')
deeplabcut.evaluate_network(
    config_path, 
    plotting=True,  # This will create and save evaluation plots
    shuffle=1, 
    trainingsetindex=0, 
    destfolder=output_dir  # Save the evaluation results and plots to the specified directory
)

# Step 5: Visualize the predicted keypoints on the original video and save the video
video_path = "/path/to/video.mp4"  # Update this to the path of your video file
labeled_video_dir = os.path.join(output_dir, 'labeled_videos')
if not os.path.exists(labeled_video_dir):
    os.makedirs(labeled_video_dir)

# Generate labeled video with predictions
deeplabcut.create_labeled_video(
    config_path, 
    [video_path], 
    shuffle=1, 
    trainingsetindex=0, 
    save_as_csv=True,  # Save predictions as CSV along with video
    destfolder=labeled_video_dir  # Save the labeled video to this directory
)

# Step 6: Extract predicted points to a CSV file and save them
analyzed_data_dir = os.path.join(output_dir, 'analyzed_data')
if not os.path.exists(analyzed_data_dir):
    os.makedirs(analyzed_data_dir)

deeplabcut.analyze_videos(
    config_path, 
    [video_path], 
    shuffle=1, 
    trainingsetindex=0, 
    save_as_csv=True,  # Save the predicted keypoints as CSV
    destfolder=analyzed_data_dir  # Save the analyzed keypoints to this directory
)

# Step 7: Generate and save labeled frames for further inspection
labeled_frames_dir = os.path.join(output_dir, 'labeled_frames')
if not os.path.exists(labeled_frames_dir):
    os.makedirs(labeled_frames_dir)

deeplabcut.create_labeled_video(
    config_path, 
    [video_path], 
    shuffle=1, 
    trainingsetindex=0, 
    draw_skeleton=True, 
    save_frames=True,  # Save each frame with keypoints as images
    destfolder=labeled_frames_dir  # Save labeled frames to this directory
)
