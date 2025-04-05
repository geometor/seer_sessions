"""
Identifies the single contiguous rectangular block of a non-zero digit in the 2D 
input NumPy array (input_grid). Creates a new grid of the same shape and dtype, 
initialized with zeros. Places the identified block into the new grid, shifted 
by (0 rows, -3 columns) relative to its input position, ensuring the starting 
column is not less than 0. Returns the transformed grid (output_grid).
"""

import numpy as np

def find_non_zero_block_info(grid: np.ndarray):
    """
    Finds the properties of the first contiguous rectangular block of 
    non-zero digits in a 2D grid.

    Args:
        grid: The 2D NumPy array to search within.

    Returns:
        A dictionary containing block properties:
        'value': The non-zero digit value.
        'row': The starting row index (top).
        'col': The starting column index (left).
        'height': The height of the block.
        'width': The width of the block.
        Returns None if no non-zero block is found.
    """
    # Find coordinates of all non-zero elements
    non_zeros = np.argwhere(grid != 0)
    
    # Handle empty grid or grid with only zeros
    if non_zeros.size == 0:
        return None

    # Determine the bounding box of the non-zero elements
    min_row, min_col = non_zeros.min(axis=0)
    max_row, max_col = non_zeros.max(axis=0)
    
    # Extract block properties
    value = grid[min_row, min_col] # Value from top-left corner
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    return {'value': value, 'row': min_row, 'col': min_col, 'height': height, 'width': width}

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by shifting the non-zero block left by 3 columns.

    Args:
        input_grid: The 2D NumPy array containing the input grid.

    Returns:
        A new 2D NumPy array representing the transformed grid.
    """
    # 1. Determine the shape and data type of the input_grid.
    shape = input_grid.shape
    dtype = input_grid.dtype

    # 2. Create a new 2D NumPy array (output_grid) with the same shape and 
    #    data type as input_grid, initialized entirely with zeros.
    output_grid = np.zeros(shape, dtype=dtype)

    # 3. Identify the location, size, and value of the non-zero block.
    block_info = find_non_zero_block_info(input_grid)

    # 4. If a block was found, calculate its new position and place it.
    if block_info:
        r_in = block_info['row']
        c_in = block_info['col']
        h = block_info['height']
        w = block_info['width']
        v = block_info['value']

        # 5. Calculate the target top-left row (r_out) and column (c_out).
        #    Row remains the same. Column is shifted left by 3, clamped at 0.
        r_out = r_in
        c_out = max(0, c_in - 3)

        # 6. Copy the identified block into the output_grid at the new location.
        #    Ensure slicing doesn't go out of bounds (though width/height 
        #    should be preserved, the shifted column might affect this).
        #    Recalculate end indices based on clamped start and original dimensions.
        end_row = r_out + h
        end_col = c_out + w
        
        # Ensure slice indices stay within grid bounds
        actual_end_row = min(shape[0], end_row)
        actual_end_col = min(shape[1], end_col)
        
        # Extract the original block (or the part that fits if shifted off-edge)
        # This assumes the block itself doesn't change shape/content.
        # We just need its value to fill the target area.
        output_grid[r_out:actual_end_row, c_out:actual_end_col] = v 

    # 7. Return the output_grid.
    return output_grid