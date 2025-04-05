```python
"""
Transforms the input numpy array by shifting the contiguous block of non-zero digits 
one position to the left. This is achieved by finding the index of the first non-zero 
digit, removing the zero immediately preceding it (if one exists and the block doesn't 
start at index 0), and appending a zero to the end of the sequence to maintain its 
original length. The input and output are numpy arrays of integers.
"""

import numpy as np

def find_first_nonzero_index(data_list):
    """
    Finds the index of the first non-zero element in a list or numpy array.
    Returns -1 if no non-zero element is found.
    """
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Should not happen based on examples, but good practice

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the left-shift transformation to the non-zero block in the input array.

    Args:
        input_grid: A 1D numpy array of integers.

    Returns:
        A 1D numpy array of integers representing the transformed sequence.
    """
    # Convert numpy array to list for easier manipulation (pop, append)
    working_list = input_grid.tolist()

    # Find the index of the first non-zero element.
    first_nonzero_idx = find_first_nonzero_index(working_list)

    # Check if a non-zero element was found and if it's not at the very beginning.
    # The analysis confirmed the preceding element is always 0 in valid cases.
    if first_nonzero_idx > 0:
        # Identify the index of the zero immediately before the non-zero block.
        preceding_zero_idx = first_nonzero_idx - 1

        # Remove the element at the preceding zero's index.
        # pop() modifies the list in place.
        working_list.pop(preceding_zero_idx)

        # Append a single integer 0 to the end of this modified list
        # to maintain the original sequence length.
        working_list.append(0)
        
    # If first_nonzero_idx is 0 or -1 (no non-zeros), the list remains unchanged.

    # Convert the potentially modified list back into a numpy array 
    # with the same data type as the input.
    output_grid = np.array(working_list, dtype=input_grid.dtype)

    return output_grid
```