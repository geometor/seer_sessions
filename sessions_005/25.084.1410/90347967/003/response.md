```python
"""
Transforms the input grid based on the number of edges touched by the single connected object of non-white pixels.
1. Identify the single connected group of non-white pixels (8-way connectivity).
2. Count how many of the four grid edges (Top, Bottom, Left, Right) this group touches (E).
3. Rotate the entire input grid by 180 degrees.
4. If E is exactly 1, shift the rotated grid up by 2 rows (filling the bottom 2 rows with white).
5. Otherwise, use the rotated grid directly as the output.
"""

import numpy as np
from scipy.ndimage import label

def count_edges_touched(grid):
    """
    Counts the number of grid edges touched by non-white pixels.
    Assumes a single connected component or handles empty grid.
    """
    height, width = grid.shape
    
    # Find coordinates of non-white pixels
    non_white_coords = np.argwhere(grid != 0) # Use != 0 for non-white
    
    # Handle empty grid case
    if non_white_coords.shape[0] == 0:
        return 0 
        
    r_min = non_white_coords[:, 0].min()
    r_max = non_white_coords[:, 0].max()
    c_min = non_white_coords[:, 1].min()
    c_max = non_white_coords[:, 1].max()
    
    touches_top = (r_min == 0)
    touches_bottom = (r_max == height - 1)
    touches_left = (c_min == 0)
    touches_right = (c_max == width - 1)
    
    num_edges_touched = sum([touches_top, touches_bottom, touches_left, touches_right])
    
    return num_edges_touched

def rotate_180(grid):
    """Rotates a 2D grid by 180 degrees."""
    height, width = grid.shape
    rotated_grid = np.zeros_like(grid)
    for r in range(height):
        for c in range(width):
            rotated_grid[height - 1 - r, width - 1 - c] = grid[r, c]
    return rotated_grid

def shift_up(grid, rows):
    """Shifts a grid up by a specified number of rows, filling bottom with white (0)."""
    height, width = grid.shape
    shifted_grid = np.zeros_like(grid)
    if rows >= height: # Shifting more than height results in empty grid
        return shifted_grid 
    # Copy the relevant part of the original grid to the shifted position
    shifted_grid[0:height-rows, :] = grid[rows:height, :]
    return shifted_grid

def transform(input_grid):
    """
    Applies the conditional rotation and shift transformation.
    """
    # Convert input to numpy array
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Check for trivial case: all white grid
    if np.all(grid == 0):
        return grid # Return the input grid as is

    # 1. & 2. Count edges touched by the non-white object(s)
    # Note: We are assuming based on examples there's only one object if non-white pixels exist.
    # The edge counting doesn't strictly need the single object assumption, just non-white pixels.
    num_edges = count_edges_touched(grid)

    # 3. Rotate the grid 180 degrees
    rotated_grid = rotate_180(grid)

    # 4. & 5. Apply conditional shift
    if num_edges == 1:
        # Shift the rotated grid up by 2 rows
        output_grid = shift_up(rotated_grid, 2)
    else:
        # No shift needed
        output_grid = rotated_grid

    return output_grid.tolist() # Return as list of lists per ARC standard

```