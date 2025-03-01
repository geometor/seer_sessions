# fcb5c309 • 014 • refine_coder

---
```python
"""
1.  **Locate Green Shape:** Find all pixels in the input grid that are green (value 3). These pixels constitute the "green shape."
2.  **Bounding Box:** Determine the rectangular bounding box that completely encloses the green shape. This is done by finding the minimum and maximum row and column indices of all green pixels.
3.  **Identify Exterior:** Create a temporary working grid the same size as the input grid. Perform a flood fill operation on this temporary grid, starting from outside the identified bounding box. Use a distinct temporary color (e.g., -1) that is not present in the original grid. This flood fill will mark all pixels *outside* the green shape.
4.  **Identify Interior:** Examine the temporary grid created in step 3. Any pixel within the bounding box that remains its original colour (i.e. is not green (3) and is not the temporary exterior color (-1)), is by definition, inside the enclosed region.
5.  **Create Output Grid:** Create a new output grid with dimensions equal to the bounding box.
6.  **Populate Output Grid**: Populate the grid as follows:
    *   Pixels corresponding to the `green_shape` are set to green (3).
    *   Pixels identified as part of the `enclosed_region` are set to white (0).
7.  **Return:** Return the output grid.
"""

import numpy as np

def get_green_pixel_coords(grid):
    # Find coordinates of all green pixels (value 3).
    return np.argwhere(grid == 3)

def get_bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    if len(coords) == 0:
        return 0, -1, 0, -1  # Handle empty case
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
    input_grid = np.array(input_grid)
    # Find coordinates of all green pixels.
    green_coords = get_green_pixel_coords(input_grid)

    # Determine the bounding box around the green pixels.
    min_row, max_row, min_col, max_col = get_bounding_box(green_coords)

    # Create a temporary grid for flood filling, initialized to the input grid.
    temp_grid = np.copy(input_grid)

    # Flood fill the exterior with -1, starting from outside each edge of bounding box
    for r in range(input_grid.shape[0]):
      if r < min_row or r > max_row:
        flood_fill(temp_grid, r, 0, input_grid[r,0], -1) #left
        flood_fill(temp_grid, r, input_grid.shape[1]-1, input_grid[r,input_grid.shape[1]-1], -1) #right
    for c in range(input_grid.shape[1]):
      if c < min_col or c > max_col:
        flood_fill(temp_grid, 0, c, input_grid[0,c], -1) # top
        flood_fill(temp_grid, input_grid.shape[0]-1, c, input_grid[input_grid.shape[0]-1,c], -1)  #bottom

    # Create output grid from identified boundary
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.full((output_height, output_width), 3, dtype=int)

    # Fill enclosed regions within the bounding box.
    for r in range(output_height):
        for c in range(output_width):
            original_r = r + min_row
            original_c = c + min_col

            # if temp grid is not green and not exterior, then it's interior
            if temp_grid[original_r, original_c] != 3 and temp_grid[original_r, original_c] != -1:
                output_grid[r, c] = 0

    return output_grid.tolist()
```
