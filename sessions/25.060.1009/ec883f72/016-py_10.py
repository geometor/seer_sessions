"""
1.  **Identify Original Azure Shape:** Find all pixels with the color azure (8). This constitutes the "original azure shape".
2.  **Translate Azure Shape:** Copy the original azure shape one row down. This is the "translated azure shape."
3.  **Identify Columns:** Find all columns that contain either:
    *   Any pixel of the *original* azure shape.
    *   Any pre-existing magenta pixels
4. **Preserve original magenta:** original magenta pixels are not changed.
5.  **Create Magenta Lines:** For each identified column:
    *   Starting Point: If the column is from the original azure, the magenta line starts one row below the lowest row of the *original* azure shape within that column. If the column contains an original magenta pixel, the magenta line starts at that pixel.
    *   Ending Point: The line extends downwards to the bottom-most non-white pixel *in that specific column*. If no non-white pixel is found below the starting point, the line extends to the bottom of the grid.
6.  **Output:** The output grid consists of the translated azure shape, the newly created magenta lines, and all other pixels from the input grid unchanged, including the *original* magenta pixels.
"""

import numpy as np

def find_azure_shape(grid):
    """Finds the coordinates of all azure (8) pixels."""
    return np.argwhere(grid == 8)

def translate_shape(coords, rows_to_move, grid_shape):
    """Translates a set of coordinates down by a specified number of rows, respecting grid boundaries."""
    translated_coords = []
    for r, c in coords:
        new_r = r + rows_to_move
        if 0 <= new_r < grid_shape[0]:  # Check row boundary
            translated_coords.append((new_r, c))
    return np.array(translated_coords)

def find_columns(grid):
    """Finds all columns containing azure (8) or magenta (6) pixels."""
    azure_cols = set(np.argwhere(grid == 8)[:, 1])
    magenta_cols = set(np.argwhere(grid == 6)[:, 1])
    return sorted(list(azure_cols.union(magenta_cols)))

def find_lowest_non_white_per_column(grid, column):
    """Finds the lowest row index that contains a non-white pixel within a specific column."""
    rows = grid.shape[0]
    for r in range(rows - 1, -1, -1):
        if grid[r, column] != 0:
            return r
    return rows - 1  # If no non-white, return the last row

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Original Azure Shape
    azure_coords = find_azure_shape(input_grid)

    # 2. Translate Azure Shape
    translated_azure_coords = translate_shape(azure_coords, 1, input_grid.shape)
    for r, c in translated_azure_coords:
        output_grid[r, c] = 8

    # 3. Identify Columns
    relevant_columns = find_columns(input_grid)

    # 4. & 5. Create Magenta Lines (including preservation of original magenta)
    for col in relevant_columns:
        # Determine starting row for magenta line
        if col in [c for _, c in azure_coords]:  # Column contains part of the original azure shape
            min_azure_row_in_col = min([r for r, c in azure_coords if c == col])
            start_row = min_azure_row_in_col + 1
        else:  # Assuming the only other option is that the column had a pre-existing magenta
            start_row = min([r for r,c in np.argwhere(input_grid == 6) if c==col])

        # Determine ending row for magenta line
        end_row = find_lowest_non_white_per_column(input_grid, col)

        # Draw the magenta line
        for row_index in range(start_row, end_row + 1):
            if output_grid[row_index, col] != 6:
                output_grid[row_index, col] = 6

    # 6. Output (already handled by the above steps)
    return output_grid