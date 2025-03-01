"""
1.  **Identify the magenta shape:** Locate the contiguous block of magenta (6) pixels in the input grid.
2.  **Overlay Yellow Inside:** Find the pixels that are directly above magenta and make yellow.
3.  **Overlay Border:**
    *   Locate all white (0) pixels adjacent to any magenta (6) pixel.
    *   For any horizontal edges of magenta pixels, extend the border one step further in the perpendicular direction. This creates a kind of cross-stitch pattern
"""

import numpy as np

def find_magenta_shape(grid):
    # Find coordinates of all magenta pixels
    magenta_coords = np.argwhere(grid == 6)
    return magenta_coords

def overlay_yellow_inside(grid, magenta_coords):
    # Create a copy of the grid to modify
    new_grid = np.copy(grid)
    for r, c in magenta_coords:
        if r > 0 and grid[r-1,c] == 0:
          new_grid[r-1, c] = 4  # Set pixel above to yellow
    return new_grid

def overlay_border(grid, magenta_coords):
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    for r, c in magenta_coords:
        # Check adjacent pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                new_grid[nr, nc] = 4
                
        #check for horizontal, and extend
        if 0 <= r-1 < rows and 0 <= c+1 < cols and grid[r-1,c+1] == 0 and grid[r,c+1] == 6:
            if 0 <= r-2 < rows and 0 <= c+1 < cols:
                new_grid[r-2,c+1] = 4
        if 0 <= r-1 < rows and 0 <= c-1 < cols and grid[r-1,c-1] == 0 and grid[r,c-1] == 6:
            if 0 <= r-2 < rows and 0<= c-1 < cols:
                new_grid[r-2,c-1] = 4

    return new_grid

def transform(input_grid):
    # Find the magenta shape
    magenta_coords = find_magenta_shape(input_grid)

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Overlay Yellow Inside
    output_grid = overlay_yellow_inside(output_grid, magenta_coords)

    # Overlay Border
    output_grid = overlay_border(output_grid, magenta_coords)
    
    return output_grid