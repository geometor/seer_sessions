import numpy as np

"""
Transforms an input grid into an output grid that is twice the height and twice the width, composed of four quadrants.
1.  The top-left quadrant is identical to the input grid.
2.  The top-right quadrant is a copy of the input grid where all white pixels (0) have been replaced by the color of the input grid's top-left pixel (fill_color).
3.  The bottom-left and bottom-right quadrants are identical. They are generated row by row based on the input grid:
    - For each row in the input grid, find the first non-white pixel from the left.
    - Fill the corresponding row in the bottom quadrants entirely with this color.
    - If a row in the input grid contains only white pixels, fill the corresponding row in the bottom quadrants with the fill_color (the color of the input grid's top-left pixel).
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
    bottom_grid = np.zeros_like(grid) # Initialize with same shape and type

    # Iterate through each row of the input grid
    for r in range(H):
        input_row = grid[r, :]
        # Find non-white pixels in the current row
        non_white_pixels = input_row[input_row != 0]

        # Determine the color for the output row
        if len(non_white_pixels) > 0:
            # Use the first non-white pixel's color
            row_color = non_white_pixels[0]
        else:
            # Use the fill_color if the row is all white
            row_color = fill_color

        # Fill the corresponding row in the bottom_grid
        bottom_grid[r, :] = row_color

    return bottom_grid


def transform(input_grid):
    """
    Transforms the input grid based on the quadrant rules described above.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Determine the fill color from the top-left pixel
    fill_color = input_np[0, 0]

    # Create the modified grid for the top-right quadrant
    modified_grid = create_modified_grid(input_np, fill_color)

    # Create the grid pattern for the bottom two quadrants
    bottom_grid = create_bottom_grid(input_np, fill_color)

    # Initialize the output grid with dimensions 2H x 2W
    output_H, output_W = 2 * H, 2 * W
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Place the original input grid in the top-left quadrant
    output_grid[0:H, 0:W] = input_np

    # Place the modified grid in the top-right quadrant
    output_grid[0:H, W:output_W] = modified_grid

    # Place the bottom pattern grid in the bottom-left quadrant
    output_grid[H:output_H, 0:W] = bottom_grid

    # Place the bottom pattern grid in the bottom-right quadrant
    output_grid[H:output_H, W:output_W] = bottom_grid

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()