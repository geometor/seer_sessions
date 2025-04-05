import numpy as np
from typing import List

"""
Transforms a sequence of digits based on contiguous blocks of identical non-zero digits.
The input is a NumPy array, potentially 2D (1xN or Nx1) or 1D (N,).
The core logic extracts the 1D sequence from the input array.
It then identifies contiguous blocks of identical non-zero numbers within this sequence.
If a block's length is greater than 2, only the first and last elements of the block 
are kept in the output sequence, and the elements between them are changed to 0. 
Blocks of length 1 or 2, and all zero elements, remain unchanged in the output sequence.
The function returns the transformed sequence as a Python list of integers.
"""

def _extract_1d_sequence(grid: np.ndarray) -> List[int]:
    """Extracts the 1D sequence from a potentially 1D or 2D numpy array."""
    if grid.ndim == 1:
        # Already a 1D array
        sequence = grid
    elif grid.ndim == 2:
        # Check if it's a row vector (1xN) or column vector (Nx1)
        if grid.shape[0] == 1:
            # Row vector
            sequence = grid[0]
        elif grid.shape[1] == 1:
            # Column vector
            sequence = grid[:, 0]
        else:
            # Handle unexpected 2D shapes if necessary, for now assume 1xN or Nx1
            # Defaulting to first row if shape is ambiguous but 2D
            sequence = grid[0] 
    else:
        # Handle higher dimensions if necessary, raise error or default
        raise ValueError(f"Input grid has unexpected dimension: {grid.ndim}")
        
    return sequence.tolist() # Convert the extracted 1D numpy array to a Python list


def transform(input_grid: np.ndarray) -> List[int]:
    """
    Applies the block transformation rule to the input numpy array sequence.

    Args:
        input_grid: A numpy array containing the sequence (potentially 1D or 2D).

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    # 1. Extract the 1D sequence from the input grid and convert to list
    sequence_list = _extract_1d_sequence(input_grid)
    n = len(sequence_list)
    
    # 2. Initialize output_list as a copy of the extracted sequence_list
    # This list will be modified according to the rules.
    output_list = list(sequence_list) 

    # 3. Iterate through the sequence_list to find blocks
    i = 0
    while i < n:
        current_val = sequence_list[i]
        
        # 4. Check if the current element is non-zero (potential start of a block)
        if current_val != 0:
            start_index = i
            
            # 5. Find the end of the contiguous block of the same non-zero value
            j = i
            while j + 1 < n and sequence_list[j + 1] == current_val:
                j += 1
            end_index = j
            
            # 6. Calculate the length of the block
            block_length = end_index - start_index + 1
            
            # 7. Apply the transformation rule if block length is greater than 2
            if block_length > 2:
                # Zero out the middle elements in the output list
                # Loop from the element *after* the start up to (but not including) the end element.
                for k in range(start_index + 1, end_index):
                    output_list[k] = 0
            # Else (block_length <= 2): No change needed in output_list, 
            # as it was initialized as a copy.
            
            # 8. Advance the main loop index past the processed block
            i = end_index + 1
        else:
            # 9. If the current element is 0, just move to the next element
            i += 1
            
    # 10. Return the modified list
    return output_list