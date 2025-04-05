import numpy as np

"""
Transforms a 12-element sequence by finding the single contiguous block of 
identical non-zero digits and shifting this block exactly 4 positions to the 
right. Handles input that might be a 1D list, a list containing one 1D list, 
or a 2D numpy array (shape 1x12). The output is always a 1D list of 12 
integers with the shifted block and zeros elsewhere.
"""

def standardize_input(input_grid, expected_length=12):
    """
    Standardizes the input to ensure it's a 1D list of the expected length.
    Handles nested lists and numpy arrays (shape 1xN).

    Args:
        input_grid: The input data (list, list of lists, numpy array).
        expected_length: The expected length of the 1D sequence.

    Returns:
        A 1D list of the expected length, or None if standardization fails.
    """
    processed_list = None

    # Check if input is a numpy array
    if isinstance(input_grid, np.ndarray):
        # If it's 2D with shape (1, N), extract the first row
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
            processed_list = input_grid[0].tolist()
        # If it's 1D, convert directly
        elif input_grid.ndim == 1:
            processed_list = input_grid.tolist()
            
    # Check if input is a list
    elif isinstance(input_grid, list):
        # Check if it's a list containing a single list (e.g., [[...]])
        if len(input_grid) == 1 and isinstance(input_grid[0], list):
             processed_list = input_grid[0]
        # Check if it's already a flat list
        elif all(isinstance(item, (int, np.integer)) for item in input_grid): # Check if elements are numbers
             processed_list = input_grid

    # Validate the length of the processed list
    if processed_list is not None and len(processed_list) == expected_length:
        return processed_list
    else:
        # print(f"Warning: Input could not be standardized to a 1D list of length {expected_length}. Input: {input_grid}")
        return None # Indicate failure


def find_non_zero_block(input_list):
    """
    Helper function to find the first contiguous block of identical non-zero digits.

    Args:
        input_list: The 1D list of integers to search within.

    Returns:
        A tuple (block_val, start_index, block_length) if a block is found,
        otherwise (None, -1, 0). Returns (None, -1, 0) if input_list is None.
    """
    if input_list is None:
        return None, -1, 0
        
    start_index = -1
    block_val = 0
    block_length = 0
    n = len(input_list)

    # Search for the start of the first non-zero sequence
    for i in range(n):
        if input_list[i] != 0:
            start_index = i
            block_val = input_list[i]
            block_length = 1
            # Continue checking for the same value to find the length/end of the block
            for j in range(i + 1, n):
                if input_list[j] == block_val:
                    block_length += 1
                else:
                    # Block ends here as the value changed or became zero
                    break
            # Found the first block, so we can stop the outer search
            break 
            
    if start_index != -1:
        # A block was found
        return block_val, start_index, block_length
    else:
        # No non-zero block found in the input list
        return None, -1, 0


def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid after standardization.

    Args:
        input_grid: A sequence (list, nested list, or numpy array) representing 12 integers.

    Returns:
        A list of 12 integers representing the transformed grid, or a list of 12 zeros if input is invalid or contains no block.
    """
    
    # Define fixed parameters for the transformation
    sequence_length = 12
    shift_distance = 4

    # Step 1: Standardize the input to get a 1D list of 12 integers
    standardized_list = standardize_input(input_grid, sequence_length)

    # Initialize the output_grid with zeros. This will be the default return if input is bad or no block is found.
    output_grid = [0] * sequence_length

    # Proceed only if standardization was successful
    if standardized_list is not None:
        
        # Step 2: Find the non-zero block in the standardized list
        block_val, start_index, block_length = find_non_zero_block(standardized_list)

        # Step 3: If a block was found, calculate its new position and place it
        if block_val is not None: # Checks if find_non_zero_block returned valid data
            
            # Calculate the new starting index after shifting right
            new_start_index = start_index + shift_distance
            
            # Place the block's value into the output grid at the new position
            for i in range(block_length):
                # Calculate the target index for the current element of the block
                target_index = new_start_index + i
                
                # Ensure the placement is within the bounds of the output grid
                if 0 <= target_index < sequence_length:
                     output_grid[target_index] = block_val
                # else: # Handle cases where block shifts out of bounds (not observed in examples)
                    # pass 

    # Step 4: Return the resulting output grid
    return output_grid