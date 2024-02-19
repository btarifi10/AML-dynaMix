from video_reproduction import instantiate_reproduction_app
from experiment_logging import ExperimentLogger
from utils import load_experiment_config, get_parsed_args, override_config

import os
import random

def run_experiment():

    config_path, subject_id, optional_args = get_parsed_args()

    config = load_experiment_config(config_path)

    config = override_config(config, optional_args)

    logger = ExperimentLogger(subject_id=subject_id)

    video_files = os.listdir(config['video_path'])
    selected_video_files = random.sample(video_files, config['n_videos'])

    app = instantiate_reproduction_app(selected_video_files, config, logger)
    app.run_video_loop()

    logger.save_record(config['logs_output_path'], app.session_start_time)


if __name__ == '__main__':
    run_experiment()




