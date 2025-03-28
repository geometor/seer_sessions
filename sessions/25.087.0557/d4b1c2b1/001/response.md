```python
import numpy as np
import collections

"""
Identify all unique pixel values (colors) in the input grid, excluding white (0).
Count the number of these unique non-white colors. This count is the scaling factor S. If there are no non-white colors or only one, the scaling factor is 1.
Determine the dimensions of the input grid: input_height and input_width.
Calculate the dimensions of the output grid: output_height = input_height * S and output_width = input_width * S.
Create a new grid with the calculated output_height and output_width.
Iterate through each pixel (r, c) of the input grid:
  Get the color C of the input pixel at (r, c).
  In the output grid, fill a square block of size S x S, starting at the top-left corner (r * S, c * S), with the color C.
Return the generated output grid.
"""

def find_scale_factor(grid):
    """
    Counts the number of unique non-white colors in the grid.
    Returns the count, or 1 if the count is 0.
    """
    unique_colors = set(grid.flatten())
    non_white_colors = unique_colors - {0} # Remove white color (0)
    count = len(non_white_colors)
    # The scaling factor is the count, but at least 1.
    # Examples 4 and 5 show that if only one color exists, the scale factor is 1.
    return max(1, count) 

def transform(input_grid):
    """
    Scales the input grid based on the number of unique non-white colors.
    Each pixel in the input grid is expanded into a square block of size SxS
    in the output grid, where S is the count of unique non-white colors (min 1).
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Determine the scaling factor S
    scale_factor = find_scale_factor(input_np)

    # Calculate output dimensions
    output_height = input_height * scale_factor
    output_width = input_width * scale_factor

    # Initialize the output grid (e.g., with zeros)
    # Using the color of the top-left input pixel might be safer if 0 isn't guaranteed background
    # but examples suggest 0 is safe, or it gets overwritten anyway.
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_np[r, c]

            # Calculate the top-left corner of the block in the output grid
            start_row = r * scale_factor
            start_col = c * scale_factor

            # Calculate the end coordinates (exclusive) for slicing
            end_row = start_row + scale_factor
            end_col = start_col + scale_factor

            # Fill the corresponding S x S block in the output grid with the color
            output_grid[start_row:end_row, start_col:end_col] = color

    # Return the output grid (as a list of lists if required by the environment)
    # For now, return as numpy array as it's common in ARC contexts.
    # Convert back to list of lists if necessary: return output_grid.tolist()
    return output_grid.tolist() 
```