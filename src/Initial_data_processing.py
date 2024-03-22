import json
import os
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import os
import numpy as np
import neurokit2 as nk


# Function to convert data to a DataFrame
def convert_to_dataframe(user_data):
    # Extract user details
    details = user_data["user_details"]
    name = details['name']
    # Create DataFrame for timestamp and feature signals
    df = pd.DataFrame({
        "timestamp": user_data["timestamp"],
        "ECG": user_data["ecg"],
        "GSR": user_data["gsr"],
        "PPG_red": user_data["ppg_red"],
        "PPG_ir": user_data["ppg_ir"],
        "PPG_green": user_data["ppg_green"]
    })
    
    df.attrs = details
    
    return name, df


def partition_dataset(df, videoDuration):
    partitions = {}
    for i, video_index in enumerate(videoDuration["video_index"]):
        video_name = videoDuration["video_name"][i]
        partitions[video_name] = {}
        
        # Iterate over each segment (baseline, single_video, self_assessment, "break")
        for segment in ["baseline", "single_video", "self_assessment", "break"]:
            start_time_col = f"{segment}_start_time"
            end_time_col = f"{segment}_end_time"
            
            name = df.attrs['name']
            # Filter the DataFrame for the current segment and video
            segment_df = df[(df['timestamp'] >= videoDuration[start_time_col][i]) & 
                            (df['timestamp'] <= videoDuration[end_time_col][i])]
            
            # Store additional information about the video as DataFrame attributes
            segment_df.attrs['video_index'] = video_index
            segment_df.attrs['video_name'] = video_name
            
            # Store the filtered DataFrame in the partitions dictionary
            partitions[video_name][segment] = segment_df
    
    return partitions, name


def plot_segments_features_by_video_index(partitions, segments, features, filename, video_index = 1):

    video_names = list(partitions.keys())
    
    if video_index - 1 >= len(video_names) or video_index - 1 < 0:
        print(f"Video index {video_index} is out of range.")
        return
    video_name = video_names[video_index - 1]
    
    # Setup for subplots based on the number of segments and features
    nrows = len(segments)
    ncols = len(features)
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5 * ncols, 4 * nrows), constrained_layout=True)
    fig.suptitle(f"{filename}_{video_name}", fontsize=16)
    
    # Ensure axs is always a 2D array for consistent indexing
    if nrows == 1 and ncols == 1:
        axs = [[axs]]  # Encapsulate it in a list to make it 2D
    elif nrows == 1:
        axs = [axs]  # Make the 1D array of axs into a 2D array with one row
    elif ncols == 1:
        axs = [[ax] for ax in axs]  # Make the 1D array of axs into a 2D array with one column

    # Iterate over each segment and feature to create subplots
    for i, segment in enumerate(segments):
        for j, feature in enumerate(features):
            ax = axs[i][j]  # Correct indexing for any configuration of axs
            segment_df = partitions[video_name][segment]

            # Plot the feature if data is available
            if not segment_df.empty and feature in segment_df.columns:
                ax.plot(segment_df['timestamp'], segment_df[feature], label=feature)
                ax.set_title(f"{segment} - {feature}")
                ax.set_xlabel('Timestamp')
                ax.legend()
            else:
                ax.set_title(f"{segment} - {feature}")
                ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            
            if j == 0:  # Add y-label to the first column for cleanliness
                ax.set_ylabel(feature)

    plt.savefig(f"{filename}_{video_name}.png")

FileNames = ["Alysonn_2024-03-07_17-58-45",
             "Jared_2024-03-07_18-54-03",
             "Thomas_2024-03-07_19-47-05",
             "Lia Llorca_2024-03-05_19-04-49",
             "William Powell_2024-03-04_18-23-11",
             "Aaron Fainman_2024-03-12_15-20-57",
             "gabriella_2024-03-12_18-24-59",
             "Genaro_2024-03-12_16-06-10",
             "Joe_2024-03-12_17-36-10",
             "Kostas_2024-03-12_16-54-27",
             "shaushan_2024-03-12_19-32-25"
             ]

# Dictionary to hold DataFrames for each file
dataframes = {}

# Base path assumes files are one directory up from the current script's directory
base_path = os.path.join(os.path.dirname(__file__), '..')

# Loop through each file in FileNames
for file_name in FileNames:
    json_file_path = os.path.join(base_path, f"{file_name}.json")  # Construct file path
    normalized_path = os.path.normpath(json_file_path)  # Normalize the path

    try:
        with open(normalized_path, 'r') as file:
            data = json.load(file)
        print(f"JSON data successfully loaded from {file_name}.")
        
        # Convert dictionary to pandas DataFrame
        name, df = convert_to_dataframe(data)
        
        # Store the DataFrame in the dictionary
        dataframes[name] = df

    except Exception as e:
        print(f"Failed to load JSON data from {file_name}: {e}")


videoDuration = {
    "video_index": [1, 2, 3],
    "video_name": ["Video 1", "Video 2", "Video 3"],  # Assuming each video has a unique name
    "baseline_duration": [200, 400, 600],
    "baseline_start_time": [0, 600, 1200],
    "baseline_end_time": [200, 1000, 1800],
    "single_video_duration": [100, 10000, 700],
    "single_video_start_time": [10000, 20000, 1800],
    "single_video_end_time": [20000, 1500, 2500],
    "self_assessment_duration": [100, 200, 300],
    "self_assessment_start_time": [500, 1500, 2500],
    "self_assessment_end_time": [600, 1700, 2800],
    "break_duration": [50, 100, 150],
    "break_start_time": [600, 1700, 2800],
    "break_end_time": [650, 1800, 2950],
}

# segments = ['baseline', 'single_video', 'self_assessment', 'break']
# features = ['ECG', 'GSR', 'PPG_red', 'PPG_ir', 'PPG_green']

# segments = ['single_video', 'self_assessment', 'break']
# features = ['ECG', 'PPG_red', 'PPG_ir', 'PPG_green']
print(dataframes)
# df_signals = dataframes['shaushan']
# df_signals1 = dataframes['shaushan']


# partitions_Arm, name_ARM = partition_dataset(df_signals, videoDuration)
# partitions_Chest, name_CHEST = partition_dataset(df_signals1, videoDuration)


# segments = ['single_video']
# features = ['ECG']
# # Assuming partitions is your dictionary of DataFrames created earlier
# # plot_segments_features_by_video_index(partitions_Arm, segments, features, name_ARM, video_index = 1)


# # plot_segments_features_by_video_index(partitions_Chest, segments, features, name_CHEST, video_index = 1)



# raw_GSR = partitions_Arm['Video 1']['single_video']['GSR']
# timestamps = partitions_Arm['Video 1']['single_video']['timestamp']



