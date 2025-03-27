```python
import numpy as np

"""
Identify the color (C) of the single non-white pixel in the input grid.
Create an output grid of the same dimensions as the input.
Fill the border pixels (top row, bottom row, leftmost column, rightmost column) of the output grid with color C.
Fill all interior pixels (if any) of the output grid with white (0).
"""

def find_non_background_color(grid, background_color=0):
    """
    Finds the first color in the grid that is not the background_color.
    Assumes there is exactly one such color.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != background_color:
            return color
    # Should not happen based on task description, but return background as fallback
    return background_color 

def transform(input_grid):
    """
    Transforms the input grid by finding the single non-white pixel's color
    and creating a frame of that color around the border of an output grid
    of the same dimensions, filling the interior with white.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Find the color of the single non-white pixel
    frame_color = find_non_background_color(input_np, 0)
    
    # Initialize output_grid with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Fill the border with the frame_color
    # Fill top row
    if height > 0:
        output_grid[0, :] = frame_color
    # Fill bottom row
    if height > 1:
        output_grid[height - 1, :] = frame_color
    # Fill left column
    if width > 0:
        output_grid[:, 0] = frame_color
    # Fill right column
    if width > 1:
        output_grid[:, width - 1] = frame_color
        
    # Interior is already filled with 0 (white) due to initialization

    return output_grid.tolist()
```