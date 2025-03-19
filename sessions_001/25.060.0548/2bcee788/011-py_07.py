import numpy as np
from typing import List, Tuple, Dict

# dummy variables for code execution - provided by prompt
train = []
dummy_train = [
    {'input': [[0, 0, 0, 0, 0, 0],
               [0, 2, 2, 2, 0, 0],
               [0, 2, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0],
               [0, 6, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]],
     'output': [[3, 3, 3, 3, 3, 3],
                [3, 6, 6, 6, 3, 3],
                [3, 6, 3, 3, 3, 3],
                [3, 6, 3, 3, 3, 3],
                [3, 6, 3, 3, 3, 3],
                [3, 3, 3, 3, 3, 3]]
     },
    {'input': [[0, 0, 0, 0, 0],
               [0, 2, 2, 2, 0],
               [0, 2, 0, 0, 0],
               [0, 6, 0, 0, 0],
               [0, 0, 0, 0, 0]],
     'output': [[3, 3, 3, 3, 3],
                [3, 6, 6, 6, 3],
                [3, 6, 3, 3, 3],
                [3, 6, 3, 3, 3],
                [3, 3, 3, 3, 3]]
     },
    {'input': [[0, 0, 0, 0],
               [0, 2, 2, 0],
               [0, 2, 6, 0],
               [0, 0, 0, 0]],
     'output': [[3, 3, 3, 3],
                [3, 6, 6, 3],
                [3, 6, 6, 3],
                [3, 3, 3, 3]]
     },
    {'input': [[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 2, 2, 2, 0, 0],
               [0, 0, 2, 0, 0, 0, 0],
               [0, 0, 2, 0, 0, 0, 0],
               [0, 0, 6, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]],
     'output': [[3, 3, 3, 3, 3, 3, 3],
                [3, 3, 6, 6, 6, 3, 3],
                [3, 3, 6, 3, 3, 3, 3],
                [3, 3, 6, 3, 3, 3, 3],
                [3, 3, 6, 3, 3, 3, 3],
                [3, 3, 3, 3, 3, 3, 3]]
     },
     {'input': [[0, 2, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 0],
                [0, 6, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]],
        'output': [[3, 6, 3, 3, 3, 3, 3],
                 [3, 6, 3, 3, 3, 3, 3],
                 [3, 6, 3, 3, 3, 3, 3],
                 [3, 3, 3, 3, 3, 3, 3]]}
]

train = dummy_train  # replace with prompt.train when available

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Replace all white (0) pixels with green (3)
    output_grid[output_grid == 0] = 3

    # Replace all red (2) pixels with magenta (6)
    output_grid[output_grid == 2] = 6

    # Magenta (6) pixels remain unchanged, so no additional operations are needed.

    return output_grid

def compare_grids(grid1, grid2):
    """Compares two grids and returns the number of differing pixels."""
    return np.sum(grid1 != grid2)

def analyze_examples(examples, transform_function):
    """Analyzes a set of examples and returns a dictionary of results."""

    results = {}
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        actual_output_grid = transform_function(input_grid)
        differences = compare_grids(expected_output_grid, actual_output_grid)
        results[f'example_{i+1}'] = {
            'input_shape': input_grid.shape,
            'output_shape': expected_output_grid.shape,
            'differences': differences,
            'same_size': expected_output_grid.shape == actual_output_grid.shape,

        }
    return results

results = analyze_examples(train, transform)
print(results)