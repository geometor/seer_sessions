# f15e1fac • 014 • refine_coder

---
```python
"""
1.  **Identify Azure Pixels:** Locate all pixels in the input grid with the color azure (8).
2.  **Check for Diagonal Arrangement:** If all azure pixels lie on a diagonal line (where the sum of the row index and column index is constant for all azure pixels), move each azure pixel to the main diagonal (where the row index equals the column index). Ensure new positions are within grid bounds.
3. **Check for Single Column:** If the azure pixels are *not* on a diagonal and they are all within a single column, extend that column. Find the lowest row index containing an azure pixel in the column. Add one azure pixel immediately below it, if adding the pixel does not exceed the grid boundaries.
4. **Other cases:** If azure pixels are present but the arrangement is neither a diagonal (as described above) nor a single column, the output is identical to the input.
"""

import numpy as np

def find_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels."""
    return np.argwhere(grid == 8)

def is_diagonal(azure_coords):
    """Checks if the given azure pixel coordinates form a diagonal line."""
    if len(azure_coords) == 0:
        return False
    first_sum = azure_coords[0][0] + azure_coords[0][1]
    return all(i + j == first_sum for i, j in azure_coords)

def move_to_main_diagonal(grid, azure_coords):
    """Moves azure pixels to the main diagonal, respecting grid bounds."""
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    output_grid[output_grid == 8] = 0 #clear existing
    for i, j in azure_coords:
        new_index = min(i,j, rows - 1, cols - 1)
        output_grid[new_index, new_index] = 8
    return output_grid

def is_single_column(azure_coords):
    """Checks if all azure pixel coordinates are in the same column."""
    if len(azure_coords) == 0:
        return False
    first_col = azure_coords[0][1]
    return all(j == first_col for _, j in azure_coords)

def extend_column(grid, azure_coords):
    """Extends the azure column by one pixel, respecting grid bounds."""
    output_grid = np.copy(grid)
    rows, _ = grid.shape
    col = azure_coords[0][1]  # Get the column (all are the same)
    lowest_row = max(i for i, _ in azure_coords)
    if lowest_row + 1 < rows:
        output_grid[lowest_row + 1, col] = 8
    return output_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find all azure pixels
    azure_coords = find_azure_pixels(input_grid)

    # Check for diagonal arrangement
    if is_diagonal(azure_coords):
        output_grid = move_to_main_diagonal(input_grid, azure_coords)
    # Check for single column arrangement
    elif is_single_column(azure_coords):
        output_grid = extend_column(output_grid, azure_coords)
    # Otherwise, return input unchanged

    return output_grid
```
