"""
Transforms an input 1D NumPy array of integers based on the position of the first occurrence of the number 2.
If 2 is found, the portion of the array *before* the first 2 is modified: all zero elements are moved to the beginning of this portion, and all non-zero elements are moved after the zeros, preserving their relative order. The portion of the array starting from the first 2 onwards remains unchanged.
If 2 is not present, or if it is the first element, the array remains unchanged.
"""

import numpy as np
import collections # Although not strictly needed now, kept for potential future list operations

def find_first_occurrence(sequence: list, target: int) -> int:
    """
    Finds the index of the first occurrence of target in the sequence (list).
    Returns -1 if the target is not found.
    """
    try:
        return sequence.index(target)
    except ValueError:
        return -1 # Indicate not found

def segregate_and_reorder(sub_sequence: list) -> list:
    """
    Separates zero elements from non-zero elements in a list,
    then returns a new list with zeros first, followed by the non-zeros,
    preserving the relative order of the non-zero elements.
    """
    # Extract zero elements
    zeros = [elem for elem in sub_sequence if elem == 0]
    # Extract non-zero elements, maintaining order
    non_zeros = [elem for elem in sub_sequence if elem != 0]
    # Combine them with zeros first
    return zeros + non_zeros

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Convert NumPy array to list for easier manipulation
    input_list = input_grid.tolist()

    # Define the separator value
    separator_value = 2

    # Find the index of the first occurrence of the separator
    separator_index = find_first_occurrence(input_list, separator_value)

    # Handle cases where no transformation is needed:
    # 1. Separator not found
    # 2. Separator is the first element (left part is empty)
    if separator_index == -1 or separator_index == 0:
        # Return the original grid as no changes are made
        return input_grid

    # Partition the list into left and right parts based on the separator index
    left_part = input_list[:separator_index]
    right_part = input_list[separator_index:] # Includes the separator

    # Segregate zeros and non-zeros in the left part and reorder
    reordered_left_part = segregate_and_reorder(left_part)

    # Concatenate the reordered left part with the original right part
    output_list = reordered_left_part + right_part

    # Convert the final list back to a NumPy array
    output_grid = np.array(output_list, dtype=input_grid.dtype) # Preserve original dtype

    # Return the transformed grid
    return output_grid
