"""
1.  **Background Change:** Change all black (0) pixels in the input to green (3) pixels in the output.
2.  **Preserve Outline:** Keep all azure (8) pixels in the input unchanged in the output.
3.  **Fill Enclosed Areas:** Identify any areas of black (0) that are completely enclosed by azure (8) pixels. Change these enclosed black (0) pixels to red (2) pixels in the output.
"""

import numpy as np

def flood_fill(grid, start_row, start_col, target_color, replacement_color):
    """
    Performs a flood fill operation on the grid.
    """
    if grid[start_row, start_col] != target_color:
        return

    rows, cols = grid.shape
    queue = [(start_row, start_col)]
    grid[start_row, start_col] = replacement_color

    while queue:
        row, col = queue.pop(0)

        neighbors = [
            (row - 1, col),  # Up
            (row + 1, col),  # Down
            (row, col - 1),  # Left
            (row, col + 1)   # Right
        ]

        for n_row, n_col in neighbors:
            if 0 <= n_row < rows and 0 <= n_col < cols and grid[n_row, n_col] == target_color:
                grid[n_row, n_col] = replacement_color
                queue.append((n_row, n_col))
                
def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # 1. Change all black (0) pixels to green (3)
    output_grid[output_grid == 0] = 3

    # 2. Preserve azure (8) pixels (already done by copying)

    # 3. Fill Enclosed Areas
    rows, cols = output_grid.shape
    # Find a seed point that's green (3, was 0 in input) *outside* the azure shape
    # This assumes the top-left corner is always outside.
    # and will be part of the background
    
    # First, temporarily set all 0s to 3s to do the flood fill of the background.
    temp_grid = np.copy(input_grid)
    flood_fill(temp_grid, 0, 0, 0, 3)

    # Now, identify remaining 0s in temp_grid (those inside the shape)
    # And change them to 2 in the output_grid
    for r in range(rows):
      for c in range(cols):
        if temp_grid[r,c] == 0:
          output_grid[r,c] = 2
    

    return output_grid