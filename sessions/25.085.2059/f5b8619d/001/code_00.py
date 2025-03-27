import numpy as np

"""
Transforms an input grid by first creating a 'unit pattern' grid of the same dimensions. 
In the unit pattern, non-white pixels from the input are copied directly. 
White pixels (0) in the input are changed to azure (8) in the unit pattern if they are adjacent (horizontally, vertically, or diagonally) to any non-white pixel in the input grid; otherwise, they remain white. 
Finally, the output grid is constructed by tiling this unit pattern 2x2, resulting in a grid twice the height and twice the width of the input.
"""

def has_non_white_neighbor(grid, r, c, H, W):
    """
    Checks if the cell at (r, c) in the grid has any non-white (non-zero) neighbors
    within the 8 adjacent cells (including diagonals).

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        H (int): Height of the grid.
        W (int): Width of the grid.

    Returns:
        bool: True if a non-white neighbor exists, False otherwise.
    """
    for dr in range(-1, 2):  # Iterate through row offsets (-1, 0, 1)
        for dc in range(-1, 2):  # Iterate through column offsets (-1, 0, 1)
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself

            nr, nc = r + dr, c + dc # Neighbor coordinates

            # Check if the neighbor is within grid bounds
            if 0 <= nr < H and 0 <= nc < W:
                # Check if the neighbor is non-white
                if grid[nr, nc] != 0:
                    return True
    return False

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape

    # Create the unit pattern grid, initialized with zeros
    unit_pattern = np.zeros_like(input_array)

    # Iterate through each pixel in the input grid to create the unit pattern
    for r in range(H):
        for c in range(W):
            input_color = input_array[r, c]
            
            # If the input pixel is non-white, copy it directly
            if input_color != 0:
                unit_pattern[r, c] = input_color
            # If the input pixel is white (0)
            else:
                # Check for adjacent non-white pixels in the *input* grid
                if has_non_white_neighbor(input_array, r, c, H, W):
                    # If adjacent to non-white, set unit pattern pixel to azure (8)
                    unit_pattern[r, c] = 8
                else:
                    # Otherwise, keep it white (0) - already initialized to 0
                    pass # unit_pattern[r, c] = 0 (already 0)

    # Create the final output grid with dimensions 2*H x 2*W
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # Tile the unit pattern into the four quadrants of the output grid
    output_grid[0:H, 0:W] = unit_pattern       # Top-left
    output_grid[0:H, W:2*W] = unit_pattern    # Top-right
    output_grid[H:2*H, 0:W] = unit_pattern    # Bottom-left
    output_grid[H:2*H, W:2*W] = unit_pattern  # Bottom-right

    return output_grid.tolist() # Return as list of lists as per common ARC format