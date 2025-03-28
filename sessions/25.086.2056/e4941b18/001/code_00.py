import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return r, c
    return None # Should not happen based on task description

def find_block_boundaries(grid, color):
    """Finds the min/max row/col of a contiguous block of the specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None # Should not happen for gray block
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by repositioning a red pixel and an azure pixel
    relative to a gray rectangular block.

    1. Locates a gray rectangular block, a single red pixel, and a single azure pixel.
    2. Creates a copy of the input grid.
    3. Removes the original red and azure pixels (sets them to orange).
    4. Places the red pixel one row above the gray block, in the original column of the azure pixel.
    5. Places the azure pixel at the bottom-right corner of the gray block.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = grid_np.copy()

    # Define colors
    RED = 2
    GRAY = 5
    ORANGE = 7
    AZURE = 8

    # 1. Find the initial positions of the red and azure pixels
    red_row_in, red_col_in = find_pixel(grid_np, RED)
    azure_row_in, azure_col_in = find_pixel(grid_np, AZURE)

    # 2. Find the boundaries of the gray block
    gray_min_row, gray_max_row, gray_min_col, gray_max_col = find_block_boundaries(grid_np, GRAY)

    # 3. Remove the original red and azure pixels from the output grid (set to orange)
    output_grid[red_row_in, red_col_in] = ORANGE
    output_grid[azure_row_in, azure_col_in] = ORANGE

    # 4. Calculate the final position for the red pixel
    final_red_row = gray_min_row - 1
    final_red_col = azure_col_in 
    # Place the red pixel at its new location
    # Check bounds just in case, although examples suggest it's always valid
    if 0 <= final_red_row < output_grid.shape[0] and 0 <= final_red_col < output_grid.shape[1]:
        output_grid[final_red_row, final_red_col] = RED

    # 5. Calculate the final position for the azure pixel (bottom-right of gray block)
    final_azure_row = gray_max_row
    final_azure_col = gray_max_col
    # Place the azure pixel at its new location
    # Check bounds just in case
    if 0 <= final_azure_row < output_grid.shape[0] and 0 <= final_azure_col < output_grid.shape[1]:
        output_grid[final_azure_row, final_azure_col] = AZURE

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()