```python
"""
1.  **Identify Azure Regions:** Locate all contiguous regions of azure (8) colored pixels in the input grid.  Pixels are considered part of the same region if they are adjacent horizontally or vertically. Also locate isolated azure pixels (with no adjacent azure pixels).

2.  **Classify Azure Pixels:** Within each identified azure region, classify each azure pixel as follows:
    *   **Border Pixel:** An azure pixel is a border pixel if *at least one* of its four directly adjacent neighbors (up, down, left, or right) has a color *different* from azure (8).
    *   **Interior Pixel:** An azure pixel is an interior pixel if *all* of its four directly adjacent neighbors (up, down, left, or right) are also azure (8).
    * **Isolated Pixel:** An azure pixel which has no azure colored neighbors.

3.  **Apply Transformation:**
    *   Change the color of all border azure pixels to red (2).
    *   Change the color of all interior azure pixels to blue (1).
    *  Change the color of all isolated azure pixels to red (2)
    *   Leave all other (non-azure) pixels unchanged.
"""

import numpy as np

def get_cardinal_neighbors(grid, row, col):
    """Gets the 4 directly adjacent neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Cardinal directions
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def is_border(grid, row, col, color):
    """Checks if a cell of the specified color is a border cell."""
    if grid[row, col] != color:
        return False

    neighbors = get_cardinal_neighbors(grid, row, col)
    for nr, nc in neighbors:
        if grid[nr, nc] != color:
            return True  # Found a different colored neighbor
    return False

def is_interior(grid, row, col, color):
    """Checks if a cell of the specified color is an interior cell."""
    if grid[row, col] != color:
        return False

    neighbors = get_cardinal_neighbors(grid, row, col)
    if not neighbors:
        return False

    for nr, nc in neighbors:
        if grid[nr, nc] != color:
            return False  # Found a different colored neighbor
    return True # All neighbors are same color

def is_isolated(grid, row, col, color):
    """check if a cell of the specified color is isolated"""
    if grid[row, col] != color:
        return False
    
    neighbors = get_cardinal_neighbors(grid, row, col)
    
    for nr, nc in neighbors:
        if grid[nr, nc] == color:
            return False
    return True

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find azure regions and apply replacements
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 8:  # Found an azure pixel
                if is_isolated(input_grid, row, col, 8):
                    output_grid[row, col] = 2
                elif is_border(input_grid, row, col, 8):
                    output_grid[row, col] = 2  # Replace border azure with red
                elif is_interior(input_grid, row, col, 8):
                    output_grid[row, col] = 1  # Replace interior azure with blue

    return output_grid
```