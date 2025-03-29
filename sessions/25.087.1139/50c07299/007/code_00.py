import numpy as np

"""
Transformation Rule:
1. Find the diagonal segment of red (2) pixels in the input grid. This segment runs from top-right to bottom-left.
2. Determine the length (L_in) of the input segment.
3. Identify the coordinates (r_in, c_in) of the top-rightmost pixel of the input segment (the pixel with the minimum row index).
4. Calculate the length of the output segment: L_out = L_in + 1.
5. Calculate the coordinates (r_out, c_out) for the top-rightmost pixel of the output segment using the following formulas:
   - r_out = r_in - L_out
   - c_out = c_in + min(L_out, 3) 
   (The column offset is capped at 3).
6. Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color, orange (7).
7. Draw the output segment onto the output grid based on its length (L_out):
   - If L_out is 4: Starting from (r_out, c_out), place L_out red pixels using relative coordinates (r_out + i, c_out - max(0, i - 1)) for i from 0 to L_out - 1.
   - Otherwise (L_out is 2 or 3): Starting from (r_out, c_out), place L_out red pixels using relative coordinates (r_out + i, c_out - i) for i from 0 to L_out - 1.
   - Ensure pixel coordinates are within the grid boundaries before drawing.
8. Return the final output grid.
"""

def find_colored_pixels(grid, color):
    """
    Finds the coordinates of all pixels of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of (row, column) tuples for pixels matching the color.
    """
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                pixels.append((r, c))
    return pixels

def get_segment_properties(pixels):
    """
    Determines the length and top-right pixel of a diagonal segment.
    Assumes pixels form a top-right to bottom-left diagonal segment.

    Args:
        pixels (list): A list of (row, column) coordinates of the segment pixels.

    Returns:
        tuple: A tuple containing (length, (top_right_row, top_right_col)).
               Returns (0, (-1, -1)) if no pixels are provided.
    """
    if not pixels:
        return 0, (-1, -1) # No segment found

    length = len(pixels)
    # For a top-right to bottom-left diagonal, the pixel with the minimum row index
    # is the top-rightmost one (and also has the maximum column index among segment pixels).
    top_right_pixel = min(pixels, key=lambda p: p[0])

    return length, top_right_pixel

def transform(input_grid):
    """
    Applies the transformation rule to the input grid. Finds a red diagonal segment,
    increases its length by one, calculates a new top-right starting position,
    and draws the new segment on an orange background using a drawing rule
    that depends on the output segment's length.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Define colors
    background_color = 7 # orange
    foreground_color = 2 # red

    # 1. Find red pixels (input segment)
    red_pixels = find_colored_pixels(input_np, foreground_color)

    # 2. & 3. Determine input segment properties
    length_in, (r_in, c_in) = get_segment_properties(red_pixels)

    # Handle case where no red segment is found (return a grid filled with background)
    if length_in == 0:
        return np.full_like(input_np, background_color).tolist()

    # 4. Calculate output segment length
    length_out = length_in + 1

    # 5. Calculate output segment top-right position
    # The row position moves up by the length of the *output* segment.
    r_out = r_in - length_out
    # The column position moves right by the length of the *output* segment, but capped at 3.
    c_out = c_in + min(length_out, 3)

    # 6. Initialize output grid with the background color
    output_grid = np.full_like(input_np, background_color)

    # 7. Draw the output segment based on its length
    for i in range(length_out):
        draw_r = r_out + i
        
        # Determine the column offset based on the output length L_out
        if length_out == 4:
            # Special drawing rule for length 4
            col_offset = max(0, i - 1) 
        else:
            # Standard diagonal drawing rule for length 2 or 3
            col_offset = i
            
        draw_c = c_out - col_offset
            
        # Check grid boundaries before drawing the pixel
        if 0 <= draw_r < rows and 0 <= draw_c < cols:
            output_grid[draw_r, draw_c] = foreground_color

    # 8. Return the output grid as a list of lists
    return output_grid.tolist()