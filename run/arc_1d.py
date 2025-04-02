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

    output_dir = Path("../sessions_1D/")

    #  tasks = Tasks("../tasks/ConceptARC_minimal")
    #  #  tasks = get_unsolved_tasks(Path("../sessions"))
    #  tasks = tasks.get_ordered_tasks()

    #  seer.run(tasks, output_dir, "minimal")

    parent_path = Path("../tasks/1D")
    for set_dir in parent_path.iterdir():
        if set_dir.is_dir():
            print("SET:", set_dir.name)

            tasks = Tasks(set_dir)
            tasks = tasks.get_ordered_tasks()
            seer.run(tasks, output_dir, set_dir.name)





if __name__ == "__main__":
    run()
