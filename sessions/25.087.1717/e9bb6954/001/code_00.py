import numpy as np

"""
Transformation Rule:
1. Identify all solid 3x3 blocks of a single non-white color in the input grid.
2. For each identified 3x3 block:
   a. Determine its color (C).
   b. Find the row (R_center) and column (L_center) indices of its center pixel.
3. Create a copy of the input grid.
4. Apply column fills: For each identified block (C, R_center, L_center), fill the entire column L_center with color C, but only overwriting pixels that are currently white (0).
5. Apply row fills: For each identified block (C, R_center, L_center), fill the entire row R_center with color C, but only overwriting pixels that are currently white (0). If a pixel is at the intersection of a column fill and a row fill, the row fill color takes precedence.
"""

def find_3x3_blocks(grid):
    """
    Finds all solid 3x3 blocks of a single non-white color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (color, center_row, center_col)
              for a found 3x3 block.
    """
    blocks = []
    height, width = grid.shape
    # Iterate through possible top-left corners of 3x3 blocks
    for r in range(height - 2):
        for l in range(width - 2):
            # Extract the 3x3 subgrid
            subgrid = grid[r:r+3, l:l+3]
            
            # Get the color of the top-left pixel
            color = subgrid[0, 0]
            
            # Check if the color is non-white and if all pixels in the subgrid are the same color
            if color != 0 and np.all(subgrid == color):
                center_row = r + 1
                center_col = l + 1
                blocks.append((color, center_row, center_col))
    return blocks

def transform(input_grid):
    """
    Applies the transformation rule based on identified 3x3 blocks.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # 1. Identify all 3x3 blocks
    blocks = find_3x3_blocks(input_np)

    # 4. Apply column fills
    for color, center_row, center_col in blocks:
        for r in range(height):
            if output_grid[r, center_col] == 0: # Only overwrite white pixels
                output_grid[r, center_col] = color

    # 5. Apply row fills (overwriting column fills at intersections if necessary)
    for color, center_row, center_col in blocks:
        for l in range(width):
            if output_grid[center_row, l] == 0: # Only overwrite white pixels
                output_grid[center_row, l] = color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()