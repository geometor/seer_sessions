import numpy as np

"""
Scan the input grid to find all "corner points". A corner point is a pixel at (row, col) such that its color differs from the pixel above it (row-1, col) or the pixel to its left (row, col-1). The top-left pixel (0, 0) is always considered a corner point.
Collect all unique row indices and unique column indices from these identified corner points.
Sort the unique row indices (sorted_rows) and unique column indices (sorted_cols).
Create an output grid with dimensions len(sorted_rows) x len(sorted_cols).
Populate each cell (out_r, out_c) of the output grid by sampling the color from the input grid at the corresponding corner point coordinate: input_grid[sorted_rows[out_r], sorted_cols[out_c]].
Return the fully populated output grid.
"""

def find_corner_points_indices(grid_np):
    """
    Identifies the row and column indices corresponding to "corner points".
    A corner point marks the top-left of a visually distinct block region.

    Args:
        grid_np (np.array): The input grid as a NumPy array.

    Returns:
        tuple: A tuple containing two sorted lists:
               - sorted unique row indices of corner points
               - sorted unique column indices of corner points
    """
    rows, cols = grid_np.shape
    corner_rows = {0}  # Always include the top edge
    corner_cols = {0}  # Always include the left edge

    for r in range(rows):
        for c in range(cols):
            current_color = grid_np[r, c]
            # Check change from above
            if r > 0 and grid_np[r - 1, c] != current_color:
                corner_rows.add(r)
            # Check change from left
            if c > 0 and grid_np[r, c - 1] != current_color:
                corner_cols.add(c)

    return sorted(list(corner_rows)), sorted(list(corner_cols))


def transform(input_grid):
    """
    Transforms the input grid by identifying corner points defining the block
    structure and sampling colors from these points to create a smaller output grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    if input_grid_np.size == 0:
        return [] # Handle empty input

    # 1. Scan the input grid to find corner point indices
    #    (implicitly defines the grid structure)
    sorted_rows, sorted_cols = find_corner_points_indices(input_grid_np)

    # 2. Determine the output grid dimensions
    output_rows = len(sorted_rows)
    output_cols = len(sorted_cols)

    # 3. Create the output grid (initialize with numpy for efficiency)
    #    Using the dtype from input prevents potential type issues if all colors were 0.
    output_grid_np = np.zeros((output_rows, output_cols), dtype=input_grid_np.dtype)

    # 4. Populate the output grid by sampling colors from the input grid
    #    at the identified corner point coordinates.
    for out_r in range(output_rows):
        for out_c in range(output_cols):
            # Map output grid coordinates back to input grid corner coordinates
            in_r = sorted_rows[out_r]
            in_c = sorted_cols[out_c]
            # Sample the color from the input grid
            output_grid_np[out_r, out_c] = input_grid_np[in_r, in_c]

    # 5. Convert the numpy array back to a list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid