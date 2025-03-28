import numpy as np

def find_pixel(grid, color):
    """
    Finds the coordinates (row, col) of the first pixel with the specified color.
    Returns coordinates as plain integers or None if not found.
    """
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        # Return as plain integers
        return int(coords[0, 0]), int(coords[0, 1])
    return None

def find_block_boundaries(grid, color):
    """
    Finds the min/max row/col of a contiguous block of the specified color.
    Returns boundaries as plain integers (min_r, max_r, min_c, max_c) or None if not found.
    """
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    # Return as plain integers
    min_row = int(np.min(coords[:, 0]))
    max_row = int(np.max(coords[:, 0]))
    min_col = int(np.min(coords[:, 1]))
    max_col = int(np.max(coords[:, 1]))
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by repositioning a single red pixel (2) and a single azure pixel (8)
    relative to a gray (5) rectangular block, based on their initial positions and the block's boundaries.
    The original locations of the red and azure pixels are changed to the background color (orange, 7).

    1. Find initial positions of red (2) and azure (8) pixels.
    2. Find boundaries of the gray (5) block.
    3. Create a copy of the input grid for output.
    4. Set original red/azure locations to orange (7) in the output.
    5. Calculate final red position: row = gray_min_row - 1, col = azure_col_in.
    6. Calculate final azure position: row = gray_max_row. Column depends on whether azure_col_in < red_col_in.
       If true: col = azure_row_in.
       If false: col = gray_max_col + 1.
    7. Place red and azure pixels at their final positions in the output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Create a copy of the input grid to serve as the output grid
    output_grid = grid_np.copy()

    # Define colors
    RED = 2
    GRAY = 5
    ORANGE = 7
    AZURE = 8

    # 1. Find the initial positions of the red and azure pixels
    red_pos_in = find_pixel(grid_np, RED)
    azure_pos_in = find_pixel(grid_np, AZURE)

    # Handle cases where pixels might not be found
    if red_pos_in is None or azure_pos_in is None:
        print("Error: Red or Azure pixel not found.")
        return input_grid # Return original grid if key pixels are missing
    red_row_in, red_col_in = red_pos_in
    azure_row_in, azure_col_in = azure_pos_in

    # 2. Find the boundaries of the gray block
    gray_bounds = find_block_boundaries(grid_np, GRAY)
    if gray_bounds is None:
        print("Error: Gray block not found.")
        return input_grid # Return original grid if gray block is missing
    gray_min_row, gray_max_row, gray_min_col, gray_max_col = gray_bounds

    # 4. Set the original locations of red and azure pixels to orange
    # Check bounds just in case initial pixels are somehow outside
    if 0 <= red_row_in < height and 0 <= red_col_in < width:
      output_grid[red_row_in, red_col_in] = ORANGE
    if 0 <= azure_row_in < height and 0 <= azure_col_in < width:
      output_grid[azure_row_in, azure_col_in] = ORANGE

    # 5. Calculate the final position for the red pixel
    final_red_row = gray_min_row - 1
    final_red_col = azure_col_in
    # Place the red pixel at its new location, checking bounds
    if 0 <= final_red_row < height and 0 <= final_red_col < width:
        output_grid[final_red_row, final_red_col] = RED
    else:
        print(f"Warning: Final red position ({final_red_row}, {final_red_col}) is out of bounds.")


    # 6. Calculate the final position for the azure pixel
    final_azure_row = gray_max_row
    # Determine the final azure column based on the refined condition
    if azure_col_in < red_col_in:
        final_azure_col = azure_row_in # Use initial azure row as the column index
    else: # azure_col_in >= red_col_in
        final_azure_col = gray_max_col + 1 # Use column right of gray block

    # Place the azure pixel at its new location, checking bounds
    if 0 <= final_azure_row < height and 0 <= final_azure_col < width:
        output_grid[final_azure_row, final_azure_col] = AZURE
    else:
        print(f"Warning: Final azure position ({final_azure_row}, {final_azure_col}) is out of bounds.")

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()