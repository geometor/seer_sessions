import numpy as np
from typing import List, Set

"""
Transforms an input list/array of integers by shifting the positions occupied 
by zeros one step to the right (wrapping around from the end to the beginning) 
and filling the remaining positions with the non-zero elements from the input, 
preserving their original relative order.
"""

def _find_indices(data: List[int], value: int) -> List[int]:
    """Helper function to find all indices of a specific value in a list."""
    return [i for i, x in enumerate(data) if x == value]

def _get_non_zero_elements(data: List[int]) -> List[int]:
    """Helper function to extract non-zero elements in their original order."""
    return [x for x in data if x != 0]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the zero-shifting transformation to the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array representing the transformed output.
    """
    # Convert input numpy array to list for easier index manipulation if needed,
    # or work directly with numpy. Choose list approach for clarity based on previous steps.
    input_list = input_grid.tolist()
    n = len(input_list)
    
    # Handle the edge case of an empty list/array
    if n == 0:
        return np.array([], dtype=input_grid.dtype)

    # 1. Identify the indices of all elements equal to 0 in the input sequence.
    zero_indices_input = _find_indices(input_list, 0)
    
    # 2. Extract all non-zero elements from the input sequence, preserving order.
    non_zero_elements = _get_non_zero_elements(input_list)

    # 3. Calculate the target indices for the 0s in the output sequence.
    #    Apply the formula target_index = (input_index + 1) % n
    target_zero_indices: Set[int] = set([(i + 1) % n for i in zero_indices_input])

    # 4. Determine the target indices for the non-zero elements in the output sequence.
    #    These are all indices not targeted by zeros. Sort them.
    all_indices = set(range(n))
    target_non_zero_indices: List[int] = sorted(list(all_indices - target_zero_indices))

    # 5. Create the output sequence (list first, then convert to numpy array).
    #    Initialize with a placeholder (like None) or default value (like 0).
    #    Using None helps catch unfilled spots if logic is flawed.
    output_list = [None] * n 

    # 6. Place the sequence of non-zero elements into the output sequence 
    #    at the corresponding sorted available indices.
    #    Check for length mismatch (should not occur if logic is correct).
    if len(non_zero_elements) != len(target_non_zero_indices):
        raise ValueError("Internal logic error: Mismatch between number of non-zero elements and available target slots.")
        
    non_zero_iter = iter(non_zero_elements)
    for idx in target_non_zero_indices:
        output_list[idx] = next(non_zero_iter)

    # 7. Place the value 0 into the output sequence at each of the target zero indices.
    for idx in target_zero_indices:
        output_list[idx] = 0
        
    # 8. Return the completed output sequence as a NumPy array.
    # Ensure no None placeholders remain.
    if None in output_list:
         raise ValueError("Internal logic error: Output list construction incomplete, placeholder found.")
         
    return np.array(output_list, dtype=input_grid.dtype)