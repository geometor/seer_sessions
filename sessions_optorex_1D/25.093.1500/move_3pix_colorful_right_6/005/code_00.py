import numpy as np

"""
Transforms an input grid (list of lists or 2D NumPy array) by identifying a 
contiguous vertical block of rows containing at least one non-zero element. 
This block is then shifted downwards by 3 rows within a new grid of the same 
dimensions. Rows outside the shifted block are filled with zeros. If the shifted 
block extends beyond the grid boundaries, it is truncated. If no non-zero 
elements are found in any row, the output grid remains filled with zeros.
"""

def _find_non_zero_row_indices(grid):
    """
    Finds the start and end row indices of the first contiguous block of 
    rows containing at least one non-zero element.

    Args:
        grid: A NumPy array representing the input grid.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no 
        non-zero rows are found.
    """
    first_nz_row_index = None
    last_nz_row_index = None
    # Iterate through each row index
    for i in range(grid.shape[0]):
        row = grid[i, :]
        # Check if any element in the row is non-zero
        if np.any(row != 0):
            # If this is the first non-zero row found, record its index
            if first_nz_row_index is None:
                first_nz_row_index = i
            # Always update the last non-zero row index found
            last_nz_row_index = i
            
    # Return the found indices (or None if none were found)
    return first_nz_row_index, last_nz_row_index

def transform(input_grid):
    """
    Applies the row-block shifting transformation to the input grid.

    Args:
        input_grid: A list of lists or a 2D NumPy array representing the grid.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Convert input to NumPy array for consistent handling and array operations
    input_grid_np = np.array(input_grid)
    
    # Get grid dimensions (rows N, columns M)
    if input_grid_np.ndim == 1:
        # Handle case where input might be flattened but represents rows of size 1
        num_rows = input_grid_np.shape[0]
        num_cols = 1
        # Reshape into N x 1 explicitly for consistent indexing
        input_grid_np = input_grid_np.reshape((num_rows, num_cols))
    elif input_grid_np.ndim == 2:
        num_rows, num_cols = input_grid_np.shape
    else:
        # Handle unexpected dimensions if necessary, though examples suggest 2D
        raise ValueError("Input grid must be interpretable as 2D.")

    # Initialize output_grid with zeros, same dimensions as input
    output_grid = np.zeros_like(input_grid_np)

    # Find the start and end indices of the non-zero row block
    first_nz_row_index, last_nz_row_index = _find_non_zero_row_indices(input_grid_np)

    # Check if a non-zero row block was actually found
    if first_nz_row_index is not None:
        # Extract the block of rows using NumPy slicing
        # Note: slicing is exclusive of the end index, so add 1
        non_zero_row_block = input_grid_np[first_nz_row_index : last_nz_row_index + 1, :]

        # Calculate the new starting row index for the block (shift down by 3)
        new_start_row_index = first_nz_row_index + 3
        
        # Determine the number of rows in the extracted block
        block_height = non_zero_row_block.shape[0]
        
        # Calculate the index where the placement would end
        end_placement_index = new_start_row_index + block_height

        # Determine how many rows from the block can actually be placed
        # without going out of bounds of the output grid.
        rows_to_place = block_height
        if end_placement_index > num_rows:
            # If the block overflows, calculate how many rows fit
            rows_to_place = num_rows - new_start_row_index
            # If the adjusted count is negative (start index out of bounds), set to 0
            if rows_to_place < 0:
                rows_to_place = 0
        
        # Slice the block if it needs truncation
        truncated_block = non_zero_row_block[:rows_to_place, :]

        # Place the block (or the truncated portion) into the output grid
        # Ensure the new start index is within the grid bounds and there are rows to place
        if new_start_row_index < num_rows and rows_to_place > 0:
            output_grid[new_start_row_index : new_start_row_index + rows_to_place, :] = truncated_block

    # Return the constructed output grid
    return output_grid