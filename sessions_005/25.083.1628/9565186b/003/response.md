```python
"""
1.  **Identify Azure Pixels:** Iterate through each pixel in the input grid, looking for azure (8) pixels.

2.  **Check for Horizontal or Vertical Adjacency:**
    *   If an azure (8) pixel is found, check if it's *horizontally or vertically* adjacent to *another* azure (8) pixel.
    *   If two or more azure pixels are adjacent, replace *all* connected azure pixels in the group with gray (5).

3.  **Lone Azure Pixel Checks (if not part of an adjacent group):**
    *   If an azure (8) pixel is *not* adjacent to any other azure pixels (horizontally or vertically):
        *   **Row Check:** If there's a blue (1) or green (3) pixel *anywhere in the same row* as the lone azure pixel, change the azure pixel to gray (5).
        *   **Column Check:** If there's a blue (1) or a green (3) pixel *anywhere in the same column* as the lone azure pixel, the azure pixel does *not* change.
        *   **Otherwise**: If none of the above conditions are met, replace the lonely azure (8) pixel with a gray (5).

4.  **Output:** Create a new output grid with all the modifications, keeping all other pixels the same as the input.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of horizontally and vertically adjacent pixels."""
    adjacent = []
    rows, cols = grid.shape
    if row > 0:
        adjacent.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent.append((row + 1, col))  # Down
    if col > 0:
        adjacent.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent.append((row, col + 1))  # Right
    return adjacent

def flood_fill(grid, row, col, target_color, replacement_color):
    """Recursively replaces connected pixels of target_color with replacement_color."""
    rows, cols = grid.shape
    if (
        row < 0
        or row >= rows
        or col < 0
        or col >= cols
        or grid[row, col] != target_color
    ):
        return
    grid[row, col] = replacement_color
    for adj_row, adj_col in get_adjacent_pixels(grid, row, col):
        flood_fill(grid, adj_row, adj_col, target_color, replacement_color)
        
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check for 8s
            if input_grid[row, col] == 8 and not visited[row,col]:
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                adjacent_8s = [(r,c) for r, c in adjacent_pixels if input_grid[r, c] == 8]
                
                # Conditional Replacement - flood fill for adjacent 8s
                if adjacent_8s:
                    flood_fill(output_grid, row, col, 8, 5)
                    for r,c in adjacent_8s:
                      visited[r,c] = True
                    visited[row,col] = True #mark as visited
                else:
                    # Check other conditions for lone 8s
                    row_values = input_grid[row, :]
                    col_values = input_grid[:, col]
                    visited[row,col] = True
                    if 1 in row_values or 3 in row_values:
                         output_grid[row, col] = 5
                    elif not(1 in col_values or 3 in col_values):
                         output_grid[row,col] = 5

    return output_grid
```