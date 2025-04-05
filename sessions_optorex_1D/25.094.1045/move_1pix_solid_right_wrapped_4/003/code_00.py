import collections
from typing import List, Set

"""
Transforms an input list of integers by shifting the positions occupied by zeros 
one step to the right (wrapping around from the end to the beginning) and filling 
the remaining positions with the non-zero elements from the input list, 
preserving their original relative order.
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
    # Get the length of the input list
    n = len(input_list)
    
    # Handle the edge case of an empty list
    if n == 0:
        return []

    # Find the indices of all zero elements in the input list
    zero_indices_input = _find_indices(input_list, 0)
    
    # Extract all non-zero elements from the input list, preserving their order
    non_zero_elements = _get_non_zero_elements(input_list)

    # Calculate the target indices for the zeros in the output list
    # Each zero's original index 'i' maps to target index '(i + 1) % n'
    target_zero_indices: Set[int] = set([(i + 1) % n for i in zero_indices_input])

    # Determine the target indices for the non-zero elements
    # These are all indices from 0 to n-1 that are NOT target indices for zeros
    all_indices = set(range(n))
    target_non_zero_indices: List[int] = sorted(list(all_indices - target_zero_indices))

    # Initialize the output list with a placeholder (e.g., None)
    # Using a placeholder helps ensure all positions are explicitly filled later
    output_list = [None] * n 

    # Place the non-zero elements into their target positions in the output list
    # Use an iterator for the non-zero elements to easily map them to the sorted target indices
    non_zero_iter = iter(non_zero_elements)
    for idx in target_non_zero_indices:
        # Ensure we don't run out of non-zero elements (shouldn't happen with correct logic)
        try:
            output_list[idx] = next(non_zero_iter)
        except StopIteration:
             # This indicates a mismatch between expected slots and available elements
            raise ValueError("Mismatch between number of non-zero elements and available slots.")

    # Place the zero elements into their calculated target positions
    for idx in target_zero_indices:
        output_list[idx] = 0
        
    # Check if any placeholder remains (debugging check, should not happen)
    if None in output_list:
        raise ValueError("Output list construction incomplete, placeholder found.")

    # Return the fully constructed output list
    return output_list