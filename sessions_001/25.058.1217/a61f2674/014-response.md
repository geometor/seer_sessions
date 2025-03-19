# a61f2674 • 014 • refine_coder

---
```python
"""
1.  **Identify the Blue Line:** Find the vertical line of blue (1) pixels in the output grid. This line consistently replaces the centermost vertical gray (5) line in the input.
2.  **Locate Trigger Pixels:**  Identify pixels in the *input* grid that have the same column as red lines in the *output* grid.  These are the "trigger" pixels.
3.  **Create Red Lines Based on Triggers:** For each trigger pixel, create a vertical red (2) line in the output grid.  The red line starts at the same row as the trigger and extends *downward* until it either reaches the bottom of the grid or encounters a non-black (0) pixel in the *output* grid.  The red line appears in the same column as the trigger pixel.
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds all vertical lines of the specified color."""
    height, width = grid.shape
    lines = []
    for col in range(width):
        for row in range(height):
            if grid[row, col] == color:
                lines.append((row, col))
                break  # Move to the next column after finding a line
    return lines
def get_trigger_pixels(input_grid, output_grid):
    """
    Finds pixels in the input_grid that cause red lines in output_grid.
    The trigger pixels are in the same column as the red lines.
    """
    red_cols = set([c for r, c in find_vertical_line(output_grid, 2)])
    trigger_pixels = []
    for col in red_cols:
        for row in range(input_grid.shape[0]):
          trigger_pixels.append((row, col)) #all pixels in the column are triggers
    return trigger_pixels

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the centermost vertical gray line in the input and replace with blue
    center_col = width // 2
    
    #replace gray with blue - but only when there is an odd number of cols
    #and when all the values in the center column are the same
    unique_vals = np.unique(input_grid[:,center_col])
    if width % 2 != 0 and len(unique_vals) == 1 and unique_vals[0] == 5:    
        for row in range(height):
                output_grid[row, center_col] = 1

    # Create red lines
    #first locate them in output_grid
    trigger_pixels = get_trigger_pixels(input_grid, output_grid)

    for trigger_row, trigger_col in trigger_pixels:
      #only create trigger in locations where there is existing output
      if output_grid[trigger_row, trigger_col] != 0:
        for row in range(trigger_row, height):
            if output_grid[row, trigger_col] != 0 and output_grid[row, trigger_col] != 2:
                break # Stop if not black or red
            output_grid[row, trigger_col] = 2

    return output_grid
```
