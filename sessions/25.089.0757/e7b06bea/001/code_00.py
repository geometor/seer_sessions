import numpy as np

"""
Transforms the input grid based on the following rules:
1. Identify a contiguous block of vertical lines (columns) towards the right side of the input grid. 
   These lines consist of colors other than white (0) and gray (5).
2. Create an output grid of the same dimensions as the input, initialized to white (0).
3. Copy the first column (index 0) from the input grid to the first column of the output grid.
4. Determine the starting column index (`start_col`) and the number of columns (`N`) of the identified block in the input grid.
5. Calculate the target column index in the output grid as `target_col = start_col - 1`.
6. Populate the `target_col` in the output grid by interleaving the colors from the input block's columns. 
   For each row `r`, the color placed at `output_grid[r, target_col]` is taken from the input grid at `input_grid[r, start_col + (r mod N)]`.
7. All other cells in the output grid remain white (0), except for the copied first column and the newly created interleaved column.
"""

def find_color_block(grid):
    """
    Finds the start column and width of the contiguous block of non-white, non-gray columns.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (start_col, width) or (None, None) if no block is found.
    """
    height, width = grid.shape
    start_col = -1
    block_width = 0

    for c in range(1, width): # Start searching from column 1
        column = grid[:, c]
        # Check if the column contains any color other than white (0) or gray (5)
        is_block_column = np.any((column != 0) & (column != 5))

        if is_block_column:
            if start_col == -1:
                start_col = c # Found the start of the block
            block_width += 1
        elif start_col != -1:
            # Block ended
            break
            
    if start_col != -1:
        return start_col, block_width
    else:
        return None, None # No block found (excluding column 0)

def transform(input_grid):
    """
    Applies the interleaving transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np)

    # Copy the first column (index 0) from input to output
    if width > 0:
        output_grid[:, 0] = input_np[:, 0]

    # Find the contiguous block of non-white, non-gray columns
    start_col, N = find_color_block(input_np)

    # If no block is found, return the output grid with only column 0 copied
    if start_col is None:
        # This case shouldn't happen based on examples, but good to handle
        return output_grid.tolist() 

    # Calculate the target column in the output grid
    target_col = start_col - 1

    # Check if target_col is valid (should be >= 0)
    if target_col < 0:
        # This would indicate the block started at column 1, which means target is 0.
        # We need to overwrite column 0 in this specific case if it wasn't gray.
        # However, the examples show the target column is always >= 1.
        # If target_col was 0, the copy operation above might be partially or fully overwritten.
        # Let's assume target_col >= 1 based on observed patterns.
        # If an example violates this, the logic might need adjustment.
        pass # Continue assuming target_col >= 1 or potentially 0 if start_col is 1

    if target_col >= 0 : # Ensure we don't write to negative index
        # Interleave the colors into the target column
        for r in range(height):
            # Determine the source column index within the block
            block_col_index = r % N
            # Calculate the actual source column index in the input grid
            input_source_col = start_col + block_col_index
            
            # Get the color from the input grid
            color = input_np[r, input_source_col]
            
            # Place the color in the output grid's target column
            output_grid[r, target_col] = color

    # Convert the result back to a list of lists
    return output_grid.tolist()