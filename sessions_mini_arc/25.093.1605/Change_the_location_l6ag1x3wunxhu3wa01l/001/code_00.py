"""
Transforms an input grid by rearranging its columns. 
The central column remains fixed. 
The columns to the left of the center are swapped with the columns to the right of the center, preserving the internal order within each block.
For a grid with N columns:
- Columns from index N//2 + 1 to N-1 move to indices 0 to N//2 - 1.
- Column at index N//2 stays at index N//2.
- Columns from index 0 to N//2 - 1 move to indices N//2 + 1 to N-1.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the column swapping transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert the input list of lists to a NumPy array for easier column manipulation
    input_array = np.array(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = input_array.shape
    
    # Create an empty output array with the same dimensions
    output_array = np.zeros_like(input_array)
    
    # Calculate the index of the middle column
    middle_col_index = cols // 2
    
    # Define the indices for the left and right blocks of columns
    # Left block: columns from index 0 up to (but not including) the middle column
    left_block_indices = slice(0, middle_col_index)
    # Right block: columns from the one after the middle column to the end
    right_block_indices = slice(middle_col_index + 1, cols)
    
    # Perform the column assignments according to the transformation rule
    
    # 1. Copy the right block of the input to the left block of the output
    output_array[:, left_block_indices] = input_array[:, right_block_indices]
    
    # 2. Copy the middle column from input to output
    output_array[:, middle_col_index] = input_array[:, middle_col_index]
    
    # 3. Copy the left block of the input to the right block of the output
    output_array[:, right_block_indices] = input_array[:, left_block_indices]

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
