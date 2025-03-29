import numpy as np

"""
Transforms the input grid according to the following rules:
1. Identify the main color (C), which is the unique color present in the grid that is not white (0) or gray (5).
2. Find the coordinates (gr, gc) of the top-leftmost gray (5) pixel (minimum row, then minimum column).
3. Find the coordinates (mr, mc) of the top-leftmost main color (C) pixel (minimum row, then minimum column).
4. Determine a starting point (sr, sc) for a new diagonal line based on the column indices:
   - If the gray column `gc` is greater than the main color column `mc`, the start point is (0, gc).
   - Otherwise (if `gc` is less than or equal to `mc`), the start point is (gr, 0).
5. Create the output grid by first copying the input grid.
6. In the output grid, change all gray (5) pixels to white (0).
7. Starting from the determined coordinates (sr, sc), draw a diagonal line using the main color C. This line extends downwards and to the right (incrementing row and column by 1 at each step) until it goes off the grid boundary. Pixels along this line are set to color C, overwriting any existing color.
"""

def find_top_leftmost_pixel(grid, color):
    """
    Finds the (row, col) coordinates of the top-leftmost pixel of a given color.
    Searches row by row, then column by column within the first row containing the color.
    Returns None if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row = np.min(rows)
    # Find the minimum column index among pixels in the minimum row
    min_col_in_min_row = np.min(cols[rows == min_row])
    return (min_row, min_col_in_min_row)

def identify_main_color(grid):
    """
    Identifies the main color in the grid, excluding white (0) and gray (5).
    Assumes there is exactly one such color based on the task examples.
    Returns the main color value, or None if none is found.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != 5:
            return color
    return None # Should not happen based on examples

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)

    # Identify the main color (C)
    main_color = identify_main_color(input_np)
    # If no main color other than 0 or 5 is found, return the original grid unchanged.
    if main_color is None:
        # This case isn't expected based on examples, but handles potential edge cases.
        return input_grid 

    # Locate the top-leftmost gray (5) pixel
    gray_coords = find_top_leftmost_pixel(input_np, 5)
    
    # Locate the top-leftmost main color (C) pixel
    main_coords = find_top_leftmost_pixel(input_np, main_color)

    # If either gray or main color pixels are missing (not expected), return the original grid.
    if gray_coords is None or main_coords is None:
        # This signifies an input structure different from the examples.
        # A safe fallback is to return the input grid after removing gray.
        output_np[output_np == 5] = 0
        return output_np.tolist()

    gr, gc = gray_coords
    mr, mc = main_coords

    # Remove all gray pixels (change them to white) in the output grid
    output_np[output_np == 5] = 0

    # Determine the starting coordinates (sr, sc) for the new diagonal line
    if gc > mc:
        # If gray column is further right than main color column, start at top edge, gray column
        sr, sc = 0, gc
    else: # gc <= mc
        # Otherwise, start at left edge, gray row
        sr, sc = gr, 0

    # Draw the diagonal line starting from (sr, sc) using the main color C
    r, c = sr, sc
    while 0 <= r < height and 0 <= c < width:
        # Set the pixel at the current position to the main color
        output_np[r, c] = main_color
        # Move down and right for the next pixel
        r += 1
        c += 1

    # Convert the final numpy array back to a list of lists before returning
    return output_np.tolist()