```python
"""
Transforms a 3x3 input grid into a larger output grid by expanding each non-zero pixel into a 5x5 block of the same color. Zero-valued pixels in the input are represented as zero-filled separators in the output, their sizes dynamically adjusted to accommodate the expanded blocks.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid
    input_height, input_width = input_grid.shape
    
    # expansion factor
    expansion_factor = 5

    # Initialize the output grid with zeros, 5 times the size of the input grid
    output_height = input_height * expansion_factor
    output_width = input_width * expansion_factor
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for row_index in range(input_height):
        for col_index in range(input_width):
            pixel_value = input_grid[row_index, col_index]

            # If the pixel is non-zero, expand it into a 5x5 block
            if pixel_value != 0:
                start_row = row_index * expansion_factor
                start_col = col_index * expansion_factor
                for i in range(expansion_factor):
                    for j in range(expansion_factor):
                        output_grid[start_row + i, start_col + j] = pixel_value

    return output_grid
```