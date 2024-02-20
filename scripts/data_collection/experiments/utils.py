import json
import argparse

def load_experiment_config(config_path):
    with open(config_path, 'r') as config_json:
        config_dict = json.load(config_json)

    return config_dict

def get_parsed_args():
    parser = argparse.ArgumentParser(description="Provide config_path and subject_id arguments. Optional arguments allow to override configuration specifics.")

    parser.add_argument('config_path', type=str, help="Path to the configuration file")
    parser.add_argument('subject_id', type=int, help="ID associated to the experiment subject")

    parser.add_argument('--baseline_time_seconds', type=int, default=None, required=False, help="Amount of seconds for which the relaxation point is showed at the beginning of the experiment")
    parser.add_argument('--main_video_seconds', type=str, default=None, required=False, help="Amount of seconds for which each main video is showed")
    parser.add_argument('--self_assessment_seconds', type=str, default=None, required=False, help="Amount of seconds for which the self-assessment video is showed after the main video")
    parser.add_argument('--break_time_seconds', type=str, default=None, required=False, help="Amount of seconds for which the relaxation point is showed after the self-assessment")
    parser.add_argument('--video_width', type=str, default=None, required=False, help="Width pixels of the reproduced videos")
    parser.add_argument('--video_height', type=str, default=None, required=False, help="Height pixels of the reproduced videos")

    args = parser.parse_args()

    # Access arguments
    config_path = args.config_path
    subject_id = args.subject_id

    optional_args = {
        'baseline_time_seconds': args.baseline_time_seconds,
        'main_video_seconds': args.main_video_seconds,
        'self_assessment_seconds': args.self_assessment_seconds,
        'break_time_seconds': args.break_time_seconds,
        'video_width': args.video_width,
        'video_height': args.video_height,
                     }
    
    return config_path, subject_id, optional_args

def override_config(config, optional_args):
    for arg in optional_args:
        if optional_args[arg] is not None:
            config[arg] = optional_args[arg]

    return config    