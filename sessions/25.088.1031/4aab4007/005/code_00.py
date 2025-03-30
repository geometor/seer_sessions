import numpy as np

"""
Transforms the input grid by filling in white (0) pixels based on a diagonal
pattern. The transformation applies to all pixels except the absolute outermost
border (row 0, H-1, col 0, W-1). The color used to fill a white pixel at (r, c)
is determined by finding the first non-white pixel along the same diagonal
(where r + c is constant) within the fillable area (rows 1 to H-2, cols 1 to W-2) 
of the *input* grid. The search for the pattern color along the diagonal 
iterates through columns first within the fillable area. Non-white pixels 
within the fillable area retain their original color.
"""

def find_color_on_diagonal(input_grid_np, r, c, fillable_min_row, fillable_max_row, fillable_min_col, fillable_max_col):
    """
    Finds the color of the first non-white pixel on the diagonal r+c=k
    by searching within the fillable area, iterating through columns first.

    Args:
        input_grid_np: The input grid as a numpy array.
        r: The row index of the target white pixel.
        c: The column index of the target white pixel.
        fillable_min_row: The minimum row index of the fillable/search area (usually 1).
        fillable_max_row: The maximum row index of the fillable/search area (usually H-2).
        fillable_min_col: The minimum column index of the fillable/search area (usually 1).
        fillable_max_col: The maximum column index of the fillable/search area (usually W-2).

    Returns:
        The color (int) found on the diagonal, or 0 (white) if none is found
        within the search area.
    """
    target_sum = r + c
    H, W = input_grid_np.shape
    
    # Iterate through possible column indices within the fillable search area
    for c_s in range(fillable_min_col, fillable_max_col + 1):
        # Calculate corresponding row index
        r_s = target_sum - c_s
        # Check if the row index is within the fillable area bounds
        if fillable_min_row <= r_s <= fillable_max_row:
            # Check if the pixel at (r_s, c_s) in the *original* input grid is not white (0)
            color = input_grid_np[r_s, c_s]
            if color != 0:
                return color  # Found the pattern color for this diagonal
                
    # If no non-white color is found on this diagonal within the search area
    # This implies the entire diagonal within the fillable area was white in the input.
    # In this specific task, it seems the expected behavior is to fill with the diagonal color,
    # so finding no color source is unexpected based on examples. Return white as default.
    return 0

def transform(input_grid):
    """
    Applies the diagonal color filling transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid_np = np.copy(input_grid_np)
    
    # Get the dimensions of the grid
    H, W = input_grid_np.shape

    # Define the boundaries of the area where pixels *can* be filled or serve as color sources
    # This excludes the absolute outermost border.
    fillable_min_row = 1
    fillable_max_row = H - 2 # Inclusive
    fillable_min_col = 1
    fillable_max_col = W - 2 # Inclusive

    # Check if grid is large enough to have a fillable area
    if fillable_max_row < fillable_min_row or fillable_max_col < fillable_min_col:
        # Grid is too small (3x3 or smaller), no transformation needed inside the border
        return input_grid # Return original grid

    # Iterate through each cell within the fillable area
    for r in range(fillable_min_row, fillable_max_row + 1):
        for c in range(fillable_min_col, fillable_max_col + 1):
            # Check if the current pixel in the *input* grid is white (color 0)
            if input_grid_np[r, c] == 0:
                # Find the appropriate color from the diagonal pattern by searching the fillable area
                fill_color = find_color_on_diagonal(
                    input_grid_np, r, c, 
                    fillable_min_row, fillable_max_row, 
                    fillable_min_col, fillable_max_col
                )
                # Update the pixel in the output grid
                output_grid_np[r, c] = fill_color
            # Else (if the pixel is not white within the fillable area), 
            # it retains its original color (already copied)

    # Convert the result back to a list of lists format
    output_grid = output_grid_np.tolist()
    
    return output_grid