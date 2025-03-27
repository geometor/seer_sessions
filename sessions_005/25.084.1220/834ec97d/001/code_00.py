import numpy as np

# COLOR_MAP = {
#     0: (238, 238, 238),  # white
#     1: (30, 147, 255),  # blue
#     2: (220, 50, 40),  # red
#     3: (79, 204, 48),  # green
#     4: (230, 200, 0),  # yellow
#     5: (85, 85, 85),  # gray
#     6: (229, 58, 163),  # magenta
#     7: (230, 120, 20),  # orange
#     8: (135, 216, 241),  # azure
#     9: (146, 18, 49),  # maroon
# }
YELLOW = 4
WHITE = 0

def find_source_pixel(grid):
    """
    Finds the first non-white pixel in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (row, col, color) of the source pixel, or (None, None, None) if not found.
    """
    non_white_pixels = np.where(grid != WHITE)
    if len(non_white_pixels[0]) > 0:
        row_s = non_white_pixels[0][0]
        col_s = non_white_pixels[1][0]
        source_color = grid[row_s, col_s]
        return row_s, col_s, source_color
    return None, None, None

def transform(input_grid):
    """
    Transforms the input grid based on the position of a single non-white source pixel.
    1. Identifies the source pixel (color, row_s, col_s).
    2. Determines the parity (even/odd) of the source pixel's column (col_s).
    3. Creates an output grid filled with white.
    4. Fills the output grid with yellow (4) in rows 0 to row_s (inclusive)
       at columns whose parity matches the source column parity.
    5. Moves the source pixel one row down (to row_s + 1, col_s) in the output grid,
       placing its original color there.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify Source
    row_s, col_s, source_color = find_source_pixel(input_np)

    # Handle case where no source pixel is found (though unlikely based on examples)
    if row_s is None:
        return input_grid # Or return an empty grid, depending on desired behavior

    # 2. Determine Column Parity
    source_col_parity = col_s % 2 # 0 for even, 1 for odd

    # 3. Initialize Output grid with white background
    output_grid = np.full((height, width), WHITE, dtype=int)

    # 4. Generate Yellow Pattern
    for r in range(row_s + 1): # Iterate rows from 0 up to and including row_s
        for c in range(width): # Iterate through all columns
            # Check if the current column's parity matches the source column's parity
            if c % 2 == source_col_parity:
                output_grid[r, c] = YELLOW

    # 5. Place Moved Source Pixel
    new_row_s = row_s + 1
    # Check if the new row is within the grid bounds
    if new_row_s < height:
        output_grid[new_row_s, col_s] = source_color

    # Return the output grid, converting back to list of lists if necessary
    # Assuming numpy array output is acceptable based on common ARC practices
    return output_grid.tolist()