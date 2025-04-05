"""
Processes a 2D NumPy array representing a grid, typically with a single row. 
It extracts the first row as the sequence to operate on. It identifies an 
initial sequence of non-zero numbers ('key sequence') in this row, occurring 
before the first zero. It then iterates through the row sequence. Numbers other 
than '5' are kept as is. Each contiguous block of '5's encountered is replaced 
by repeating the corresponding number from the key sequence. The first block of 
'5's uses the first number from the key sequence, the second block uses the 
second number, and so on. The '0's act as separators and remain unchanged.
The output grid has the same shape and data type as the input grid.
"""

import numpy as np
from typing import List

def _find_key_sequence(processing_sequence: np.ndarray) -> List[int]:
    """
    Extracts the initial sequence of non-zero integers before the first zero 
    from a 1D NumPy array.

    Args:
        processing_sequence: The 1D NumPy array to scan.

    Returns:
        A list containing the key sequence integers.
    """
    key_sequence = []
    for num in processing_sequence:
        # Convert numpy number types to standard python int for comparison if needed
        # but direct comparison should work for standard integer types.
        if int(num) != 0:
            key_sequence.append(int(num))
        else:
            # Stop at the first zero encountered
            break
    return key_sequence

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the described rule.

    Args:
        input_grid: A 2D NumPy array, expected to be 1xN.

    Returns:
        A 2D NumPy array with the same shape as input_grid, containing the 
        transformed sequence.
    """
    
    # Validate input shape and extract the sequence to process
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected dimensions, maybe raise error or return input
        # For now, assume the structure is always 1xN based on error analysis
        # If grid is empty, return an empty grid of the same shape
        if input_grid.size == 0:
             return np.array([], dtype=input_grid.dtype).reshape(input_grid.shape)
        # Attempt to process the first row if multiple rows exist, although 
        # examples suggest 1 row is standard
        print(f"Warning: Input grid shape {input_grid.shape} not 1xN. Processing first row.")
        # If it's 1D, reshape it to 2D (1, N)
        if input_grid.ndim == 1:
             input_grid = input_grid.reshape(1, -1)
        elif input_grid.shape[0] == 0: # Handle (0, N) case
             return np.array([], dtype=input_grid.dtype).reshape(input_grid.shape)
        # Fallback if shape is still not suitable after attempting fixes
        # This part might need adjustment based on stricter requirements
        if input_grid.shape[0] == 0:
             return np.array([], dtype=input_grid.dtype).reshape(input_grid.shape)


    processing_sequence = input_grid[0] # Extract the first (and likely only) row
    n = len(processing_sequence)
    
    # Handle empty sequence case
    if n == 0:
        return np.array([], dtype=input_grid.dtype).reshape(input_grid.shape) # Return empty grid matching original shape

    # Find the key sequence (initial non-zero numbers before the first 0)
    key_sequence = _find_key_sequence(processing_sequence)

    # Initialize the output list and the index for the key sequence
    output_list = []
    key_index = 0
    
    # Iterate through the processing sequence and build the output list
    for i, element_raw in enumerate(processing_sequence):
        element = int(element_raw) # Ensure element is a standard python int for comparison
        
        if element == 5:
            # If the element is 5, replace it with the current key number
            if key_index < len(key_sequence):
                replacement_value = key_sequence[key_index]
            else:
                # Handle edge case: more blocks of 5 than keys.
                # Reuse the last key if available, otherwise keep 5.
                replacement_value = key_sequence[-1] if key_sequence else 5
                
            output_list.append(replacement_value)

            # Check if this is the end of a block of 5s
            # End of block if:
            # 1. It's the last element of the list OR
            # 2. The next element exists and is not 5
            is_last_element = (i == n - 1)
            # Need to access processing_sequence for the lookahead check
            next_element_is_not_5 = (i + 1 < n) and (int(processing_sequence[i + 1]) != 5)

            if is_last_element or next_element_is_not_5:
                 # Move to the next key for the next block of 5s
                 key_index += 1
        else:
            # If the element is not 5, keep it as is
            output_list.append(element)

    # Convert the output list back to a NumPy array with the original dtype
    output_array_1d = np.array(output_list, dtype=input_grid.dtype)
    
    # Reshape the 1D array to match the original input grid's shape
    output_grid = output_array_1d.reshape(input_grid.shape)

    return output_grid