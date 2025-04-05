import numpy as np

"""
Transforms an input 2D grid (with a single row) by identifying the contiguous 
block of non-zero digits within that row and shifting it to the right. The 
amount of the shift (in columns) is equal to the length (number of columns) 
of the non-zero block itself. Zeros act as placeholders.
"""

def find_non_zero_block_in_row(row_array):
    """
    Finds the start index, length, and elements of the first contiguous non-zero block in a 1D array.

    Args:
        row_array: A 1D NumPy array representing a row of digits.

    Returns:
        A tuple (start_index, length, block_elements) if a block is found.
        Returns (-1, 0, []) if no non-zero block is found.
    """
    start_index = -1
    length = 0
    block_elements = []
    n = len(row_array)

    # Find the start index of the first non-zero element
    for i in range(n):
        if row_array[i] != 0:
            start_index = i
            break

    # If no non-zero elements were found, return default values
    if start_index == -1:
        return start_index, length, block_elements

    # Find the end of the block (where it hits a zero or the end of the array)
    # and extract the block elements
    for i in range(start_index, n):
        if row_array[i] != 0:
            length += 1
            block_elements.append(row_array[i])
        else:
            # Found the end of the block (hit a zero)
            break
            
    return start_index, length, block_elements

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block-shifting transformation to the input grid.

    Args:
        input_grid: A 2D NumPy array (expected shape [1, N]) representing the sequence.

    Returns:
        A 2D NumPy array with the transformed sequence in the first row.
    """
    # Ensure input is a NumPy array and has at least one row
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim < 1 or input_grid.shape[0] == 0:
         # Handle unexpected input format if necessary, though test framework should provide correct format
         # For now, assume valid 2D input based on analysis
         raise ValueError("Input must be a non-empty 2D NumPy array")

    # Initialize output_grid with the same shape and type as input, filled with zeros
    output_grid = np.zeros_like(input_grid)
    
    # Extract the first (and only) row to operate on
    input_row = input_grid[0]
    num_cols = input_row.shape[0]

    # Find the non-zero block in the input row
    start_col_index, block_length, block_elements = find_non_zero_block_in_row(input_row)

    # If a non-zero block was found
    if start_col_index != -1:
        # Calculate the new starting column position for the block
        new_start_col_index = start_col_index + block_length
        
        # Calculate the theoretical end column index for slicing in the output grid row
        # This isn't strictly needed for slicing but helps visualize
        # new_end_col_index = new_start_col_index + block_length 

        # Check if the new starting position is within the bounds of the output grid row
        if new_start_col_index < num_cols:
             # Determine how many elements of the block can actually fit in the row
             place_length = min(block_length, num_cols - new_start_col_index)
             
             # Place the block elements (or the portion that fits) into the first row of the output grid
             # Ensure block_elements is treated as a sequence for assignment
             output_grid[0, new_start_col_index : new_start_col_index + place_length] = block_elements[:place_length]

    # Return the transformed grid
    return output_grid