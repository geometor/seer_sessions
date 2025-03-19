# 10fcaaa3 • 020 • example_4 • investigate_coder

---
```python
"""
The transformation rule involves replicating a single red pixel (value 2) in the input grid and adding an azure (value 8) frame around it. The output grid is double the size of the input grid. The red pixel is replicated downwards, and azure pixels form alternating rows to create a checkerboard-like pattern with the white background.
"""

import numpy as np

def find_object(grid, object_value):
    """Finds the coordinates of an object with a specific value in the grid."""
    coords = np.where(grid == object_value)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return first occurrence
    return None

def transform(input_grid):
    # Initialize the output grid with double the dimensions, filled with white (0).
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Find the red pixel (object of interest).
    red_pixel_coords = find_object(input_grid, 2)

    if red_pixel_coords:

        # replicate the red pixel row
        row = input_grid[red_pixel_coords[0]]

        # create the framing row
        frame_row = np.zeros(output_cols, dtype=int)
        for i in range(output_cols):
            if i % 2 == 0:
                frame_row[i] = 8
        
        # Assemble
        for r in range(input_rows):
           output_grid[r*2] = frame_row
           new_row = np.zeros(output_cols, dtype=int)
           for i in range(len(row)):
               if row[i] == 2:
                   new_row[i*2] = 2

           output_grid[r*2 + 1] = new_row
    
    return output_grid
```
