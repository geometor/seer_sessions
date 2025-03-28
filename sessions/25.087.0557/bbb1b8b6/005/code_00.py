import numpy as np

"""
Identifies two 4x4 subgrids (L and R) in the 4x9 input grid, separated by a gray column.
Counts non-white pixels in each subgrid (count_l, count_r).
Determines the output 4x4 grid based on the comparison of count_l and count_r and the colors in R:

1. If count_r > count_l:
    a. If count_r - count_l == 1: Output is L.
    b. If count_r - count_l > 1: Output is overlay(L, R) (start with L, paint non-white R pixels).
2. If count_l == count_r:
    a. Output is overlay(R, L) (start with R, paint non-white L pixels).
3. If count_l > count_r:
    a. Get unique non-white colors in R.
    b. If unique non-white colors in R is exactly {Red (2)} or exactly {Green (3)}: Output is L.
    c. Otherwise: Output is overlay(R, L) (start with R, paint non-white L pixels).
"""

def count_non_white_pixels(grid):
    """Counts the number of pixels in the grid that are not white (value 0)."""
    # Ensure input is a NumPy array for efficient computation
    grid_np = np.array(grid, dtype=int)
    return np.sum(grid_np != 0)

def overlay(base_grid, top_grid):
    """
    Overlays the top_grid onto the base_grid. Non-white pixels from top_grid
    replace corresponding pixels in a copy of the base_grid.
    """
    # Ensure inputs are numpy arrays
    base_np = np.array(base_grid, dtype=int)
    top_np = np.array(top_grid, dtype=int)

    # Create a copy of the base grid to modify
    result_grid = base_np.copy()

    # Apply the overlay logic: where top_np is not 0, update result_grid
    non_white_mask = top_np != 0
    result_grid[non_white_mask] = top_np[non_white_mask]

    return result_grid # Return as numpy array for intermediate use

def get_unique_non_white_colors(grid):
    """Returns a set of unique non-white color values present in the grid."""
    grid_np = np.array(grid, dtype=int)
    non_white_pixels = grid_np[grid_np != 0]
    return set(np.unique(non_white_pixels))

def transform(input_grid):
    """
    Transforms the input 4x9 grid based on comparing non-white pixel counts
    of its left and right 4x4 subgrids and applying conditional overlay/selection rules.

    Args:
        input_grid (list[list[int]]): A 4x9 list of lists representing the input grid.

    Returns:
        list[list[int]]: A 4x4 list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_grid_np = np.array(input_grid, dtype=int)

    # 1. & 2. Define the left subgrid (L) (columns 0 through 3)
    left_subgrid = input_grid_np[:, 0:4]

    # 3. & 4. Define the right subgrid (R) (columns 5 through 8)
    right_subgrid = input_grid_np[:, 5:9]

    # 5. Count non-white pixels in the left subgrid
    count_l = count_non_white_pixels(left_subgrid)

    # 6. Count non-white pixels in the right subgrid
    count_r = count_non_white_pixels(right_subgrid)

    # Initialize output grid variable
    output_grid_np = None

    # 7. Compare counts and apply transformation rules
    if count_r > count_l:
        # 7a. If count_r > count_l
        difference = count_r - count_l
        if difference == 1:
            # 7ai. If difference is 1: Output is L
            output_grid_np = left_subgrid
        else: # difference > 1
            # 7aii. If difference > 1: Output is overlay(L, R)
            # Start with L as base, overlay non-white pixels from R
            output_grid_np = overlay(left_subgrid, right_subgrid)

    elif count_l == count_r:
        # 7b. If count_l == count_r: Output is overlay(R, L)
        # Start with R as base, overlay non-white pixels from L
        output_grid_np = overlay(right_subgrid, left_subgrid)

    else: # count_l > count_r
        # 7c. If count_l > count_r
        # 7ci. Find the set of unique non-white colors present in R
        unique_colors_r = get_unique_non_white_colors(right_subgrid)

        # 7cii. Check if the set is exactly {2} (Red) or {3} (Green)
        if unique_colors_r == {2} or unique_colors_r == {3}:
            # If yes: Output is L
            output_grid_np = left_subgrid
        else:
            # 7ciii. Otherwise: Output is overlay(R, L)
            # Start with R as base, overlay non-white pixels from L
            output_grid_np = overlay(right_subgrid, left_subgrid)

    # 8. Return the resulting 4x4 grid as a list of lists
    return output_grid_np.tolist()