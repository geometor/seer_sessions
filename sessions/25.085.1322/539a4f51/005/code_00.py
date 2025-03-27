import numpy as np

"""
Transforms an input grid into an output grid that is twice the height and twice the width, composed of four quadrants.
The transformation follows these rules:
1.  The top-left quadrant of the output grid is identical to the input grid.
2.  The top-right quadrant is a copy of the input grid where all white pixels (value 0) have been replaced by the color of the input grid's top-left pixel (fill_color).
3.  The bottom-left and bottom-right quadrants are identical. They are generated based on the rows of the input grid:
    - For each row in the input grid, find the color of the first non-white pixel encountered when scanning from left to right.
    - The corresponding row in both bottom quadrants is filled entirely with this found color.
    - If a row in the input grid consists entirely of white pixels, the corresponding row in the bottom quadrants is filled entirely with the fill_color (the color of the input grid's top-left pixel).
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

def create_bottom_grid(grid, fill_color):
    """
    Creates the grid pattern used for the bottom two quadrants.
    Each row is filled with the color of the first non-white pixel
    in the corresponding row of the input grid, or the fill_color
    if the input row is all white.

    Args:
        grid (np.array): The input grid.
        fill_color (int): The color to use for all-white rows.

    Returns:
        np.array: The grid for the bottom quadrants.
    """
    H, W = grid.shape
    # Initialize the grid for the bottom quadrants with the same shape as the input
    bottom_grid = np.zeros_like(grid) 

    # Iterate through each row of the input grid
    for r in range(H):
        input_row = grid[r, :]
        # Find non-white pixels in the current row
        non_white_pixels = input_row[input_row != 0]

        # Determine the color for the output row
        if len(non_white_pixels) > 0:
            # Use the color of the first non-white pixel found (from left)
            row_color = non_white_pixels[0]
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

    # Generate the grid for the top-right quadrant
    # This is a copy of the input with white pixels replaced by fill_color
    top_right_quadrant = create_modified_grid(input_np, fill_color)

    # Generate the grid pattern used for both bottom quadrants
    # Each row is filled based on the first non-white pixel in the input's corresponding row
    bottom_quadrant_pattern = create_bottom_grid(input_np, fill_color)

    # Initialize the output grid with dimensions 2H x 2W
    output_H, output_W = 2 * H, 2 * W
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Place the original input grid in the top-left quadrant (0:H, 0:W)
    output_grid[0:H, 0:W] = input_np

    # Place the modified grid in the top-right quadrant (0:H, W:2W)
    output_grid[0:H, W:output_W] = top_right_quadrant

    # Place the bottom pattern grid in the bottom-left quadrant (H:2H, 0:W)
    output_grid[H:output_H, 0:W] = bottom_quadrant_pattern

    # Place the same bottom pattern grid in the bottom-right quadrant (H:2H, W:2W)
    output_grid[H:output_H, W:output_W] = bottom_quadrant_pattern

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()