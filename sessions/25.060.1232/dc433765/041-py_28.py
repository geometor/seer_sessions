import numpy as np
from collections import Counter

def describe_grid(grid):
    rows, cols = grid.shape
    pixel_counts = Counter(grid.flatten())
    description = {
        'dimensions': (rows, cols),
        'pixel_counts': dict(pixel_counts)
    }
    return description

def compare_grids(input_grid, expected_output, actual_output):
    return {
        'input': describe_grid(input_grid),
        'expected_output': describe_grid(expected_output),
        'actual_output': describe_grid(actual_output),
        'match': np.array_equal(expected_output, actual_output)
    }

# dummy data, as no actual data is provided in the request, but is available for code_execution
task_examples = [
  {
    "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 3, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 4, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
    "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
  },
  {
    "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 3, 5, 5], [5, 5, 3, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 4, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]],
    "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
  },
  {
    "input": [[1, 1, 1, 5, 5, 5, 5, 5, 5], [1, 1, 1, 5, 5, 5, 3, 5, 5], [1, 1, 1, 5, 5, 3, 5, 5, 5], [1, 1, 1, 5, 5, 5, 5, 5, 5], [1, 1, 1, 5, 4, 5, 5, 5, 5], [1, 1, 1, 5, 5, 5, 5, 5, 5]],
    "output": [[1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 3, 0, 0, 0, 0], [1, 1, 1, 0, 4, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0]],
  }
]

results = [compare_grids(np.array(example['input']), np.array(example['output']), transform(np.array(example['input']))) for example in task_examples]
print(results)
