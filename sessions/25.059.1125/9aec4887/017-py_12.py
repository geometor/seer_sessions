# Example Usage (replace with actual grids from the task)
task_id = "6f8cd79b"
from pathlib import Path
import json
import numpy as np

def load_task(task_id, task_type="train"):
    """Loads a task from the ARC dataset."""
    task_file = Path("arc") / f"{task_type}" / f"{task_id}.json"
    with open(task_file, "r") as f:
        task = json.load(f)
    return task

task = load_task(task_id)

results = []
for i, example in enumerate(task["train"]):
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  predicted_output = transform(input_grid)
  metrics = analyze_example(input_grid, output_grid, predicted_output)
  results.append({
        "example_index": i,
        "metrics": metrics
  })
    
print (results)
