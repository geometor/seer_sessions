import numpy as np

"""
Processes each row of the input grid independently. 
Looks for specific pairs of colors within a row: Yellow(4)/Orange(7) and Blue(1)/Azure(8).
If exactly one pixel of each color in a pair exists in the row, and all pixels strictly between them are white(0), then a transformation occurs:
1. Identify the pixel on the left and the pixel on the right within the pair.
2. The pixel that was originally on the right moves to the position immediately to the right of the left pixel.
3. The original position of the moved pixel becomes white(0).
4. The pixel that was originally on the left remains in its position.
Pixels not involved in such qualifying pairs, or rows not meeting the conditions, remain unchanged.
"""

def find_pixel_indices(row_data, color_value):
    """Finds the column indices of pixels with a specific color in a row."""
    return np.where(row_data == color_value)[0]

def check_clear_path(row_data, col1, col2):
    """Checks if all pixels strictly between col1 and col2 are white(0)."""
    start = min(col1, col2) + 1
    end = max(col1, col2)
    # If columns are adjacent, the path is clear (slice is empty)
    if start >= end:
        return True
    # Check if all values in the slice are 0
    return np.all(row_data[start:end] == 0)

def transform(input_grid):
    """
    Applies the row-based pixel pair transformation.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Work on a copy to avoid modifying the original during iteration
    height, width = grid.shape

    # Iterate through each row
    for r in range(height):
        row_data = output_grid[r, :]

        # --- Check for Yellow(4) and Orange(7) pair ---
        indices_4 = find_pixel_indices(row_data, 4)
        indices_7 = find_pixel_indices(row_data, 7)

        # Check if exactly one of each color exists
        if len(indices_4) == 1 and len(indices_7) == 1:
            col_4 = indices_4[0]
            col_7 = indices_7[0]

            # Check if the path between them is clear (only white pixels)
            if check_clear_path(row_data, col_4, col_7):
                # Determine which is left and which is right
                col_left, val_left = (col_4, 4) if col_4 < col_7 else (col_7, 7)
                col_right, val_right = (col_7, 7) if col_4 < col_7 else (col_4, 4)
                
                # Move the right pixel next to the left pixel
                # Ensure the target position is within bounds (should be, as col_right > col_left)
                if col_left + 1 < width:
                    output_grid[r, col_right] = 0       # Clear original position of the moved pixel
                    output_grid[r, col_left + 1] = val_right # Place the moved pixel

        # --- Check for Blue(1) and Azure(8) pair ---
        indices_1 = find_pixel_indices(row_data, 1)
        indices_8 = find_pixel_indices(row_data, 8)

        # Check if exactly one of each color exists
        if len(indices_1) == 1 and len(indices_8) == 1:
            col_1 = indices_1[0]
            col_8 = indices_8[0]

            # Check if the path between them is clear (only white pixels)
            if check_clear_path(row_data, col_1, col_8):
                # Determine which is left and which is right
                col_left, val_left = (col_1, 1) if col_1 < col_8 else (col_8, 8)
                col_right, val_right = (col_8, 8) if col_1 < col_8 else (col_1, 1)
                
                # Move the right pixel next to the left pixel
                # Ensure the target position is within bounds (should be, as col_right > col_left)
                if col_left + 1 < width:
                     output_grid[r, col_right] = 0      # Clear original position of the moved pixel
                     output_grid[r, col_left + 1] = val_right # Place the moved pixel

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
