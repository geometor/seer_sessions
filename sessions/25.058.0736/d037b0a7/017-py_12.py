import numpy as np

def get_metrics(task):
    metrics = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        input_shape = input_grid.shape
        output_shape = output_grid.shape
        top_left_color = input_grid[0, 0]
        output_color = output_grid[0, 0] # Assuming the output is uniform

        example_metrics = {
            'input_shape': input_shape,
            'output_shape': output_shape,
            'top_left_color': int(top_left_color),  # Convert to regular integer
            'output_color': int(output_color),
            'output_uniform': np.all(output_grid == output_color)
        }
        metrics.append(example_metrics)
    return metrics

# Assuming 'task' variable holds the current task data (replace with actual loading)
# For demonstration, let's create a dummy task:
task = {
  "train": [
    {"input": [[1, 2], [3, 4]], "output": [[1, 1], [1, 1]]},
    {"input": [[5, 6], [7, 8]], "output": [[5, 5], [5, 5]]},
    {"input": [[9, 0, 1], [2, 3, 4], [5,6,7]], "output": [[9, 9, 9], [9, 9, 9],[9,9,9]]}
  ]
}

metrics = get_metrics(task)
print(metrics)