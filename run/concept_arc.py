import yaml
from pathlib import Path
from datetime import datetime

from geometor.seer import Seer, Tasks
from geometor.seer.tasks.tasks import get_unsolved_tasks


def run():
    #  config_file = "thinker.yaml"
    config_file = "config-25.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    seer = Seer(config)

    output_dir = Path("../sessions_ConceptARC/")

    #  tasks = Tasks("../tasks/ConceptARC_minimal")
    tasks = get_unsolved_tasks(output_dir)
    tasks = tasks.get_ordered_tasks()

    seer.run(tasks, output_dir, "unsolved")

    #  parent_path = Path("../tasks/ConceptARC")
    #  for set_dir in parent_path.iterdir():
        #  if set_dir.is_dir():
            #  print("SET:", set_dir.name)

            #  tasks = Tasks(set_dir)
            #  tasks = tasks.get_ordered_tasks()
            #  seer.run(tasks, output_dir, set_dir.name)


if __name__ == "__main__":
    run()
