import numpy as np

"""
Transformation Rule:
1. Initialize an output grid with the same dimensions as the input, filled with orange (7).
2. Find all red (2) pixels in the input grid. These form a diagonal segment (top-right to bottom-left).
3. Determine the length (L) of the input segment (number of red pixels).
4. Find the coordinates (r_in, c_in) of the top-rightmost red pixel (minimum row index).
5. Calculate the length of the output segment: L_out = L + 1.
6. Calculate the coordinates (r_out, c_out) for the top-rightmost pixel of the output segment:
   - r_out = r_in - (L + 1)
   - c_out = c_in + min(L + 1, 3)
7. Draw the output segment onto the output grid: Place L_out red pixels starting at (r_out, c_out) and extending diagonally down-left. The coordinates are (r_out + i, c_out - i) for i from 0 to L_out - 1.
8. Return the output grid.
"""

def find_red_pixels(grid):
    """Finds the coordinates of all red (2) pixels."""
    red_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 2:
                red_pixels.append((r, c))
    return red_pixels

def get_segment_properties(red_pixels):
    """Determines the length and top-right pixel of the segment."""
    if not red_pixels:
        return 0, (-1, -1) # No segment found

    length = len(red_pixels)
    # Sort by row (ascending), then column (descending) to find top-right
    # For a top-right to bottom-left diagonal, the min row index is sufficient
    top_right_pixel = min(red_pixels, key=lambda p: p[0])

    return length, top_right_pixel

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 7
    foreground_color = 2

    # 1. Initialize output grid
    output_grid = np.full_like(input_np, background_color)

    # 2. Find red pixels
    red_pixels = find_red_pixels(input_np)

    # 3. & 4. Determine input segment properties
    length_in, (r_in, c_in) = get_segment_properties(red_pixels)

    if length_in == 0:
        # Handle case with no red pixels if necessary, though examples always have them.
        # For now, just return the background grid.
        return output_grid.tolist()

    # 5. Calculate output segment length
    length_out = length_in + 1

    # 6. Calculate output segment top-right position
    # Note: The logic derived was r_out = r_in - (L + 1), which is r_in - length_out
    # And c_out = c_in + min(L + 1, 3), which is c_in + min(length_out, 3)
    r_out = r_in - length_out
    c_out = c_in + min(length_out, 3)

    # 7. Draw the output segment
    for i in range(length_out):
        draw_r = r_out + i
        draw_c = c_out - i
        # Check boundaries before drawing
        if 0 <= draw_r < rows and 0 <= draw_c < cols:
            output_grid[draw_r, draw_c] = foreground_color
        else:
            # Optional: Log or handle pixels outside bounds if needed
            # print(f"Warning: Calculated pixel ({draw_r}, {draw_c}) is outside grid bounds.")
            pass

    # 8. Return the output grid
    return output_grid.tolist()