"""
1.  **Identify "seed" pixels:** Locate all pixels with color 6 (magenta) in the input grid.
2.  **Propagate Change:** Change the color of all 8s (azure) that are directly adjacent to color 6 pixels to color 7 (orange).
3. **Influence of 1's.** Some color 8's adjacent to color 1 pixels are also converted to color 7. The conversion rule in these locations depend on their relative x coordinate to the adjacent 1.
4. The color 1s (blue) stay the same except when adjacent to an 8 which gets converted to a 7 in which case the 1 also converts to a 7.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                neighbors.append((r, c))
    return neighbors

def transform(input_grid):
    # Initialize output grid with a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Change 8s adjacent to 6s to 7s
            if output_grid[row, col] == 6:
                neighbors = get_neighbors(output_grid, row, col)
                for r, c in neighbors:
                    if output_grid[r, c] == 8:
                        output_grid[r, c] = 7

    for row in range(rows):
        for col in range(cols):
            if output_grid[row,col] == 1:
                neighbors = get_neighbors(output_grid, row, col)
                for r, c in neighbors:
                    if output_grid[r,c] == 8:
                        if c < col:
                           output_grid[r,c] = 7
                        
    for row in range(rows):
        for col in range(cols):
             if input_grid[row,col] == 1:
                neighbors = get_neighbors(input_grid, row, col)
                for r, c in neighbors:
                    if input_grid[r,c] == 8 and output_grid[r,c] == 7:
                        output_grid[row,col] = 7

    return output_grid