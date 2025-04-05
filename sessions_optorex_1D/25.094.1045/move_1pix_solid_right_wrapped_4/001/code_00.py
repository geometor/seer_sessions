import numpy as np
from typing import List

"""
Transforms an input list of integers based on the positions of the zero elements. 
The positions occupied by zeros in the input list are shifted one position to the 
right (wrapping around from the last position to the first) in the output list. 
The non-zero elements from the input list fill the remaining positions in the 
output list, maintaining their original relative order.
"""

def _find_indices(data: List[int], value: int) -> List[int]:
    """Helper function to find all indices of a specific value in a list."""
    return [i for i, x in enumerate(data) if x == value]

def _get_non_zero_elements(data: List[int]) -> List[int]:
    """Helper function to extract non-zero elements in their original order."""
    return [x for x in data if x != 0]

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the zero-shifting transformation to the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A new list of integers representing the transformed output.
    """
    n = len(input_list)
    if n == 0:
        return []

    # 1. Initialize an empty output list of the same size as the input list.
    #    (We'll use a temporary structure like None or a value not in input,
    #     then fill it. Or directly create the final list.)
    output_list = [None] * n # Initialize with placeholders

    # 2. Create a list of the indices where the input list contains the value 0.
    zero_indices_input = _find_indices(input_list, 0)

    # 3. Create an ordered list of the values of all non-zero elements from the input list.
    non_zero_elements = _get_non_zero_elements(input_list)

    # 4. Calculate the target indices for the 0s in the output list.
    #    For each index i found in step 2, compute the target index j as (i + 1) modulo n.
    target_zero_indices = set([(i + 1) % n for i in zero_indices_input])

    # 5. Determine the available indices for the non-zero elements in the output list.
    #    These are all indices from 0 to n-1 that are *not* target zero indices.
    all_indices = set(range(n))
    target_non_zero_indices = sorted(list(all_indices - target_zero_indices))

    # 6. Populate the output list:
    #    a. Place the ordered non-zero values into the output list at the available indices.
    non_zero_iter = iter(non_zero_elements)
    for idx in target_non_zero_indices:
        try:
            output_list[idx] = next(non_zero_iter)
        except StopIteration:
            # This shouldn't happen if logic is correct, but good practice
            raise ValueError("Mismatch between number of non-zero elements and available slots.")

    #    b. Place the value 0 into the output list at each of the target zero indices.
    for idx in target_zero_indices:
        output_list[idx] = 0

    # 7. Return the fully populated output list.
    return output_list
