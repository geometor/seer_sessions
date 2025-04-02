"""
Fill the horizontal gap between pairs of same-colored pixels in each row.

1. Initialize the output grid as a copy of the input grid.
2. For each row in the input grid:
    a. Find all non-white pixels in the current row, noting their colors and column indices.
    b. Check if there are exactly two non-white pixels found in this row.
    c. Check if these two non-white pixels have the same color.
    d. If both conditions (exactly two pixels, same color) are true:
        i. Identify the color of these two pixels (`fill_color`).
        ii. Identify the column index of the leftmost pixel (`col_start`).
        iii. Identify the column index of the rightmost pixel (`col_end`).
        iv. In the output grid, for the current row, set the color of all pixels 
           from `col_start` to `col_end` (inclusive) to `fill_color`.
3. Return the completed output grid.
"""

import numpy as np

def find_non_white_pixels(row):
    """Finds non-white pixels (value != 0) in a row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        list: A list of tuples, where each tuple contains (color, column_index).
              Returns an empty list if no non-white pixels are found.
    """
    non_white_pixels = []
    for col_index, pixel_color in enumerate(row):
        if pixel_color != 0:
            non_white_pixels.append((pixel_color, col_index))
    return non_white_pixels

def transform(input_grid):
    """
    Fills the horizontal segment between pairs of same-colored pixels in each row.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    num_rows, _ = input_np.shape

    # Iterate through each row
    for r_idx in range(num_rows):
        current_row = input_np[r_idx, :]
        
        # Find all non-white pixels in the current row
        non_white_pixels = find_non_white_pixels(current_row)
        
        # Check if there are exactly two non-white pixels
        if len(non_white_pixels) == 2:
            pixel1_color, pixel1_col = non_white_pixels[0]
            pixel2_color, pixel2_col = non_white_pixels[1]
            
            # Check if these two non-white pixels have the same color
            if pixel1_color == pixel2_color:
                # Identify the fill color
                fill_color = pixel1_color
                
                # Identify the start and end columns for filling
                col_start = min(pixel1_col, pixel2_col)
                col_end = max(pixel1_col, pixel2_col)
                
                # In the output grid, for the current row, set the color of all pixels
                # from col_start to col_end (inclusive) to fill_color.
                output_grid[r_idx, col_start : col_end + 1] = fill_color
                
    # No changes needed for rows that don't meet the criteria, 
    # as the output_grid was initialized as a copy.

    return output_grid.tolist() # Return as list of lists per ARC standard