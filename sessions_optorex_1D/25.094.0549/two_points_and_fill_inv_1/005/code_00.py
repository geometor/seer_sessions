import numpy as np
import math # Keep standard imports, even if math isn't used directly here

"""
Transforms a 1D sequence of integers, typically provided within a nested list 
(e.g., [[...]] representing a 1xN grid). It identifies contiguous blocks of 
identical non-zero numbers within the sequence. If a block's length is greater 
than 2, it replaces all elements within the block, except for the first and 
the last, with 0. Elements that are 0 or part of non-zero blocks with 
length 2 or less remain unchanged. The output is returned in the same 
nested list format as the input.
"""

def find_block_end(sequence: list[int], start_index: int) -> int:
    """
    Finds the end index of a contiguous block of identical values starting at start_index.

    Args:
        sequence (list[int]): The 1D sequence of numbers being processed.
        start_index (int): The starting index of the block.

    Returns:
        int: The index of the last element in the block.
    """
    # Get the value to match for the block
    value_to_match = sequence[start_index]
    
    # Start assuming the block ends where it starts
    end_index = start_index
    
    # Extend the end_index as long as the next element is within bounds and matches the block value
    while end_index + 1 < len(sequence) and sequence[end_index + 1] == value_to_match:
        end_index += 1
        
    # Return the final index of the block
    return end_index

def transform(input_grid) -> list[list[int]]:
    """
    Applies the transformation rule to the input sequence contained within the input_grid.

    Args:
        input_grid (list[list[int]] or np.ndarray): The input structure, expected 
                   to contain a single inner list or row representing the 1D sequence.

    Returns:
        list[list[int]]: The transformed sequence, wrapped in a list to match the 
                         expected output format.
    """
    
    # Extract the actual 1D sequence from the input grid structure
    # Handles both list of lists and numpy array inputs
    if isinstance(input_grid, np.ndarray):
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
             # Extract the first row if it's a 1xN numpy array
             work_sequence = [int(x) for x in input_grid[0].tolist()]
        elif input_grid.ndim == 1:
             # Handle 1D numpy array directly
             work_sequence = [int(x) for x in input_grid.tolist()]
        else:
             raise ValueError("Input numpy array format not supported. Expected 1D or 1xN.")
             
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
         # Extract the first list if it's a list containing one inner list
         work_sequence = [int(x) for x in input_grid[0]]
         
    elif isinstance(input_grid, list) and all(isinstance(x, (int, np.integer)) for x in input_grid):
         # Handle if a flat list is passed directly (less likely based on errors, but robust)
         work_sequence = [int(x) for x in input_grid]
         
    else:
        # Raise error for unexpected input types/structures
        raise TypeError(f"Unsupported input_grid type or structure: {type(input_grid)}")

    # Initialize output_sequence as a copy of the extracted sequence to modify
    output_sequence = list(work_sequence)
    n = len(output_sequence)
    i = 0 # Current index for scanning the sequence

    # Iterate through the sequence to find and process blocks
    while i < n:
        # Get the value at the current index
        current_value = output_sequence[i]

        # Check if the current element is non-zero (potential start of a block to modify)
        if current_value != 0:
            # Find the start and end indices of the contiguous block
            start_index = i
            end_index = find_block_end(output_sequence, start_index)
            
            # Calculate the length of the identified block
            block_length = end_index - start_index + 1

            # Modify the block in the output_sequence if its length is greater than 2
            if block_length > 2:
                # Iterate through the interior elements of the block (excluding start and end)
                for j in range(start_index + 1, end_index):
                    # Set the interior elements to 0
                    output_sequence[j] = 0
            
            # Move the main index past the currently processed block
            # regardless of whether it was modified or not
            i = end_index + 1 
        else:
            # If the current element is 0, just move to the next element
            i += 1

    # Return the modified sequence, wrapped in a list to match the expected output format
    return [output_sequence]