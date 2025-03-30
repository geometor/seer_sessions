```python
"""
Transforms an input grid based on its own pixel values.

1. Determine the height `H` and width `W` of the input grid.
2. Create a new output grid with dimensions `H*H` by `W*W`, initialized to white (0).
3. Iterate through each pixel `(r, c)` of the input grid.
4. If the input pixel `input_grid[r][c]` is non-white (value > 0), copy the entire original `H x W` input grid into the corresponding `H x W` block in the output grid. The top-left corner of this block in the output grid is at `(r * H, c * W)`.
5. If the input pixel `input_grid[r][c]` is white (value == 0), the corresponding `H x W` block in the output grid remains white (0).
6. Return the resulting output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine the height H and width W of the input grid.
    input_h, input_w = input_grid.shape

    # 2. Create a new output grid with dimensions H*H by W*W, initialized to white (0).
    output_h = input_h * input_h
    output_w = input_w * input_w
    output_grid = np.zeros((output_h, output_w), dtype=int) # 0 is white

    # 3. Iterate through each pixel (r, c) of the input grid.
    for r in range(input_h):
        for c in range(input_w):
            # 4. Examine the pixel value P at input[r][c].
            pixel_value = input_grid[r, c]

            # 5. If the pixel value P is not white (0):
            if pixel_value != 0:
                # Calculate the top-left corner coordinates for the corresponding block in the output grid.
                output_row_start = r * input_h
                output_col_start = c * input_w

                # Define the end coordinates for slicing (exclusive)
                output_row_end = output_row_start + input_h
                output_col_end = output_col_start + input_w

                # Copy the entire original H x W input grid into the output grid block.
                output_grid[output_row_start:output_row_end, output_col_start:output_col_end] = input_grid
            # 6. Else (if the pixel value P is white (0)):
            # The corresponding H x W block in the output grid remains filled with white (0) as initialized, no action needed.

    # 7. Return the completed output grid.
    return output_grid

```