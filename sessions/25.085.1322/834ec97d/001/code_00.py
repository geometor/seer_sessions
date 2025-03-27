"""
Identify the single non-white pixel in the input grid. Record its color and its location (input row `r`, input column `c`).
Create a new output grid with the same dimensions as the input grid, initially filled entirely with white (0).
Determine the starting color for an alternating pattern: if the input column `c` is even, the pattern starts with yellow (4); if `c` is odd, the pattern starts with white (0).
Fill each row `i` of the output grid, from row 0 up to and including the input row `r`, with the alternating pattern determined in step 3 (e.g., `4 0 4 0...` or `0 4 0 4...`).
Place the original non-white pixel (identified in step 1) into the output grid at location (`r + 1`, `c`), overwriting the pixel currently at that position. This step should only be performed if `r + 1` is a valid row index within the grid boundaries.
"""

import numpy as np

def find_single_object(grid):
    """Finds the first non-zero pixel in the grid."""
    non_zero_coords = np.argwhere(grid != 0)
    if len(non_zero_coords) == 0:
        return None, -1, -1  # No object found
    r, c = non_zero_coords[0]
    color = grid[r, c]
    return color, r, c

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify the single non-white pixel
    object_color, r_in, c_in = find_single_object(input_grid_np)

    # Handle case where no object is found (though unlikely based on examples)
    if object_color is None:
        return input_grid # Or return an empty grid, depending on desired behavior

    # 2. Create a new output grid, initialized with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # 3. Determine the starting color for the pattern
    pattern_start_color = 4 if c_in % 2 == 0 else 0

    # 4. Fill rows 0 to r_in with the alternating pattern
    for r in range(r_in + 1):
        for c in range(width):
            # Determine color based on column index and starting color
            if (c % 2 == 0 and pattern_start_color == 4) or \
               (c % 2 != 0 and pattern_start_color == 0):
                output_grid[r, c] = 4
            else:
                output_grid[r, c] = 0 # This is technically redundant due to initialization

    # 5. Place the original object one row down, if within bounds
    r_out = r_in + 1
    c_out = c_in
    if 0 <= r_out < height: # Check if the new row is valid
        output_grid[r_out, c_out] = object_color

    return output_grid.tolist()