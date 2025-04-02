import numpy as np

"""
Processes each row of the input grid independently based on the non-white pixels within that row.

Transformation rules:
1. If a row contains no non-white pixels (only white, 0), the output row remains unchanged (all white).
2. If a row contains exactly one non-white pixel:
   - Identify its color (C) and column index (Col).
   - Fill the corresponding output row with color C from column Col to the rightmost edge of the grid.
   - Pixels to the left of Col remain white (0).
3. If a row contains two or more non-white pixels:
   - Find the leftmost non-white pixel (at MinCol with color C) and the rightmost non-white pixel (at MaxCol).
   - Fill the corresponding output row with color C (the color of the leftmost pixel) from column MinCol to MaxCol (inclusive).
   - Pixels outside this range [MinCol, MaxCol] remain white (0).
"""

def find_non_white_pixels(row):
    """
    Finds the indices and colors of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        list: A list of tuples, where each tuple is (column_index, color).
              Returns an empty list if no non-white pixels are found.
    """
    pixels = []
    for col_idx, color in enumerate(row):
        if color != 0:
            pixels.append((col_idx, color))
    return pixels

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid (list or np.ndarray): A 2D list or numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize output grid with the background color (white, 0)
    output_array = np.zeros_like(input_array)

    # Process each row independently
    for r in range(num_rows):
        input_row = input_array[r, :]
        output_row = output_array[r, :] # Get a reference to the output row for modification

        # Find non-white pixels in the current input row
        non_white_pixels = find_non_white_pixels(input_row)
        count = len(non_white_pixels)

        # Apply transformation rules based on the count of non-white pixels
        if count == 0:
            # Rule 1: No non-white pixels, row remains white (already initialized)
            pass
        elif count == 1:
            # Rule 2: Exactly one non-white pixel
            col, color = non_white_pixels[0]
            # Fill from the pixel's column to the end of the row
            output_row[col:] = color
        else: # count > 1
            # Rule 3: Two or more non-white pixels
            # Find leftmost and rightmost pixel indices
            min_col = min(p[0] for p in non_white_pixels)
            max_col = max(p[0] for p in non_white_pixels)
            # Get the color of the leftmost pixel
            leftmost_color = input_row[min_col]
            # Fill between min_col and max_col (inclusive) with the leftmost color
            output_row[min_col:max_col + 1] = leftmost_color

    return output_array.tolist() # Return as list of lists to match ARC format if needed