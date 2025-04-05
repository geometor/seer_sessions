```python
import numpy as np

"""
Transforms an input sequence (list or array of 12 integers) by identifying the 
first contiguous block of non-zero digits and shifting this block 3 positions 
to the right within a new sequence of 12 zeros. If the shifted block extends 
beyond the sequence boundary, it is truncated. If no non-zero block exists, 
returns a sequence of 12 zeros. The relative order of the digits within the 
block is preserved.
"""

def find_first_nonzero_block(sequence: list) -> tuple | None:
    """
    Finds the start and end indices (inclusive) of the first contiguous 
    block of non-zero numbers in a list.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
    """
    start_index = -1
    end_index = -1
    in_block = False
    sequence_length = len(sequence)

    for i, digit in enumerate(sequence):
        # Start of a block
        if digit != 0 and not in_block:
            start_index = i
            in_block = True
        
        # End of a block (found a zero after being in a block)
        if digit == 0 and in_block:
            end_index = i - 1
            break # Found the first block, stop searching

        # Handle block extending to the very end of the sequence
        if digit != 0 and in_block and i == sequence_length - 1:
            end_index = i
            break # Reached the end while in a block

    # Check if a valid block was found (both start and end defined)
    if start_index != -1 and end_index != -1:
        return start_index, end_index
    else:
        # No non-zero digits found or only single non-zero at start without end being set
        # (or other unexpected cases like all zeros)
        return None


def transform(input_grid) -> list:
    """
    Applies the transformation rule to the input grid (sequence).
    
    Args:
        input_grid: A list or numpy array of 12 integers.
        
    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Ensure input is a flat list of integers
    if isinstance(input_grid, np.ndarray):
        input_sequence = input_grid.flatten().tolist()
    else:
        # Assuming it's already a list or similar iterable
        input_sequence = list(input_grid) 

    sequence_length = len(input_sequence) 
    # Assuming fixed length 12 based on examples, but using variable for robustness
    if sequence_length != 12:
        # Handle error or unexpected length if necessary, for now assume 12
        pass 

    # Initialize the output grid with zeros
    output_grid = [0] * sequence_length 

    # Find the first contiguous non-zero block in the input sequence
    block_indices = find_first_nonzero_block(input_sequence)

    # If a block is found, proceed with the shift and copy operation
    if block_indices:
        start_index, end_index = block_indices
        shift_amount = 3
        
        # Calculate the starting index for the block in the output grid
        new_start_index = start_index + shift_amount

        # Extract the block of non-zero digits from the input sequence
        # Slicing handles getting the correct sublist
        block_to_move = input_sequence[start_index : end_index + 1]

        # Place the extracted block into the output grid at the new position, handling boundaries
        for i, digit in enumerate(block_to_move):
            target_index = new_start_index + i
            
            # Check if the target index is within the bounds of the output grid
            if 0 <= target_index < sequence_length:
                output_grid[target_index] = digit
            else:
                # If the block shift goes out of bounds, stop copying (truncates)
                break 

    # If no block is found (block_indices is None), the output_grid remains all zeros

    # Return the transformed grid
    return output_grid
```