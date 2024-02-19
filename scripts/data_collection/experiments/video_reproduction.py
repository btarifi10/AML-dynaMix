import vlc
import tkinter as tk

from tkinter import ttk
import time

class FullscreenVideoPlayer:
    def __init__(self, root, video_files, config, logger):
        self.root = root
        self.video_files = video_files

        self.config = config 
        self.logger = logger

        # Initialize VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Set up the GUI
        self.root.title("Video Player")
        self.root.geometry(f"{config['video_width']}x{config['video_height']}")  # Initial window size, before going fullscreen
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.close_button = ttk.Button(self.frame, text="Close", command=self._close_player)
        self.close_button.pack(side=tk.BOTTOM, pady=5)

        self.self_assessment_video_path = self.config['self_assessment_path']
        self.break_video_path = self.config['relaxation_point_path']

        self.session_start_time = time.time()

    def _close_player(self):
        self.player.stop()
        self.root.quit()

        self.session_end_time = time.time()

    def _play_single_video(self, video_path, duration):
        single_video_start_time = time.time()

        media = self.instance.media_new(video_path)
        media.get_mrl()
        self.player.set_media(media)
        self.player.set_fullscreen(True)  # Set the player to fullscreen
        self.player.play()

        time.sleep(duration)  # Wait for 10 seconds before playing the next video

        single_video_end_time = time.time()
        single_video_duration = single_video_end_time - single_video_start_time

        return single_video_start_time, single_video_end_time, single_video_duration

    def run_video_loop(self):
        video_loop_start_time = time.time()
        
        baseline_start_time, baseline_end_time, baseline_duration = self._play_single_video(self.break_video_path, duration=self.config['baseline_time_seconds'])

        for video_name in self.video_files:
            video_index = self.video_files.index(video_name)
            video_path = self.video_files[video_index]

            single_video_start_time, single_video_end_time, single_video_duration = self._play_single_video(video_path, duration=self.config['main_video_seconds'])

            self_assessment_start_time, self_assessment_end_time, self_assessment_duration = self._play_single_video(self.self_assessment_video_path, duration=self.config['self_assessment_seconds'])

            break_start_time, break_end_time, break_duration = self._play_single_video(self.break_video_path, duration=self.config['break_time_seconds'])

            time_recordings_update_args = [video_index, video_name, 
                           baseline_duration, baseline_start_time, baseline_end_time,
                           single_video_duration, single_video_start_time, single_video_end_time,
                           self_assessment_duration, self_assessment_start_time, self_assessment_end_time,
                           break_duration, break_start_time, break_end_time]
            
            self.logger.update_time_recordings(time_recordings_update_args)

        video_loop_end_time = time.time()
        video_loop_duration = video_loop_end_time - video_loop_start_time
        self._close_player()

        self.session_duration = self.session_end_time - self.session_start_time

        subject_metadata_update_args = [video_loop_duration, video_loop_start_time, video_loop_end_time,
                                        self.session_duration, self.session_start_time, self.session_end_time]
        self.logger.update_subject_metadata(subject_metadata_update_args)

        
def instantiate_reproduction_app(video_files, config, logger):
    root = tk.Tk()
    app = FullscreenVideoPlayer(root, video_files, config, logger)
    
    return app





''' 
# Example usage

video_files = os.listdir('DEAP Videos') # Substitute with directory containing .mp4 DEAP videos

root = tk.Tk()

app = FullscreenVideoPlayer(root, video_files)
root.mainloop()
'''
