```python
"""
Transforms an input sequence (numpy array) of digits by identifying the first 
contiguous block of non-zero digits and shifting this block 3 positions to the left. 
The sequence length remains constant, and positions outside the newly placed block 
are filled with zeros. Elements shifted to indices less than 0 are discarded.
"""

import numpy as np

def find_nonzero_block(input_seq):
    """
    Finds the first contiguous block of non-zero digits in a sequence.

    Args:
        input_seq: A 1D numpy array of integers.

    Returns:
        A tuple containing:
        - numpy.ndarray: The block of non-zero digits.
        - int: The starting index of the block in the original sequence.
               Returns -1 if no non-zero block is found.
    """
    start_index = -1
    block = []
    
    # Find the start of the block
    for i, val in enumerate(input_seq):
        if val != 0:
            start_index = i
            break
            
    # If no non-zero element found, return empty block and -1 index
    if start_index == -1:
        return np.array([]), -1
        
    # Extract the block from the start index
    for i in range(start_index, len(input_seq)):
        if input_seq[i] != 0:
            block.append(input_seq[i])
        else:
            # End of the block found
            break
            
    return np.array(block), start_index

def transform(input_grid):
    """
    Applies the block-shifting transformation to the input numpy array.

    Args:
        input_grid: A 1D numpy array representing the sequence of digits.

    Returns:
        A 1D numpy array representing the transformed sequence.
    """
    # Ensure input is treated as a 1D sequence
    if input_grid.ndim > 1:
        # Handle potential multi-dimensional input if necessary, 
        # for now, assume it's flattenable or take the first row/appropriate dimension
        # Based on examples, it's 1D. If errors occur, this might need adjustment.
        # Flattening just in case it comes wrapped unnecessarily.
        input_seq = input_grid.flatten()
    else:
        input_seq = input_grid

    # Get the length of the sequence
    n = len(input_seq)
    
    # Initialize the output grid (sequence) with zeros
    output_grid = np.zeros_like(input_seq)

    # Find the non-zero block and its original starting position
    block, start_index = find_nonzero_block(input_seq)

    # If no block was found, the output is already correctly initialized to zeros
    if start_index == -1:
        return output_grid

    # Calculate the new starting index for the block (shift left by 3)
    new_start_index = start_index - 3
    block_len = len(block)

    # Place the identified block into the output grid at the new position
    # Iterate through the elements of the found block
    for i in range(block_len):
        # Calculate the target index in the output grid
        output_index = new_start_index + i
        
        # Place the block element only if the target index is within the bounds of the grid
        # Elements shifted beyond the start (index < 0) are effectively dropped.
        if 0 <= output_index < n:
            output_grid[output_index] = block[i]
            
    # Return the transformed grid
    return output_grid
```