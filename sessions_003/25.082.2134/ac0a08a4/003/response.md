```python
"""
Transforms the input grid into an output grid by expanding each non-zero pixel into a block. The size of each block is determined by calculating an expansion factor based on the input and output grid dimensions. Zero-valued pixels in the input act as dynamic separators.
"""

import numpy as np

def calculate_expansion_factor(input_grid, output_height, output_width):
    """Calculates the expansion factor for height and width."""
    input_height, input_width = input_grid.shape
    height_factor = output_height / input_height
    width_factor = output_width / input_width
    return int(height_factor), int(width_factor)

def transform(input_grid, output_grid):
    # Get dimensions of the input and output grids
    output_height, output_width = output_grid.shape

    # Calculate expansion factors
    height_factor, width_factor = calculate_expansion_factor(input_grid, output_height, output_width)

    # Iterate through each pixel of the input grid
    for row_index in range(input_grid.shape[0]):
        for col_index in range(input_grid.shape[1]):
            pixel_value = input_grid[row_index, col_index]

            # If the pixel is non-zero, expand it into a block
            if pixel_value != 0:
                start_row = row_index * height_factor
                start_col = col_index * width_factor
                for i in range(height_factor):
                    for j in range(width_factor):
                        output_grid[start_row + i, start_col + j] = pixel_value

    return output_grid
```