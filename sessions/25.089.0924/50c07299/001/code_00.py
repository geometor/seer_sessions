import numpy as np

"""
Transformation Rule:
1. Identify the connected group of red (2) pixels in the input grid, which forms a diagonal line segment sloping down and to the left.
2. Determine the length of this segment (`L_in`) by counting the red pixels.
3. Find the coordinates `(r_in, c_in)` of the top-right pixel of the segment (minimum row index, maximum column index).
4. Calculate a displacement value `k = L_in + 1`.
5. Calculate the starting coordinates `(r_out, c_out)` for the output segment: `r_out = r_in - k`, `c_out = c_in + k`.
6. Determine the length of the output segment: `L_out = L_in + 1`.
7. Create an output grid of the same dimensions as the input, filled with the background color, orange (7).
8. Draw the new red segment of length `L_out` onto the output grid, starting at `(r_out, c_out)` and extending diagonally down and to the left. The pixels colored are `(r_out + i, c_out - i)` for `i` from 0 to `L_out - 1`.
"""

def find_red_segment_properties(grid):
    """
    Finds the red (2) pixels, calculates the segment length, 
    and identifies the top-right pixel coordinates.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (length, top_right_row, top_right_col) or (0, -1, -1) if no red pixels.
    """
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return 0, -1, -1 # No red segment found

    length = len(red_pixels)
    
    # Find the top-right pixel (min row, max col)
    min_row = np.min(red_pixels[:, 0])
    # Filter pixels in the minimum row
    top_pixels = red_pixels[red_pixels[:, 0] == min_row]
    # Find the maximum column among those top pixels
    max_col = np.max(top_pixels[:, 1])
    top_right_row = min_row
    top_right_col = max_col
    
    return length, top_right_row, top_right_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): The input 2D array representing the grid.

    Returns:
        np.ndarray: The transformed 2D array representing the output grid.
    """
    # Find properties of the red segment in the input grid
    L_in, r_in, c_in = find_red_segment_properties(input_grid)

    # Handle case where no red segment is found (though not expected based on examples)
    if L_in == 0:
        return np.copy(input_grid) # Or return an empty grid/error, depending on desired behavior

    # Calculate displacement and new segment properties
    k = L_in + 1
    r_out = r_in - k
    c_out = c_in + k
    L_out = L_in + 1

    # Initialize the output grid with the background color (orange, 7)
    output_grid = np.full_like(input_grid, 7)
    
    # Get grid dimensions for boundary checks (optional but good practice)
    height, width = output_grid.shape

    # Draw the new red segment
    for i in range(L_out):
        row_idx = r_out + i
        col_idx = c_out - i
        # Check if the pixel coordinates are within the grid boundaries
        if 0 <= row_idx < height and 0 <= col_idx < width:
            output_grid[row_idx, col_idx] = 2 # Set pixel to red
        # else: # Handle out-of-bounds pixels if necessary, e.g., log a warning or stop
        #     print(f"Warning: Calculated pixel ({row_idx}, {col_idx}) is out of bounds.")
            
    return output_grid