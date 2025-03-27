import numpy as np

"""
Transforms an input grid into an output grid that is twice the height and twice the width, composed of four quadrants.
The transformation follows these rules:
1.  The output grid has dimensions 2H x 2W, where H and W are the height and width of the input grid.
2.  Let the input grid be 'I'. Let the color of the top-left pixel (I[0,0]) be 'fill_color'.
3.  Top-left quadrant (0:H, 0:W): This is identical to the input grid 'I'.
4.  Top-right quadrant (0:H, W:2W): This is a modified version of the input grid ('I_mod') where all white pixels (value 0) in 'I' have been replaced by 'fill_color'.
5.  Bottom-left quadrant (H:2H, 0:W): This grid ('B') is generated based on the rows of the input grid 'I':
    - For each row 'r' in 'I', find the color of the first non-white pixel encountered when scanning from left to right.
    - The corresponding row 'r' in 'B' is filled entirely with this found color.
    - If a row 'r' in 'I' consists entirely of white pixels (value 0), the corresponding row 'r' in 'B' is filled entirely with 'fill_color'.
6.  Bottom-right quadrant (H:2H, W:2W): This is identical to the top-right quadrant ('I_mod').
"""

def create_modified_grid(grid, fill_color):
    """
    Creates a copy of the input grid where all white (0) pixels are replaced
    by the specified fill_color.

    Args:
        grid (np.array): The input grid.
        fill_color (int): The color to replace white pixels with.

    Returns:
        np.array: The modified grid.
    """
    # Create a copy to avoid modifying the original grid
    modified = np.copy(grid)
    # Replace white pixels (0) with the fill_color
    modified[modified == 0] = fill_color
    return modified

def create_bottom_left_grid(grid, fill_color):
    """
    Creates the grid pattern used for the bottom-left quadrant.
    Each row is filled with the color of the first non-white pixel
    in the corresponding row of the input grid, or the fill_color
    if the input row is all white.

    Args:
        grid (np.array): The input grid.
        fill_color (int): The color to use for all-white rows.

    Returns:
        np.array: The grid for the bottom-left quadrant.
    """
    H, W = grid.shape
    # Initialize the grid for the bottom-left quadrant with the same shape as the input
    bottom_grid = np.zeros_like(grid) 

    # Iterate through each row of the input grid
    for r in range(H):
        input_row = grid[r, :]
        # Find non-white pixels in the current row
        non_white_indices = np.where(input_row != 0)[0] # Get indices of non-white pixels

        # Determine the color for the output row
        if len(non_white_indices) > 0:
            # Use the color of the first non-white pixel found (from left)
            first_non_white_index = non_white_indices[0]
            row_color = input_row[first_non_white_index]
        else:
            # If the row is all white, use the fill_color 
            row_color = fill_color

        # Fill the corresponding row in the bottom_grid entirely with the determined color
        bottom_grid[r, :] = row_color

    return bottom_grid


def transform(input_grid):
    """
    Transforms the input grid based on the quadrant rules described above.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid as a list of lists.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Determine the fill color from the top-left pixel of the input grid
    fill_color = input_np[0, 0]

    # --- Generate Quadrants ---
    
    # Top-Left Quadrant: Identical to input
    top_left_quadrant = input_np
    
    # Top-Right Quadrant: Input grid with white pixels replaced by fill_color
    # This is also used for the Bottom-Right Quadrant
    top_right_quadrant = create_modified_grid(input_np, fill_color)
    
    # Bottom-Left Quadrant: Rows filled based on the first non-white pixel in the input's corresponding row
    bottom_left_quadrant = create_bottom_left_grid(input_np, fill_color)

    # Bottom-Right Quadrant: Identical to Top-Right Quadrant
    bottom_right_quadrant = top_right_quadrant

    # --- Assemble Output Grid ---
    
    # Initialize the output grid with dimensions 2H x 2W
    output_H, output_W = 2 * H, 2 * W
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Place the top-left quadrant (0:H, 0:W)
    output_grid[0:H, 0:W] = top_left_quadrant

    # Place the top-right quadrant (0:H, W:2W)
    output_grid[0:H, W:output_W] = top_right_quadrant

    # Place the bottom-left quadrant (H:2H, 0:W)
    output_grid[H:output_H, 0:W] = bottom_left_quadrant

    # Place the bottom-right quadrant (H:2H, W:2W)
    output_grid[H:output_H, W:output_W] = bottom_right_quadrant

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()