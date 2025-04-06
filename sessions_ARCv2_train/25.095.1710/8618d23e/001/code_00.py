import numpy as np

"""
Transforms an input grid by splitting it horizontally at the middle row, 
creating a larger output grid with an extra row and column initialized with 9s, 
and placing the top half of the input in the top-left corner and the bottom half 
in the bottom-right corner (offset by one row and one column) of the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the grid transformation rule.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Determine the dimensions of the input grid
    R, C = input_array.shape
    
    # Calculate the split row index (integer division)
    split_row_index = R // 2
    
    # Define the dimensions of the output grid
    output_rows = R + 1
    output_cols = C + 1
    
    # Define the padding value
    padding_value = 9
    
    # Initialize the output grid with the padding value
    output_array = np.full((output_rows, output_cols), padding_value, dtype=int)
    
    # Copy the top part of the InputGrid to the top-left of the OutputGrid
    # Source: rows 0 to split_row_index - 1, columns 0 to C - 1
    # Target: rows 0 to split_row_index - 1, columns 0 to C - 1
    if split_row_index > 0: # Check if there is a top part to copy
        output_array[0:split_row_index, 0:C] = input_array[0:split_row_index, 0:C]
        
    # Copy the bottom part of the InputGrid to the bottom-right (offset) of the OutputGrid
    # Source: rows split_row_index to R - 1, columns 0 to C - 1
    # Target: rows split_row_index + 1 to R, columns 1 to C
    if split_row_index < R: # Check if there is a bottom part to copy
        output_array[split_row_index + 1 : R + 1, 1 : C + 1] = input_array[split_row_index : R, 0:C]

    # Convert the numpy array back to a list of lists for the return value
    output_grid = output_array.tolist()
    
    return output_grid
