import numpy as np

"""
Transforms the input grid by identifying a contiguous block of pixels (not background/white 0 or boundary/red 2) and moving it horizontally so its right edge is adjacent to the left side of the single boundary pixel (red, color 2). The original position of the block is filled with the background color (white, color 0). Assumes the input is a 1D grid (1 row).
"""

# Define background and boundary colors
BACKGROUND_COLOR = 0
BOUNDARY_COLOR = 2

def find_boundary_column(grid):
    """
    Finds the column index of the boundary pixel (color 2).
    Assumes exactly one boundary pixel exists and the grid is 1D.
    """
    # grid is expected to be a numpy array here
    rows, cols = grid.shape
    for c in range(cols):
        # Since it's 1D, we only check the first row (row 0)
        if grid[0, c] == BOUNDARY_COLOR:
            return c
    return None # Should not happen based on task description

def find_movable_block(grid):
    """
    Finds the first contiguous block of pixels that are not background (0) or boundary (2).
    Returns the block's color, start column, end column, and length.
    Assumes a 1D grid (1 row) and exactly one such block exists.
    """
    # grid is expected to be a numpy array here
    row = grid[0]
    cols = len(row)
    block_color = None
    start_col = -1
    end_col = -1

    for c in range(cols):
        color = row[c]
        is_block_pixel = (color != BACKGROUND_COLOR and color != BOUNDARY_COLOR)

        if is_block_pixel and start_col == -1:
            # Start of a potential block
            block_color = color
            start_col = c
        elif start_col != -1:
            # Inside a potential block or just ended one
            if not is_block_pixel or color != block_color:
                 # Block ended at the previous column
                 end_col = c - 1
                 break # Found the first block, stop searching

    # Check if the block extends to the very end of the row
    if start_col != -1 and end_col == -1:
        # Check if the last pixel was part of the block
        if row[cols-1] != BACKGROUND_COLOR and row[cols-1] != BOUNDARY_COLOR and row[cols-1] == block_color:
             end_col = cols - 1

    if start_col != -1 and end_col != -1:
        length = end_col - start_col + 1
        return block_color, start_col, end_col, length
    else:
        # No movable block found
        return None, -1, -1, 0


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Ensure grid is 1D (has only 1 row) - defensive check
    if grid.shape[0] != 1:
        # This logic is specifically for 1D grids based on examples
        # Returning original grid if assumption is violated
        print("Warning: Input grid is not 1D. Returning original grid.")
        return input_grid

    # Initialize output_grid as a copy of the input
    output_grid = grid.copy()

    # 1. Find the boundary pixel's column
    boundary_col = find_boundary_column(grid)
    if boundary_col is None:
        # Handle case where boundary pixel isn't found (shouldn't happen)
        print("Warning: Boundary pixel (2) not found. Returning original grid.")
        return input_grid # Or raise an error

    # 2. Find the movable block details
    block_color, input_start_col, input_end_col, block_length = find_movable_block(grid)

    if block_color is None:
        # Handle case where no movable block is found (shouldn't happen)
        print("Warning: Movable block not found. Returning original grid.")
        return input_grid # Or raise an error

    # 3. Erase the block from its original position in the output grid
    # Slicing works on the single row (row 0)
    output_grid[0, input_start_col : input_end_col + 1] = BACKGROUND_COLOR

    # 4. Calculate the target position for the block
    target_end_col = boundary_col - 1
    target_start_col = target_end_col - block_length + 1

    # 5. Draw the block in its new position in the output grid
    # Add boundary checks just in case calculation leads to out-of-bounds
    grid_width = grid.shape[1]
    if target_start_col >= 0 and target_end_col < grid_width:
        # Slicing assigns the block color to the target range in the single row
        output_grid[0, target_start_col : target_end_col + 1] = block_color
    else:
        # Log if the calculated position is invalid
        print(f"Warning: Calculated target position [{target_start_col}, {target_end_col}] is out of bounds for grid width {grid_width}.")
        # Depending on requirements, might need different error handling

    # Convert the numpy array back to a list of lists for the required output format
    return output_grid.tolist()