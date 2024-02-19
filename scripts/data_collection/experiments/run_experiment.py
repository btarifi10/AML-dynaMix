from video_reproduction import instantiate_reproduction_app
from experiment_logging import ExperimentLogger
from utils import load_experiment_config, get_parsed_args, override_config

import os

def run_experiment():

    config_path, subject_id, optional_args = get_parsed_args()

    config = load_experiment_config(config_path)

    config = override_config(config, optional_args)

    logger = ExperimentLogger(subject_id=subject_id)

    video_files = os.listdir(config['video_path'])
    video_files = ['DEAP Videos/3.mp4',
                   'DEAP Videos/5.mp4']

    app = instantiate_reproduction_app(video_files, config, logger)
    app.run_video_loop()

    logger.save_record(config['logs_output_path'], app.session_start_time)


if __name__ == '__main__':
    run_experiment()




