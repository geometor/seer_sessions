import numpy as np

def analyze_grid(grid):
    """Analyzes a single grid and returns relevant metrics."""
    grid_array = np.array(grid)
    non_zero_indices = np.nonzero(grid_array)
    non_zero_values = grid_array[non_zero_indices]
    num_non_zero = len(non_zero_values)
    unique_non_zero_values = np.unique(non_zero_values)
    return {
        'shape': grid_array.shape,
        'num_non_zero': num_non_zero,
        'unique_non_zero_values': unique_non_zero_values.tolist(),
        'min_non_zero': int(np.min(non_zero_values)) if num_non_zero > 0 else None,  # Ensure int for YAML
        'max_non_zero': int(np.max(non_zero_values)) if num_non_zero > 0 else None, # Ensure int for YAML
    }

def analyze_task(task):
  report = {}
  for i, example in enumerate(task['train']):
    input_analysis = analyze_grid(example['input'])
    output_analysis = analyze_grid(example['output'])
    report.update({
        f'example_{i + 1}': {
          'input' : input_analysis,
          'output' : output_analysis,
          }
        })
  return report

# Example task (replace with actual task data)
task = {
    "train": [
        {"input": [[0, 0, 0], [0, 1, 0], [0, 0, 0]], "output": [[1]]},
        {"input": [[0, 0, 0], [0, 0, 0], [0, 2, 0]], "output": [[2]]},
        {"input": [[0, 0, 0], [0, 3, 0], [0, 0, 4]], "output": [[3]]},
        {"input": [[5, 0, 0], [0, 0, 0], [0, 0, 6]], "output": [[5]]},
    ]
}

analysis_report = analyze_task(task)
print(analysis_report)
