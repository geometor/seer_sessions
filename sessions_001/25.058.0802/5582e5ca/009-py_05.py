import numpy as np
from collections import Counter

def analyze_grid_pair(input_grid, output_grid):
    """Analyzes a single input-output grid pair and returns relevant metrics."""

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_colors = Counter(input_grid.flatten())
    output_colors = Counter(output_grid.flatten())
    shape_change = input_grid.shape != output_grid.shape

    return {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "input_colors": dict(input_colors),
        "output_colors": dict(output_colors),
        "shape_change": shape_change,
    }

# Example data (replace with actual example data from the task)
examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1]],

        [[9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 8]],

        [[9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9],
         [9, 9, 9, 9, 9, 9, 9, 9, 9]]
    ),
]

results = [analyze_grid_pair(inp, out) for inp, out in examples]
print(results)