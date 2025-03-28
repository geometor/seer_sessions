import numpy as np

"""
Transformation Rule:
1. Create an output grid of the same dimensions as the input, filled with white (0).
2. Identify unique non-white colors present in the input grid's rightmost column and bottom row.
3. For each unique color C:
    a. Find the minimum and maximum row indices (min_row, max_row) where C appears in the input's rightmost column.
    b. Find the minimum and maximum column indices (min_col, max_col) where C appears in the input's bottom row.
    c. Fill the rectangular area in the output grid from (min_row, min_col) to (max_row, max_col) with color C.
4. Copy the input grid's rightmost column and bottom row to the corresponding positions in the output grid.
"""

def transform(input_grid):
    """
    Draws colored rectangles in the output based on the positions of colors
    in the input's rightmost column and bottom row.
    """
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # 1. Initialize output_grid with background color (white, 0)
    output_grid = np.zeros_like(input_np)

    # Extract border columns and rows
    right_col = input_np[:, W - 1]
    bottom_row = input_np[H - 1, :]

    # Combine border elements to find unique colors
    border_elements = np.concatenate((right_col, bottom_row))
    
    # 2. Identify unique non-white colors
    unique_colors = np.unique(border_elements)
    unique_colors = unique_colors[unique_colors != 0] # Filter out background color

    # 3. For each unique color, determine bounds and draw rectangle
    for color in unique_colors:
        # a. Find row indices for the color in the rightmost column
        row_indices = np.where(right_col == color)[0]
        # b. Find column indices for the color in the bottom row
        col_indices = np.where(bottom_row == color)[0]

        # Check if color exists in both borders (though problem implies it does)
        if len(row_indices) > 0 and len(col_indices) > 0:
            # c. Determine min/max row and column indices
            min_row = np.min(row_indices)
            max_row = np.max(row_indices)
            min_col = np.min(col_indices)
            max_col = np.max(col_indices)

            # d. Fill the rectangular area in the output grid
            output_grid[min_row : max_row + 1, min_col : max_col + 1] = color

    # 4. Copy the input grid's borders to the output grid
    # This overwrites any part of the drawn rectangles that might overlap the borders
    output_grid[:, W - 1] = right_col
    output_grid[H - 1, :] = bottom_row

    # Convert back to list of lists if necessary, but numpy array is often fine
    return output_grid.tolist()
