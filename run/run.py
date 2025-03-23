import yaml
from pathlib import Path
from datetime import datetime

from geometor.seer import Seer, Tasks


def run():
    #  config_file = "thinker.yaml"
    config_file = "config.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    #  tasks = Tasks("../../_arc-dataset-collection/dataset/Mini-ARC/data")
    #  tasks = Tasks("../../_ConceptARC/corpus/Copy")
    #  tasks = tasks.get_ordered_tasks()
    tasks = Tasks("tasks/ARC/training").get_ordered_tasks()
    #  tasks = Tasks("tasks/ARC/training").get_ordered_by_train_count()
    #  tasks = list(reversed(tasks))

    seer = Seer(config)

    seer.run(tasks[0:50])
    #  seer.run(tasks)


if __name__ == "__main__":
    run()
