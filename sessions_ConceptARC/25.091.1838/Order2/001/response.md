```python
import numpy as np

"""
Applies vertical gravity to non-white pixels within each column of the input grid.

1. Initialize an output grid of the same dimensions as the input, filled with white (0).
2. For each column in the input grid:
    a. Collect all non-white pixels from top to bottom.
    b. Place these collected pixels at the bottom of the corresponding column in the output grid, maintaining their relative order.
    c. The remaining cells above the stacked pixels in the output column remain white (0).
"""

def transform(input_grid):
    """
    Applies vertical gravity independently to each column of the grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid after applying gravity.
    """
    # Convert input list of lists to a numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_np = np.zeros_like(input_np)

    # Process each column independently
    for col_index in range(width):
        # Extract the current column from the input grid
        column = input_np[:, col_index]

        # Find the non-white pixels in this column
        non_white_pixels = column[column != 0]

        # Count how many non-white pixels were found
        num_non_white = len(non_white_pixels)

        # If there are any non-white pixels in this column
        if num_non_white > 0:
            # Place the non-white pixels at the bottom of the corresponding column
            # in the output grid. The slicing ensures they are placed starting
            # from the bottom row upwards.
            output_np[height - num_non_white : height, col_index] = non_white_pixels

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```