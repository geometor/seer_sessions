# fcb5c309 • 012 • refine_coder

---
```python
"""
1.  **Identify Green Pixels:** Locate all green (value 3) pixels in the input grid.
2.  **Determine Bounding Box:** Find the minimum and maximum row and column indices of the green pixels to define a rectangular bounding box.
3.  **Create Initial Output:** Create a new grid with dimensions equal to the bounding box and initialize every pixel in the output grid to green.
4.  **Identify Enclosed Regions:** Within the bounding box, analyze the connectivity of non-green pixels. A non-green pixel is part of an *enclosed region* if it is fully surrounded by green pixels, either directly adjacent or via a path of other enclosed non-green pixels. This requires a traversal/flood-fill type approach.
5.  **Color Interior:** Change the color of all identified *enclosed region* pixels within the bounding box to white (value 0).
6.  **Return Bounding Box:** Return the new grid, which now contains the correct green outline and white infill.
"""

import numpy as np

def get_green_pixel_coords(grid):
    # Find coordinates of all green pixels (value 3).
    return np.argwhere(grid == 3)

def get_bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Performs a flood fill on the grid, starting from (row, col).

    Args:
        grid: The numpy array representing the grid.
        row: Starting row index.
        col: Starting column index.
        target_color: The color to be replaced.
        replacement_color: The new color.
    """
    if row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]:
        return  # Out of bounds

    if grid[row, col] != target_color:
        return  # Not the target color

    grid[row, col] = replacement_color

    # Recursively fill adjacent cells
    flood_fill(grid, row + 1, col, target_color, replacement_color)
    flood_fill(grid, row - 1, col, target_color, replacement_color)
    flood_fill(grid, row, col + 1, target_color, replacement_color)
    flood_fill(grid, row, col - 1, target_color, replacement_color)

def transform(input_grid):
    # Find coordinates of all green pixels.
    green_coords = get_green_pixel_coords(np.array(input_grid))

    # Determine the bounding box around the green pixels.
    min_row, max_row, min_col, max_col = get_bounding_box(green_coords)

    # Create output grid from identified boundary and initialize to green.
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.full((output_height, output_width), 3, dtype=int)

    # Create a mask for the "inside" based on original green pixel locations, relative to bounding box
    rel_green_coords = green_coords - [min_row, min_col]
    inside_mask = np.zeros((output_height, output_width), dtype=bool)
    for r, c in rel_green_coords:
        inside_mask[r, c] = True

    # Create a temporary grid for flood filling, initialized to all green
    temp_grid = np.full((output_height, output_width), 3, dtype=int)

    # Mark known green pixels on temp_grid
    for r, c in rel_green_coords:
        temp_grid[r,c] = 3

    # Iterate and use flood fill to identify and fill enclosed regions.
    for r in range(output_height):
        for c in range(output_width):
            if temp_grid[r, c] != 3:  # Not green, might be inside
                flood_fill(temp_grid, r, c, 0, 0) # Temporarily fill with 0
    
    # now identify any remaining 0s and set to white, because they are enclosed
    for r in range(output_height):
      for c in range(output_width):
         if temp_grid[r,c] == 0:
            output_grid[r,c] = 0

    return output_grid.tolist()
```
