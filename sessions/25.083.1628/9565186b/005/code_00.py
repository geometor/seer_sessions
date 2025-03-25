"""
1.  **Identify and Group Adjacent Azure Pixels:** Traverse the input grid. If an azure (8) pixel is found, check for *horizontally or vertically* adjacent azure pixels. Use flood fill to replace all connected azure pixels in a group with gray (5). Mark these pixels as visited.

2.  **Handle Lone Azure Pixels:** For any azure (8) pixel that is *not* part of an adjacent group (i.e., not visited in step 1):
    *   Check if there is a blue (1) or green (3) pixel *anywhere in the same row*. If there is, change the azure pixel to gray (5).
    *   If there is *not* a blue(1) or green(3) pixel in the same row, then check the column.
    *   If there is a blue (1) or a green (3) pixel anywhere in the same column as the lone azure pixel, the azure pixel *does not* change.
    *   If none of the above conditions are met, replace the lonely azure (8) pixel with a gray (5).

3.  **Output:** Create the output grid based on the above transformations, leaving all other pixels unchanged.
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
                    

    # Iterate for lone pixels again, now that visited has been updated
    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 8 and not visited[row,col]:
                # Check other conditions for lone 8s
                row_values = input_grid[row, :]
                col_values = input_grid[:, col]
                if 1 in row_values or 3 in row_values:
                     output_grid[row, col] = 5
                elif not(1 in col_values or 3 in col_values):
                     output_grid[row,col] = 5

    return output_grid