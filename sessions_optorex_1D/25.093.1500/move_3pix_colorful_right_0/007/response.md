```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms an input sequence of integers by identifying the first contiguous block 
of non-zero integers and shifting this block 3 positions to the right. 
The remaining positions in the output sequence are filled with zeros. 
The total length of the sequence remains unchanged. If no non-zero block is found,
the input sequence is returned unchanged. Handles NumPy array inputs and outputs.
"""

def _find_first_non_zero_block(data: np.ndarray) -> Optional[Tuple[int, List[int]]]:
    """
    Finds the first contiguous block of non-zero integers in a NumPy array.

    Args:
        data: A NumPy array of integers.

    Returns:
        A tuple containing the start index (0-based) of the block and the 
        block itself (as a list of integers), or None if no non-zero 
        numbers are found.
    """
    start_index = -1
    block = []
    
    # Iterate through the input array to find the start of the first block
    # np.nonzero returns indices where the condition is true. We take the first one.
    non_zero_indices = np.nonzero(data)[0] # Get indices of all non-zero elements
    if len(non_zero_indices) == 0:
        return None # No non-zero elements found

    start_index = non_zero_indices[0] # The start index is the first non-zero index

    # Extract the block starting from start_index until a zero is hit or array ends
    block = []
    for i in range(start_index, len(data)):
        num = data[i]
        if num != 0:
            block.append(num)
        else:
            break # End of the contiguous block found

    if not block: # Should not happen if start_index was found, but for safety
         return None

    return start_index, block

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array sequence.

    Args:
        input_sequence: A NumPy array of integers representing the input sequence.

    Returns:
        A NumPy array of integers representing the transformed sequence.
    """
    # Get the length of the input sequence
    n = len(input_sequence)
    
    # Find the first contiguous block of non-zero integers
    block_info = _find_first_non_zero_block(input_sequence)

    # If no non-zero block is found, return the original sequence.
    # Return a copy to ensure immutability if the original is needed elsewhere.
    if block_info is None:
        return np.copy(input_sequence) 

    # Extract block details: original start index and the block content (as a list)
    original_start_index, non_zero_block = block_info
    block_length = len(non_zero_block)
    
    # Define the shift amount (as determined from examples)
    shift_amount = 3
    
    # Calculate the new starting index for the block in the output
    new_start_index = original_start_index + shift_amount

    # Create the output sequence: an array of zeros with the same length and dtype as input
    output_sequence = np.zeros_like(input_sequence)

    # Place the non-zero block into the output sequence at the new position
    # Iterate through the elements of the found block (stored as a list)
    for i in range(block_length):
        # Calculate the target index in the output sequence for the current element
        target_index = new_start_index + i
        
        # Check if the target index is within the valid bounds of the output sequence
        if 0 <= target_index < n:
            # If within bounds, place the element from the block into the output sequence
            output_sequence[target_index] = non_zero_block[i]
        # else: 
            # If the target index is out of bounds, the element is truncated (effectively ignored).
            # No action needed here as the output array is already initialized with zeros.
            # We could break early if the first out-of-bounds index is reached,
            # but iterating fully handles all cases correctly.
            pass # Element is outside bounds, do nothing

    # Return the constructed output sequence (NumPy array)
    return output_sequence
```