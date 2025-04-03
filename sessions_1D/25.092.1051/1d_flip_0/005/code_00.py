import numpy as np
import copy

"""
Transforms the input grid by identifying a single contiguous horizontal block of 
non-zero pixels within the first row, performing a cyclic left shift on the 
pixels within that block, and returning the modified grid. The background (zero pixels) 
and the grid dimensions remain unchanged. Assumes input is a NumPy array with shape (1, N).
"""

def find_non_background_block(row):
    """
    Finds the start and end indices of the first contiguous block of non-zero pixels 
    in a 1D NumPy array.

    Args:
        row (np.ndarray): A 1D NumPy array representing a row of the grid.

    Returns:
        tuple: A tuple containing the start index and end index (inclusive) of the block.
               Returns (-1, -1) if no non-zero block is found.
    """
    non_zero_indices = np.where(row != 0)[0] # Find indices of all non-zero elements
    
    if non_zero_indices.size == 0:
        return -1, -1 # No non-zero elements found

    start_index = non_zero_indices[0]
    end_index = start_index
    
    # Iterate from the second potential element in the block
    for i in range(1, non_zero_indices.size):
        # Check if the current non-zero index is consecutive to the previous one
        if non_zero_indices[i] == non_zero_indices[i-1] + 1:
            end_index = non_zero_indices[i] # Extend the block
        else:
            # Found a gap, the first contiguous block ends here
            break
            
    return start_index, end_index

def cyclic_left_shift(sequence):
    """
    Performs a cyclic left shift on a list or 1D NumPy array. Moves the first element to the end.

    Args:
        sequence (list | np.ndarray): The sequence (list or 1D array) to be shifted.

    Returns:
        list: The cyclically left-shifted sequence as a list. Returns the original 
              sequence as a list if it has 0 or 1 elements.
    """
    # Convert numpy array to list for easier manipulation
    if isinstance(sequence, np.ndarray):
        seq_list = sequence.tolist()
    else:
        seq_list = list(sequence) # Ensure it's a list if it wasn't an ndarray

    if not seq_list or len(seq_list) <= 1:
        return seq_list # Return as list
        
    # Perform the cyclic shift using list slicing and concatenation
    shifted_list = seq_list[1:] + [seq_list[0]]
    return shifted_list

def transform(input_grid):
    """
    Transforms the input grid by finding a contiguous block of non-zero pixels
    in the single row and performing a cyclic left shift on the pixels within that block.

    Args:
        input_grid (np.ndarray): A 1xN NumPy array grid.

    Returns:
        np.ndarray: The transformed 1xN grid.
    """
    # Ensure input is a numpy array and has at least one row
    if not isinstance(input_grid, np.ndarray) or input_grid.shape[0] == 0:
        # Or handle error appropriately
        return copy.deepcopy(input_grid) if isinstance(input_grid, np.ndarray) else np.array([]) 

    # Create a copy of the input grid to modify for the output
    output_grid = np.copy(input_grid)
    
    # Extract the first (and only expected) row
    # Need to handle potential empty row case if shape is (1,0)
    if input_grid.shape[1] == 0:
        return output_grid # Return copy of empty grid
        
    input_row = input_grid[0]

    # Find the contiguous block of non-background (non-zero) pixels in the row
    start_index, end_index = find_non_background_block(input_row)

    # Check if a valid block was found
    if start_index != -1:
        # Extract the block sequence from the original row
        # Slicing is [start:end+1] for inclusive end index
        block_sequence = input_row[start_index : end_index + 1] 

        # Perform the cyclic left shift on the extracted sequence
        # cyclic_left_shift returns a list
        shifted_sequence = cyclic_left_shift(block_sequence) 

        # Replace the corresponding segment in the output grid's row 
        # NumPy slicing allows assignment from a list of the correct length
        output_grid[0, start_index : end_index + 1] = shifted_sequence

    # Return the modified output grid
    return output_grid