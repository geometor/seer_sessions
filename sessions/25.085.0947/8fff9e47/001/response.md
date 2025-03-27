```python
import numpy as np

"""
The transformation scales the input grid to a fixed 12x12 output grid.
Each pixel in the input grid is expanded into a rectangular block in the output grid.
The size of this block depends on the input grid's dimensions relative to the 12x12 output size.
Specifically, if the input grid has height H_in and width W_in, each input pixel at (r, c)
corresponds to a block of size (12 / H_in) x (12 / W_in) in the output grid,
starting at position (r * (12 / H_in), c * (12 / W_in)).
The color of this output block is the same as the color of the input pixel at (r, c).
It is assumed that 12 is always divisible by both H_in and W_in.
"""

def transform(input_grid):
    """
    Scales the input grid to a 12x12 output grid by expanding each pixel into a block.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 12x12 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid = np.array(input_grid, dtype=int)

    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Define fixed output dimensions
    output_height = 12
    output_width = 12

    # Calculate scaling factors (assuming integer division)
    scale_h = output_height // input_height
    scale_w = output_width // input_width

    # Initialize the output grid (e.g., with zeros/white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_grid[r, c]

            # Calculate the top-left corner of the corresponding block in the output grid
            out_r_start = r * scale_h
            out_c_start = c * scale_w

            # Calculate the bottom-right corner (exclusive) of the block
            out_r_end = out_r_start + scale_h
            out_c_end = out_c_start + scale_w

            # Fill the block in the output grid with the input pixel's color
            output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = color

    return output_grid
```