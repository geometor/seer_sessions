import numpy as np
import math # Although not used in the final logic, import common libraries

"""
Transforms a 1D sequence of integers. It identifies contiguous blocks of identical 
non-zero numbers. If a block's length is greater than 2, it replaces all 
elements within the block, except for the first and the last, with 0. 
Elements that are 0 or part of non-zero blocks with length 2 or less remain 
unchanged. Handles list or numpy array inputs.
"""

def find_block_end(sequence: list[int], start_index: int) -> int:
    """
    Finds the end index of a contiguous block of identical values starting at start_index.
    Assumes sequence[start_index] is the value to match.

    Args:
        sequence (list[int]): The input sequence of numbers.
        start_index (int): The starting index of the block.

    Returns:
        int: The index of the last element in the block.
    """
    value_to_match = sequence[start_index]
    # This helper assumes it's called on a valid start of a block (non-zero checked before call)
    # or on a zero, in which case the block length is 1.
    # The main loop handles the non-zero check.
    
    end_index = start_index
    # Iterate while the next index is within bounds and the value matches
    while end_index + 1 < len(sequence) and sequence[end_index + 1] == value_to_match:
        end_index += 1
    return end_index

def transform(input_grid) -> list[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid (list[int] or np.ndarray): The input 1D sequence.

    Returns:
        list[int]: The transformed 1D sequence as a Python list.
    """
    
    # Ensure input is a standard Python list of standard Python ints
    if isinstance(input_grid, np.ndarray):
         # Convert numpy array to list of standard Python ints
         work_list = [int(x) for x in input_grid.tolist()] 
    elif isinstance(input_grid, list):
         # Ensure elements are standard ints if it's already a list
         work_list = [int(x) for x in input_grid]
    else:
        # Handle other potential iterable types, converting to list of ints
        try:
            work_list = [int(x) for x in list(input_grid)]
        except (TypeError, ValueError) as e:
            raise TypeError(f"Input must be convertible to a list of integers. Error: {e}")

    # Initialize output_grid as a copy of the processed input list to modify
    output_grid = list(work_list)
    n = len(output_grid)
    i = 0 # Current index for scanning the sequence

    # Iterate through the sequence to find and process blocks
    while i < n:
        current_value = output_grid[i]

        # Check if the current element is non-zero (potential start of a block to modify)
        if current_value != 0:
            # Find the end of the contiguous block starting at index i
            start_index = i
            end_index = find_block_end(output_grid, start_index)
            
            # Calculate the length of the identified block
            block_length = end_index - start_index + 1

            # Modify the block in the output_grid if its length is greater than 2
            if block_length > 2:
                # Iterate through the interior elements of the block (excluding start and end)
                for j in range(start_index + 1, end_index):
                    # Set the interior elements to 0
                    output_grid[j] = 0
            
            # Move the main index past the currently processed block
            # regardless of whether it was modified or not
            i = end_index + 1 
        else:
            # If the current element is 0, just move to the next element
            i += 1

    # Return the modified sequence as a standard Python list
    return output_grid