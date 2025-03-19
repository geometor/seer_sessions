"""
1.  **Find Last Red:** Locate the last position (row, column) of the color '2' (red) within the input grid. If it doesn't exist, the output is the same as the input.
2.  **Extend Diagonally (if Red exists):** Starting from the cell immediately below and to the right of the last red cell's position, change the color of cells to '2' (red) diagonally downwards and to the right.
3.  **Terminate at Edge:** Continue the diagonal extension until either the bottom or right edge of the grid is reached.
4. **Preservation:** All other cells that do not fall under this rule remain the same.
"""

import numpy as np

def find_last_color_position(grid, color):
    # Find the position of the last occurrence of a given color.
    last_position = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == color:
                last_position = (r, c)  # Update row and column
    return last_position  # Color not found


def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the source position of color '2' (red).
    source_position = find_last_color_position(input_grid, 2)
    
    if source_position is None:  # Handle the case where color 2 is not found
        return output_grid
    
    row, col = source_position
    row += 1
    col += 1
    
    # Replicate '2' diagonally downwards and to the right.
    while row < output_grid.shape[0] and col < output_grid.shape[1]:
        output_grid[row, col] = 2
        row += 1
        col += 1
    
    return output_grid