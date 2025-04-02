import numpy as np

"""
Transforms an input grid based on the non-white pixels within each row, considering both row-specific and global properties.

1.  Determine the maximum column index (`max_col_overall`) containing any non-white pixel across the entire input grid. If the grid is all white, the output is also all white.
2.  Process each row independently:
    a. Find all non-white pixels within the current input row. Let their count be `count`.
    b. If `count == 0`: The corresponding output row remains all white (0).
    c. If `count == 1`:
        i. Identify the single non-white pixel's column index (`col`) and color (`C`).
        ii. Fill the corresponding output row with color `C` starting from column `col` up to and including the pre-calculated `max_col_overall`. Pixels to the left of `col` remain white.
    d. If `count > 1`:
        i. Find the leftmost non-white pixel in the row (at `min_col_row` with color `C`).
        ii. Find the rightmost non-white pixel in the row (at `max_col_row`).
        iii. Fill the corresponding output row with color `C` (the color of the leftmost pixel) from column `min_col_row` to `max_col_row` (inclusive). Pixels outside this range remain white. The `max_col_overall` is not used for filling in this case.
"""

def find_non_white_pixel_data(row):
    """
    Finds indices and colors of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a row.

    Returns:
        list: A list of tuples (column_index, color). Empty if none found.
    """
    # Helper function to identify non-white pixels and their locations/colors in a single row
    pixels = []
    for col_idx, color in enumerate(row):
        if color != 0: # 0 is the background/white color
            pixels.append((col_idx, color))
    return pixels

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input grid (list of lists) to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize the output grid with the same dimensions, filled with background color (0)
    output_array = np.zeros_like(input_array)

    # --- Global Analysis Step ---
    # Find the coordinates (row, col) of all non-white pixels in the entire grid
    non_white_coords = np.where(input_array != 0)

    # Check if there are any non-white pixels at all
    if non_white_coords[1].size == 0:
        # If the grid is entirely white, return an all-white grid of the same size
        return output_array.tolist()

    # Determine the maximum column index reached by any non-white pixel
    # non_white_coords[1] contains the column indices
    max_col_overall = non_white_coords[1].max()

    # --- Row-wise Processing Step ---
    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row from the input array
        input_row = input_array[r, :]
        # Get a reference to the corresponding row in the output array for modification
        output_row = output_array[r, :]

        # Find non-white pixel data (index, color) specifically for this row
        non_white_pixels_in_row = find_non_white_pixel_data(input_row)
        count = len(non_white_pixels_in_row)

        # --- Apply Transformation Rules Based on Pixel Count in the Row ---
        if count == 0:
            # Rule 1: No non-white pixels in this row.
            # Output row remains all zeros (as initialized).
            pass # No action needed

        elif count == 1:
            # Rule 2: Exactly one non-white pixel in this row.
            col, color = non_white_pixels_in_row[0]
            # Calculate the end index for slicing (exclusive)
            fill_end_col_global = max_col_overall + 1
            # Fill the output row from this pixel's column up to the global max column index (inclusive).
            output_row[col:fill_end_col_global] = color

        else: # count > 1
            # Rule 3: Two or more non-white pixels in this row.
            # Extract just the column indices of non-white pixels in this row
            cols_in_row = [p[0] for p in non_white_pixels_in_row]
            # Find the minimum (leftmost) and maximum (rightmost) column index for this row
            min_col_row = min(cols_in_row)
            max_col_row = max(cols_in_row)
            # Get the color of the leftmost pixel in this row
            # We can access this directly from the input row using the calculated min_col_row
            leftmost_color = input_row[min_col_row]
            # Calculate the end index for slicing (exclusive) for the row-specific range
            fill_end_col_row = max_col_row + 1
            # Fill the output row between the row-specific min and max columns (inclusive).
            output_row[min_col_row : fill_end_col_row] = leftmost_color

    # Convert the final numpy array back to a list of lists format
    return output_array.tolist()