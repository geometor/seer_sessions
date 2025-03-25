```python
"""
Transforms the input grid into an output grid by expanding each non-zero pixel into a block. The size of the block is determined by the ratio of output grid dimensions to input grid dimensions.
"""

import numpy as np

def transform(input_grid, output_grid):
    # Convert to numpy arrays for easier manipulation
    input_grid = np.array(input_grid)
    
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    # Calculate expansion factors
    vertical_expansion = output_height // input_height
    horizontal_expansion = output_width // input_width

    # Iterate through each pixel of the input grid
    for row_index in range(input_height):
        for col_index in range(input_width):
            pixel_value = input_grid[row_index, col_index]

            # If the pixel is non-zero, expand it
            if pixel_value != 0:
                # Calculate the top-left corner of the expanded block in the output grid
                top_left_row = row_index * vertical_expansion
                top_left_col = col_index * horizontal_expansion

                # Fill the corresponding block in the output grid
                for i in range(top_left_row, top_left_row + vertical_expansion):
                    for j in range(top_left_col, top_left_col + horizontal_expansion):
                        output_grid[i, j] = pixel_value

    return output_grid
```
