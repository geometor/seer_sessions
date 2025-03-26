```python
"""
Scales the input grid by a factor of 2 in both height and width.
Each pixel in the input grid is replaced by a 2x2 block of the same color
in the output grid. The top-left corner of the 2x2 output block 
corresponding to the input pixel at (r, c) is located at (r*2, c*2)
in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Scales the input grid by a factor of 2.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The scaled output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)

    # Determine the dimensions of the input grid
    input_height, input_width = input_np.shape

    # Calculate the dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros (or any default value)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_np[r, c]

            # Determine the top-left coordinates for the 2x2 block in the output grid
            output_r_start = r * 2
            output_c_start = c * 2

            # Fill the corresponding 2x2 block in the output grid with the color
            output_grid[output_r_start, output_c_start] = color          # Top-left
            output_grid[output_r_start + 1, output_c_start] = color      # Bottom-left
            output_grid[output_r_start, output_c_start + 1] = color      # Top-right
            output_grid[output_r_start + 1, output_c_start + 1] = color  # Bottom-right

    return output_grid.tolist() # Return as list of lists to match ARC standard if needed, but numpy is often easier internally

```