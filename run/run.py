import yaml
from pathlib import Path
from datetime import datetime

from geometor.seer import Seer, Tasks


def run():
    #  config_file = "thinker.yaml"
    config_file = "config.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    #  tasks = Tasks("one")
    #  tasks = Tasks("tasks/first-six")
    #  tasks = Tasks("44").get_ordered_tasks()
    tasks = Tasks("tasks/ARC/training").get_ordered_tasks()
    #  tasks = Tasks("tasks/ARC/training").get_ordered_by_train_count()
    #  tasks = Tasks("tasks/ARC/training")
    #  tasks = list(reversed(tasks))
    #  tasks = Tasks("other-six")

    seer = Seer(
        config,
    )

    seer.run(tasks[0:1]) 


if __name__ == "__main__":
    run()
