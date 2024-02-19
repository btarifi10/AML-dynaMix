# Data Collection

## Video Retrieval

video_retrieval.py allows to download the available youtube files given the URLs included in an input dataframe (from DEAP dataset "video_list.csv"). 
Discrimination depending on tag type and tag availability can be performed, thus downloading only a subset of the potentially available videos.

## Run Experiment

experiments/run_experiment.py allows to run multiple videos (appearing in the 'experiments/DEAP Videos' directory) according to the experiment video sequence setup; 
experiments/config.json contains experiment specifics, such as duration of each video component; it can be modified to change the experiment structure.
All the keys appearing in the config dictionary can be overridden by specifying their (optional) argument counterparts when running the file from command prompt;
Below an example of shell call to execute an experiment iteration:

```shell
python experiments\run_experiment.py config.json 0
```
