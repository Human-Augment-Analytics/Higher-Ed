import os
import pandas as pd
import numpy as np

# Constants
PIXEL_TO_CM = 0.41  # cm per pixel
PADDING = 1  # seconds to add before and after the bout
REALISTIC_JUMP_THRESHOLD_CM = 100  # Maximum realistic jump height in cm

# Helper Functions
def calculate_max_vertical_jump_height(data, bout_data):
    start_frame = bout_data['Start_frame'].values[0]
    buffer_start_frame = max(0, start_frame - int(PADDING * 29))  # 29 FPS

    # Use y-coordinates of the same body part with a buffer before start time
    head_y_start = data.loc[buffer_start_frame, 'head_y']
    upperback_y_start = data.loc[buffer_start_frame, 'upperback_y']

    # Calculate max jump height during the bout
    head_y_max = data.loc[start_frame:, 'head_y'].max()
    upperback_y_max = data.loc[start_frame:, 'upperback_y'].max()

    head_jump_height = head_y_max - head_y_start
    upperback_jump_height = upperback_y_max - upperback_y_start

    # Convert to cm and apply realistic threshold
    max_jump_height_cm = max(head_jump_height, upperback_jump_height) * PIXEL_TO_CM
    if max_jump_height_cm < 0 or max_jump_height_cm > REALISTIC_JUMP_THRESHOLD_CM:
        return 0  # Set to 0 if the calculated jump height is negative or exceeds the threshold
    return max_jump_height_cm

def calculate_takeoff_angle(data, bout_data):
    start_frame = bout_data['Start_frame'].values[0]
    end_frame = bout_data['End_frame'].values[0]

    # Takeoff angle only within the jump bout
    bout_data = data[(data.index >= start_frame) & (data.index <= end_frame)]
    
    dx = bout_data['head_x'].diff().fillna(0)
    dy = bout_data['head_y'].diff().fillna(0)
    movement = np.sqrt(dx**2 + dy**2)
    significant_movement_index = movement.idxmax()  # Get the index of the first significant movement (within jump bout)
    
    angle = np.arctan2(dy[significant_movement_index], dx[significant_movement_index]) * 180 / np.pi
    return angle

def calculate_takeoff_velocity(bout_data, time_bins):
    bout_start_time = bout_data['Start_time'].values[0]
    relevant_bins = time_bins[(time_bins['TIME BIN #'] >= bout_start_time) & (time_bins['TIME BIN #'] < bout_start_time + 1.5)]  # first 2 bins after start (2s)
    relevant_bins = relevant_bins[relevant_bins['MEASUREMENT'] == 'Velocity (cm/s)']
    if relevant_bins.empty:
        return 0
    return relevant_bins['VALUE'].max()

def calculate_peak_velocity(time_bins, bout_data):
    bout_start_time = bout_data['Start_time'].values[0]
    bout_end_time = bout_data['End Time'].values[0]
    relevant_bins = time_bins[(time_bins['TIME BIN #'] >= bout_start_time - PADDING) & (time_bins['TIME BIN #'] <= bout_end_time + PADDING)]
    relevant_bins = relevant_bins[relevant_bins['MEASUREMENT'] == 'Velocity (cm/s)']
    if relevant_bins.empty:
        return 0
    return relevant_bins['VALUE'].max()

def calculate_peak_acceleration(time_bins, bout_data):
    bout_start_time = bout_data['Start_time'].values[0]
    bout_end_time = bout_data['End Time'].values[0]
    relevant_bins = time_bins[(time_bins['TIME BIN #'] >= bout_start_time - PADDING) & (time_bins['TIME BIN #'] <= bout_end_time + PADDING)]
    relevant_bins = relevant_bins[relevant_bins['MEASUREMENT'] == 'Velocity (cm/s)']
    if relevant_bins.empty:
        return 0
    velocities = relevant_bins['VALUE'].values
    accelerations = np.diff(velocities)  # Calculate acceleration
    accelerations = np.where(accelerations < 0, 0, accelerations)  # Set negative accelerations to 0
    if accelerations.size == 0:
        return 0
    return accelerations.max()

# Main Function to Process Each Video
def process_video(video_id, bout_data, feature_data, time_bins):
    results = {}
    
    # Filter data for this video
    video_bout_data = bout_data[bout_data['Video'] == video_id]
    video_feature_data = feature_data
    video_time_bins = time_bins[time_bins['VIDEO'] == video_id]

    # Calculate metrics
    results['Video'] = video_id
    results['Start_time'] = video_bout_data['Start_time'].values[0]
    results['End Time'] = video_bout_data['End Time'].values[0]
    results['Max Vertical Jump Height (cm)'] = calculate_max_vertical_jump_height(video_feature_data, video_bout_data)
    results['Take-off Angle (degrees)'] = calculate_takeoff_angle(video_feature_data, video_bout_data)
    results['Take-off Velocity (cm/s)'] = calculate_takeoff_velocity(video_bout_data, video_time_bins)
    results['Peak Velocity (cm/s)'] = calculate_peak_velocity(video_time_bins, video_bout_data)
    results['Peak Acceleration (cm/s^2)'] = calculate_peak_acceleration(video_time_bins, video_bout_data)
    
    return results

# Load Data
bout_data = pd.read_csv('detailed_bout_data_summary_20240807182021.csv')
time_bins = pd.read_csv('Time_bins_0.75s_movement_results_20240807182124.csv')

# Process Each Video
video_ids = bout_data['Video'].unique()
all_results = []

for video_id in video_ids:
    feature_file = os.path.join('features_extracted', f'{video_id}.csv')
    if not os.path.exists(feature_file):
        continue
    
    feature_data = pd.read_csv(feature_file)
    result = process_video(video_id, bout_data, feature_data, time_bins)
    all_results.append(result)

# Save Results to CSV
results_df = pd.DataFrame(all_results)
results_df = results_df[['Video', 'Start_time', 'End Time', 'Max Vertical Jump Height (cm)', 'Take-off Angle (degrees)', 'Take-off Velocity (cm/s)', 'Peak Velocity (cm/s)', 'Peak Acceleration (cm/s^2)']]
results_df.to_csv('jump_metrics_summary.csv', index=False)

print("Processing complete. Results saved to 'jump_metrics_summary.csv'.")
