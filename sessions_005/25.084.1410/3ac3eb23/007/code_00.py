import numpy as np

"""
Propagates initial colored pixels downwards diagonally row by row to fill the 
grid below them.

1. Create a copy of the input grid, `output_grid`.
2. Find the row index `max_r_init` of the last row containing any non-white 
   pixels in the input grid. If no such row exists, return the copy.
3. Iterate through each row `r` from `max_r_init + 1` down to the bottom 
   row (`height - 1`).
4. For each cell `(r, c)` in these rows:
   - Retrieve the colors of the two cells diagonally above it in the 
     previous row (`r-1`): `color_ul = output_grid[r-1, c-1]` and 
     `color_ur = output_grid[r-1, c+1]`. Handle boundary conditions where 
     `c-1 < 0` or `c+1 >= width` by treating the color as white (0).
   - Apply the propagation rule:
     - If `color_ul` is non-white and `color_ur` is white, set 
       `output_grid[r, c]` to `color_ul`.
     - If `color_ul` is white and `color_ur` is non-white, set 
       `output_grid[r, c]` to `color_ur`.
     - If both are non-white and `color_ul == color_ur`, set 
       `output_grid[r, c]` to `color_ul`.
     - Otherwise, `output_grid[r, c]` remains white (0).
5. Return the modified `output_grid`.
"""

def transform(input_grid):
    """
    Applies continuous diagonal color propagation downwards.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array and initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()
    height, width = grid.shape

    # --- Step 2: Find the last row with initial non-white pixels ---
    max_r_init = -1
    for r in range(height - 1, -1, -1):
        # Check if any element in the row is non-zero (not white)
        if np.any(grid[r] != 0):
            max_r_init = r
            break

    # If the grid is all white or the last colored row is the bottom row
    if max_r_init == -1 or max_r_init == height - 1:
        return output_grid # Nothing to propagate

    # --- Step 3 & 4: Iterate through rows below max_r_init and apply propagation ---
    for r in range(max_r_init + 1, height):
        for c in range(width):
            # --- Step 5 & 6: Get diagonal upper colors, handling boundaries ---
            # Get color from diagonally up-left
            color_ul = output_grid[r-1, c-1] if c > 0 else 0
            # Get color from diagonally up-right
            color_ur = output_grid[r-1, c+1] if c < width - 1 else 0

            # --- Step 7: Apply the propagation rule ---
            # Note: We assume the area below max_r_init starts as white (0)
            # in the input, so we directly assign the new color.
            if color_ul != 0 and color_ur == 0:
                output_grid[r, c] = color_ul
            elif color_ul == 0 and color_ur != 0:
                output_grid[r, c] = color_ur
            elif color_ul != 0 and color_ur != 0 and color_ul == color_ur:
                output_grid[r, c] = color_ul
            # Otherwise (both 0 or different non-zero colors), it remains 0 (white)
            # No explicit 'else' needed as output_grid[r, c] is initially 0 below max_r_init

    # --- Step 8: Return the final grid ---
    return output_grid