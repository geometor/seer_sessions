"""
Identifies horizontal line segments in the input grid. For each horizontal line, it scans the row directly above within the horizontal span of the line. If exactly one non-white 'marker' pixel is found in this scanned region, a 3-pixel high vertical line is drawn in the output grid. This vertical line uses the color of the marker pixel and is centered horizontally at the midpoint of the original horizontal line, and vertically centered on the row of the original horizontal line. The original marker pixel's location is set to white (background color 0) in the output. All other pixels from the input are preserved unless overwritten.
"""

import numpy as np

def find_unique_marker(grid, row_to_scan, start_col, end_col):
    """
    Scans a specific segment of a row for a unique non-white marker pixel.

    Args:
        grid (np.array): The input grid.
        row_to_scan (int): The row index to scan.
        start_col (int): The starting column index (inclusive) for the scan.
        end_col (int): The ending column index (inclusive) for the scan.

    Returns:
        dict or None: A dictionary {'color': color, 'pos': (row, col)} if exactly
                      one non-white pixel is found, otherwise None.
    """
    height, width = grid.shape
    if row_to_scan < 0 or row_to_scan >= height:
        return None # Row is out of bounds

    found_marker = None
    count = 0

    for c in range(start_col, end_col + 1):
        if c < 0 or c >= width: # Ensure column is within bounds
             continue
        pixel_color = grid[row_to_scan, c]
        if pixel_color != 0: # Found a non-white pixel
            count += 1
            if count > 1:
                return None # Found more than one marker
            found_marker = {'color': pixel_color, 'pos': (row_to_scan, c)}

    return found_marker # Returns the marker info if count is 1, or None if count is 0 or >1

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Iterate through each pixel to find potential starts of horizontal lines
    for r in range(height):
        c = 0
        while c < width:
            # Check if this pixel is the start of a horizontal line
            # Condition: Pixel is not white AND (it's the first column OR the pixel to the left is white)
            if input_array[r, c] != 0 and (c == 0 or input_array[r, c-1] == 0):
                line_color = input_array[r, c]
                start_col = c
                end_col = start_col

                # Find the end of the horizontal line
                while end_col + 1 < width and input_array[r, end_col + 1] == line_color:
                    end_col += 1

                # --- Transformation Logic ---
                # Look for a unique marker in the row above, within the line's span
                unique_marker = find_unique_marker(input_array, r - 1, start_col, end_col)

                # If a unique marker was found, apply the transformation
                if unique_marker is not None:
                    marker_color = unique_marker['color']
                    marker_pos = unique_marker['pos']

                    # Calculate the midpoint column
                    mid_col = (start_col + end_col) // 2

                    # 1. Erase the original marker in the output
                    output_array[marker_pos] = 0

                    # 2. Draw the 3-pixel vertical line in the output grid
                    # Pixel above the line's row
                    if r - 1 >= 0 and 0 <= mid_col < width:
                         output_array[r - 1, mid_col] = marker_color
                    # Pixel on the line's row (overwriting part of the original line)
                    if 0 <= mid_col < width:
                        output_array[r, mid_col] = marker_color
                    # Pixel below the line's row
                    if r + 1 < height and 0 <= mid_col < width:
                         output_array[r + 1, mid_col] = marker_color

                # Move past the detected line to avoid re-processing its pixels
                c = end_col + 1
            else:
                # Move to the next pixel if not the start of a line
                c += 1

    # Convert the output numpy array back to a list of lists
    return output_array.tolist()