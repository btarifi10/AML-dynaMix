import json

class ExperimentLogger:
    def __init__(self, subject_id):

        self.subject_id = subject_id

        self.instantiate_subject_metadata()

        self.instantiate_time_recordings()


    def instantiate_subject_metadata(self):
        self.subject_metadata = {
            'subject_id': self.subject_id, #int
            'video_loop_duration': None,
            'video_loop_start_time': None,
            'video_loop_end_time': None,
            'session_duration': None,
            'session_start_time': None,
            'session_end_time': None,
            'time_recordings': None, #dict
        }
        print(f"Instantiating recording for subject n. {self.subject_id}.")

    def instantiate_time_recordings(self):
        self.time_recordings = {
            'video_index': [],
            'video_name': [],
            'baseline_duration': [],
            'baseline_start_time': [],
            'baseline_end_time': [],
            'video_duration': [],
            'video_start_time': [],
            'video_end_time': [],
            'self_assessment_duration': [],
            'self_assessment_start_time': [],
            'self_assessment_end_time': [],
            'break_duration': [],
            'break_start_time': [],
            'break_end_time': [],
        }

    def update_time_recordings(self, update_args):
        self.time_recordings['video_index'].append(update_args[0])
        self.time_recordings['video_name'].append(update_args[1])
        self.time_recordings['baseline_duration'].append(update_args[2])
        self.time_recordings['baseline_start_time'].append(update_args[3])
        self.time_recordings['baseline_end_time'].append(update_args[4])
        self.time_recordings['video_duration'].append(update_args[5])
        self.time_recordings['video_start_time'].append(update_args[6])
        self.time_recordings['video_end_time'].append(update_args[7])
        self.time_recordings['self_assessment_duration'].append(update_args[8])
        self.time_recordings['self_assessment_start_time'].append(update_args[9])
        self.time_recordings['self_assessment_end_time'].append(update_args[10])
        self.time_recordings['break_duration'].append(update_args[11])
        self.time_recordings['break_start_time'].append(update_args[12])
        self.time_recordings['break_end_time'].append(update_args[13])

    def update_subject_metadata(self, update_args):
        self.subject_metadata['video_loop_duration'] = update_args[0],
        self.subject_metadata['video_loop_start_time'] = update_args[1],
        self.subject_metadata['video_loop_end_time'] = update_args[2],
        self.subject_metadata['session_duration'] = update_args[3],
        self.subject_metadata['session_start_time'] = update_args[4],
        self.subject_metadata['session_end_time'] = update_args[5],
        self.subject_metadata['time_recordings'] = self.time_recordings, #dict
                              
    def save_record(self, logs_output_path, session_start_time):  
        output_path = f"{logs_output_path}/subject-{self.subject_id}_starttime-{session_start_time}.json"

        with open(output_path, 'w') as fp:
            json.dump(self.subject_metadata, fp)
        print(f"Data saved in {output_path}.")
    
