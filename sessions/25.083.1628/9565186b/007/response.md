```python
"""
1.  **Identify and Group Adjacent Azure Pixels:** Iterate through the input grid. When an azure (8) pixel is found, check for horizontally or vertically adjacent azure pixels. Use flood fill to identify all connected azure pixels belonging to the same group. Replace all pixels in that group with gray (5) pixels.

2.  **Handle Lone Azure Pixels:** Iterate through the input grid again. For any azure (8) pixel *not* part of an adjacent group (determined in step 1):
    *   Check if a blue (1) or green (3) pixel exists anywhere in the *same row* as the lone azure pixel. If either exists, the azure pixel remains *unchanged*.
    *   If neither a blue (1) nor a green (3) pixel exists in the same row, check if a blue (1) or green (3) pixel exists anywhere in the *same column* as the lone azure pixel. If either exists, the azure pixel remains *unchanged*.
    *   Only if *none* of the above conditions are met (no blue or green in the same row or column), replace the lone azure (8) pixel with a gray (5) pixel.

3.  **Output:** The output grid reflects these transformations, with all other pixels remaining unchanged from the input grid.
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

def flood_fill(grid, row, col, target_color, replacement_color, visited):
    """Recursively replaces connected pixels of target_color with replacement_color."""
    rows, cols = grid.shape
    if (
        row < 0
        or row >= rows
        or col < 0
        or col >= cols
        or grid[row, col] != target_color
        or visited[row,col]
    ):
        return
    visited[row,col] = True
    grid[row, col] = replacement_color
    for adj_row, adj_col in get_adjacent_pixels(grid, row, col):
        flood_fill(grid, adj_row, adj_col, target_color, replacement_color, visited)
        
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    # Iterate through each pixel, looking for azure pixels to flood_fill
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 8 and not visited[row,col]:
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                adjacent_8s = [(r,c) for r, c in adjacent_pixels if input_grid[r, c] == 8]
                
                if adjacent_8s:
                    flood_fill(output_grid, row, col, 8, 5, visited)
                    

    # Iterate for lone pixels again, using the *original* input_grid
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 8 and not visited[row,col]:
                # Check other conditions for lone 8s using input_grid
                row_values = input_grid[row, :]
                col_values = input_grid[:, col]
                if not(1 in row_values or 3 in row_values) and not(1 in col_values or 3 in col_values):
                    output_grid[row,col] = 5

    return output_grid
```