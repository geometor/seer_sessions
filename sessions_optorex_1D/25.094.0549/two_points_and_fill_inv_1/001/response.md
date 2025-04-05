```python
import math
import numpy as np # Although numpy isn't strictly needed for list manipulation, it's a common import.

"""
Identifies contiguous blocks of identical non-zero numbers in a 1D sequence. 
If a block's length is greater than 2, it replaces all elements within the block, except for the first and the last, with 0. 
Elements that are 0 or part of blocks with length 2 or less remain unchanged.
"""

def find_block_end(sequence, start_index):
    """
    Finds the end index of a contiguous block of identical non-zero values.
    
    Args:
        sequence (list): The input sequence of numbers.
        start_index (int): The starting index of the potential block.

    Returns:
        int: The index of the last element in the block.
    """
    value_to_match = sequence[start_index]
    if value_to_match == 0: # Should not happen if called correctly, but good for safety
        return start_index 
        
    end_index = start_index
    while end_index + 1 < len(sequence) and sequence[end_index + 1] == value_to_match:
        end_index += 1
    return end_index

def transform(input_grid: list[int]) -> list[int]:
    """
    Transforms the input sequence based on contiguous non-zero blocks.

    Args:
        input_grid (list[int]): The input 1D sequence of integers.

    Returns:
        list[int]: The transformed 1D sequence.
    """
    # Initialize output_grid as a copy of the input to modify
    output_grid = list(input_grid)
    n = len(output_grid)
    i = 0 # Current index for scanning the sequence

    # Iterate through the sequence to find and process blocks
    while i < n:
        current_value = output_grid[i]

        # Check if the current element is non-zero and could start a block
        if current_value != 0:
            # Find the end of the contiguous block starting at index i
            start_index = i
            end_index = find_block_end(output_grid, start_index)
            
            # Calculate the length of the identified block
            block_length = end_index - start_index + 1

            # Modify the block in the output_grid if its length is greater than 2
            if block_length > 2:
                # Iterate through the interior elements of the block
                for j in range(start_index + 1, end_index):
                    # Set the interior elements to 0
                    output_grid[j] = 0
            
            # Move the main index past the processed block
            i = end_index + 1 
        else:
            # If the current element is 0, just move to the next element
            i += 1

    # Return the modified sequence
    return output_grid
```