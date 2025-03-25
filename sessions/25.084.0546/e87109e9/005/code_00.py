"""
Remove the top five rows of the input grid. Move all azure (8) pixels to the top section of the output grid, preserving their original column positions. The rest of the grid below the top five rows should remain unchanged, except for the vacated azure positions, which are implicitly filled when removing azure. Fill the remaining unused cells with white.
"""

import numpy as np

def transform(input_grid):
    rows, cols = input_grid.shape
    new_rows = rows - 5
    output_grid = np.zeros((new_rows, cols), dtype=int)

    # Preserve the lower section of the grid.
    output_grid[:new_rows, :] = input_grid[5:, :]

    # Create a temporary grid for moving azure pixels.
    temp_grid = np.zeros((rows, cols), dtype=int)

    # Move azure pixels to the top of temp_grid.
    azure_row_index = 0
    for c in range(cols):
        for r in range(rows):
            if input_grid[r, c] == 8:
                temp_grid[azure_row_index, c] = 8
                azure_row_index += 1
        azure_row_index = 0 # reset for next column.

    # Copy only the top 5 rows worth of azure blocks
    output_grid[:min(5,new_rows),:] = temp_grid[:min(5,new_rows),:]

    return output_grid