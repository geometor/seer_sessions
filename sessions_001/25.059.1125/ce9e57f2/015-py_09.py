import numpy as np

def get_task_metrics(task, transform_function):
    """
    Calculates and prints metrics for each example in the task.

    Args:
      task: The task dictionary containing 'train' examples.
      transform_function: The function that transforms the input grid.
    """

    for example_index, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        actual_output_grid = transform_function(input_grid)
        difference_grid = expected_output_grid - actual_output_grid

        print(f"Example {example_index}:")
        print(f"Input shape: {input_grid.shape}")
        print(f"Expected shape: {expected_output_grid.shape}")
        print(f"Actual shape: {actual_output_grid.shape}")
        print("Difference:")
        print(difference_grid)
        print("-" * 20)

# Example Usage (assuming 'task' and 'transform' are defined)
#from task_solution import transform  # Import your transform function
#get_task_metrics(task, transform)

# sample task
task = {}
task['train'] = [
    {'input': [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 2, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 0]],
     'output': [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 8, 0, 0, 0], [0, 8, 0, 0, 0], [0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0], [0, 0, 0], [0, 2, 0]],
     'output': [[0, 0, 0], [0, 0, 0], [0, 8, 0]]},
     {'input': [[0,0,0],[2,0,0],[0,0,0],[2,0,0],[0,0,0]],
      'output': [[0,0,0],[2,0,0],[0,0,0],[8,0,0],[0,0,0]]}
]
get_task_metrics(task, transform)