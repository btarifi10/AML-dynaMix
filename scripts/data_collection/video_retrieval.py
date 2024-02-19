import pandas as pd
import numpy as np
import os

from pytube import YouTube
from pytube.exceptions import VideoUnavailable

def download_video(url, output_path=None, save_as=None):
    try:
        YouTube(url).streams.first().download(filename=save_as,
                                            output_path=output_path, 
                                            skip_existing=True, 
                                            timeout=5, 
                                            max_retries=2)
        print("Video Downloaded.\n")
    except VideoUnavailable:
        print("Video Unavailable.\n")                                         

def download_videos(df, tag=None, discard_none=False, output_path='experiments/DEAP Videos', save_index=True):
    if tag:
        print(f"Selecting only '{tag}' videos")
        df = df[df['Lastfm_tag'] == tag]

    elif discard_none:
        print(f"Selecting only tagged videos")
        df = df[~pd.isna(df['Lastfm_tag'])]
    
    print("Downloading batch of videos.")

    if not os.path.exists(output_path):
        print("Output folder does not exist. Creating folder...")
        os.makedirs(output_path)
        print("Folder created.")

    count = 0
    for _, video in df.iterrows():
        video_id = video['Online_id']
        if save_index:
            save_as = f"{video_id}.mp4"
        else:
            save_as = None
        
        print(f"Downloading video number {video_id}; Title: {video['Title']}...")
        download_video(video['Youtube_link'], output_path=output_path, save_as=save_as)
        count += 1
    
    print(f"Download completed! {count} videos processed!")

