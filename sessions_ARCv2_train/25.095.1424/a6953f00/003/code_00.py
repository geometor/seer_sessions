"""
Transforms an input grid of integers into a 2x2 output grid.
The transformation rule depends on the width of the input grid.
If the input grid's width is odd, the output is the top-left 2x2 subgrid.
If the input grid's width is even, the output is the top-right 2x2 subgrid.
The input grid is assumed to have at least 2 rows and 2 columns.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects a 2x2 subgrid from the input grid based on the grid's width parity.

    Args:
        input_grid: A list of lists representing the input grid of integers.
                    It's assumed to have at least 2 rows and 2 columns.

    Returns:
        A 2x2 list of lists representing the selected subgrid.
    """
    # Convert the input list of lists to a NumPy array for easier slicing
    input_np = np.array(input_grid)

    # Get the dimensions (height and width) of the input grid
    height, width = input_np.shape

    # Initialize an empty NumPy array for the output (though slicing directly is easier)
    # output_np = np.empty((2, 2), dtype=int) # Not strictly needed

    # Check if the width is even or odd
    if width % 2 == 0:
        # Width is even: select the top-right 2x2 subgrid
        # Rows 0 and 1, Columns width-2 and width-1
        selected_subgrid_np = input_np[0:2, width-2:width]
    else:
        # Width is odd: select the top-left 2x2 subgrid
        # Rows 0 and 1, Columns 0 and 1
        selected_subgrid_np = input_np[0:2, 0:2]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = selected_subgrid_np.tolist()

    return output_grid