import numpy as np
from typing import List, Tuple

#provided code
def rotate_clockwise(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)

def get_blue_shape(grid):
    """Extracts the connected blue shape from the grid."""
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
        return np.array([[]])  # Return an empty grid
    min_row = np.min(blue_pixels[:, 0])
    max_row = np.max(blue_pixels[:, 0])
    min_col = np.min(blue_pixels[:, 1])
    max_col = np.max(blue_pixels[:, 1])
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Extract the blue shape
    blue_shape = get_blue_shape(input_grid)

    # Rotate the blue shape
    rotated_shape = rotate_clockwise(blue_shape)

    # Create a new output grid filled with white, with dimensions of the rotated shape
    output_grid = np.zeros(rotated_shape.shape, dtype=input_grid.dtype)

    # Place the rotated shape in the top-left corner
    output_grid[:rotated_shape.shape[0], :rotated_shape.shape[1]] = rotated_shape

    return output_grid
#end provided code

def arrays_equal(arr1, arr2):
    return np.array_equal(arr1, arr2)

def calculate_metrics(task: dict):
    results = []
    all_match = True  # Initialize to True
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        actual_output = transform(input_grid)
        match = arrays_equal(actual_output, expected_output)
        
        if not match:  # Update all_match if any example doesn't match
            all_match = False
        
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': actual_output.shape,
            'expected_output_shape': expected_output.shape,
            'match': match,
            'output': actual_output.tolist(),
        })

    return all_match, results

# example task data - replace with the actual data from a task json file
task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
      ],
      "output": [
        [1, 1],
        [1, 1]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1]
      ]
    },
    {
      "input": [
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [1, 1, 1, 1]
      ]
    }
  ]
}

all_match, execution_results = calculate_metrics(task)
print(f"{all_match=}")
for r in execution_results:
  print(r)
