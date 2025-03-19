# aba27056 • 007 • refine_coder

---
```python
"""
1.  **Identify the Magenta Shape:** Find all pixels with the color magenta. These pixels form a single, contiguous object.

2.  **Create the Yellow Border:**  Change the color of all black pixels that are directly adjacent (up, down, left, or right) to any magenta pixel to yellow. This creates a yellow border around the magenta shape.

3.  **Fill the Interior (if any):** If there are any black pixels completely enclosed within the combined magenta shape and yellow border, change those pixels to yellow.
"""

import numpy as np

def find_magenta_shape(grid):
    # Find coordinates of all magenta pixels
    magenta_coords = np.argwhere(grid == 6)
    return magenta_coords

def create_yellow_border(grid, magenta_coords):
    # Create a copy of the grid to modify, initially all black
    border_grid = np.zeros_like(grid)
    rows, cols = grid.shape

    # Mark all cells adjacent to magenta as yellow (including diagonals for
    # complete fill later
    for r, c in magenta_coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                    border_grid[nr, nc] = 4  # Set to yellow
    return border_grid

def flood_fill(grid, start_row, start_col, target_color, replacement_color):
    """Performs a flood fill on the grid."""
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols):
        return  # Start position out of bounds
    if grid[start_row, start_col] != target_color:
        return # start position is not the target color

    queue = [(start_row, start_col)]
    grid[start_row, start_col] = replacement_color

    while queue:
        r, c = queue.pop(0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == target_color:
                grid[nr, nc] = replacement_color
                queue.append((nr, nc))

def fill_interior(grid, magenta_coords, border_grid):
    # Combine the magenta shape and the yellow border
    combined_grid = np.copy(grid)
    rows,cols = grid.shape
    
    # where we see a border pixel, set it to yellow,
    # so now we have magemta and yellow
    for r in range(rows):
        for c in range(cols):
            if border_grid[r,c] == 4:
                combined_grid[r,c] = 4
    
    # first, find all the black cells
    black_cells = np.argwhere(combined_grid == 0)
    if len(black_cells) == 0:
        return combined_grid
    
    # iterate over the perimeter, and if you find black, do a flood fill.
    # fill any black cells not on the border with yellow,
    # using the combined_grid which consists of magenta, and yellow
    for r in range(rows):
        for c in [0, cols -1]:
            if combined_grid[r,c] == 0:
                flood_fill(combined_grid, r, c, 0, 4)

    for c in range(cols):
        for r in [0, rows - 1]:
            if combined_grid[r,c] == 0:
                flood_fill(combined_grid, r, c, 0, 4)
                
    # set any left over black cells to yellow
    for r in range(rows):
        for c in range(cols):
            if combined_grid[r,c] == 0:
                combined_grid[r,c] = 4

    return combined_grid

def transform(input_grid):
    # Find the magenta shape
    magenta_coords = find_magenta_shape(input_grid)

    # Create the yellow border
    border_grid = create_yellow_border(input_grid, magenta_coords)
    
    # Fill the interior
    output_grid = fill_interior(input_grid, magenta_coords, border_grid)
    
    return output_grid
```
