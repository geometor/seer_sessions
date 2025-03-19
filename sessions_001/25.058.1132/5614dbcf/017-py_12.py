task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0],
                [0, 0, 0],
                [0, 1, 0]
            ]
        },
       {
            "input": [
                [0, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 2, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 3, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        }
    ],
    "test": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0],
                [0, 0, 0],
                [0, 4, 0]
            ]
        }
    ]
}

import numpy as np

def get_subgrid(grid, row_start, col_start):
    """Extracts a 3x3 subgrid from the input grid."""
    return grid[row_start:row_start+3, col_start:col_start+3]

def find_first_nonzero(subgrid):
    """Finds the first non-zero element in a subgrid and returns its value."""
    rows, cols = subgrid.shape
    for i in range(rows):
        for j in range(cols):
            if subgrid[i,j] != 0:
                return subgrid[i,j]
    return 0

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize output_grid as a 3x3 array filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the top-center 3x3 subgrid.
    top_center_subgrid = get_subgrid(input_grid, 0, 3)
    # Find the first non-zero value in the top-center subgrid.
    top_center_value = find_first_nonzero(top_center_subgrid)

    # Check if a non-zero value was found in the top-center subgrid.
    if top_center_value != 0:
        # Place the value in the output grid.
        output_grid[0, 1] = top_center_value
    else:
        # Get the bottom-center 3x3 subgrid.
        bottom_center_subgrid = get_subgrid(input_grid, 6, 3)
        # Find the first non-zero value in the bottom-center subgrid.
        bottom_center_value = find_first_nonzero(bottom_center_subgrid)
        # Place the value in the output grid.
        output_grid[2, 1] = bottom_center_value

    return output_grid

report_metrics(task, transform)