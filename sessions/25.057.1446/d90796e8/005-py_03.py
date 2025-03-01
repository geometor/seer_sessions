def get_input_output_from_example(task, example_type, example_index):
    """
    Retrieves input and output grids from a specific example in a task.
    """
    return task[example_type][example_index]['input'], task[example_type][example_index]['output']

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a dictionary detailing any differences.
    """
    if grid1.shape != grid2.shape:
        return {'different': True, 'reason': 'Shapes are different', 'shape1':grid1.shape, 'shape2': grid2.shape}

    differences = []
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                differences.append(((i, j), grid1[i, j], grid2[i, j]))

    return {'different': len(differences) > 0, 'differences': differences, 'shape1':grid1.shape, 'shape2': grid2.shape}

def show_grid(grid, title = ""):
  print(title)
  print(grid)
  print()

#load first task
from glob import glob
import json
import numpy as np

# Load all tasks
all_task_files = glob('data/training/*.json')
all_tasks = []

for task_file in all_task_files:
    with open(task_file, 'r') as f:
        task = json.load(f)
        all_tasks.append(task)

#we will cycle through all tasks during dev
task = all_tasks[0]

task_file_name = all_task_files[0]
task_id = task_file_name[14:-5]
print(f"Task ID: {task_id}")

#task contains a list of training and test examples
#each of these has an input and output
train_input, train_output = get_input_output_from_example(task, 'train', 0)
test_input, test_output = get_input_output_from_example(task, 'test', 0)
train_input_grid = np.array(train_input)
train_output_grid = np.array(train_output)
test_input_grid = np.array(test_input)
test_output_grid = np.array(test_output)

show_grid(train_input_grid, "train input 0")
show_grid(train_output_grid, "train output 0")

#transform the input
transformed_grid = transform(train_input_grid)
show_grid(transformed_grid, "transformed")
show_grid(train_output_grid, "expected")

#compare with output
diff = compare_grids(transformed_grid, train_output_grid)
print(f"any differences: {diff['different']}")
if (diff['different']):
  print(f"  details: {diff['differences']}")

#try the others
for i in range(1,len(task['train'])):
  train_input, train_output = get_input_output_from_example(task, 'train', i)
  train_input_grid = np.array(train_input)
  train_output_grid = np.array(train_output)
  transformed_grid = transform(train_input_grid)
  diff = compare_grids(transformed_grid, train_output_grid)
  print(f"\nexample {i}")
  show_grid(train_input_grid, "train input")
  show_grid(train_output_grid, "train output")
  print(f"any differences: {diff['different']}")
  if (diff['different']):
    print(f"  details: {diff['differences']}")
