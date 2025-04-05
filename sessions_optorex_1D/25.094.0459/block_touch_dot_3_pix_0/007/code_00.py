import numpy as np

"""
Transforms an input 1D NumPy array of integers based on the position of the first occurrence of the number 2 (the separator).
If the separator 2 is found at an index greater than 0, the portion of the array *before* the separator ('left part') is modified: all zero elements within this 'left part' are collected and placed at the beginning of this part, followed by all non-zero elements from the original 'left part', preserving the relative order of these non-zero elements.
The portion of the array starting from the separator 2 onwards ('right part') remains unchanged.
If the separator 2 is not found, or if it is the first element (index 0), the array remains unchanged.
"""

# Helper function to find the first occurrence of a target value in a list
def find_first_occurrence(sequence: list, target: int) -> int:
    """
    Finds the index of the first occurrence of target in the sequence (list).
    Returns -1 if the target is not found.
    """
    try:
        # Attempt to find the index of the target value
        return sequence.index(target)
    except ValueError:
        # Return -1 if the target is not present in the sequence
        return -1

# Helper function to reorder the part of the sequence before the separator
def segregate_and_reorder_left_part(sub_sequence: list) -> list:
    """
    Separates zero elements from non-zero elements in the input list ('left part'),
    then returns a new list with all the original zeros placed first,
    followed by all the original non-zero elements, preserving the relative
    order of the non-zero elements.
    """
    # Count the number of zero elements in the sub-sequence
    num_zeros = sub_sequence.count(0)
    
    # Create a list containing only the non-zero elements, preserving their order
    non_zeros_ordered = [elem for elem in sub_sequence if elem != 0]
    
    # Construct the reordered list: num_zeros zeros followed by the ordered non-zeros
    reordered_list = [0] * num_zeros + non_zeros_ordered
    
    # Return the newly constructed list
    return reordered_list

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Convert the input NumPy array to a Python list for easier element manipulation
    # like finding index and slicing.
    input_list = input_grid.tolist()

    # Define the value that acts as the separator
    separator_value = 2

    # Find the index of the first occurrence of the separator using the helper function
    separator_index = find_first_occurrence(input_list, separator_value)

    # Check conditions where no transformation is needed:
    # 1. Separator is not found (index is -1)
    # 2. Separator is the first element (index is 0), meaning the 'left part' is empty.
    if separator_index == -1 or separator_index == 0:
        # In these cases, the original input grid is returned unchanged.
        return input_grid

    # If the separator is found at index > 0, proceed with partitioning and reordering.
    
    # Partition the list into 'left part' and 'right part' based on the separator index.
    # Left part includes elements *before* the separator.
    left_part = input_list[:separator_index]
    # Right part includes elements *from* the separator onwards (inclusive).
    right_part = input_list[separator_index:]

    # Apply the segregation and reordering logic to the 'left part' using the helper function.
    # This moves zeros to the start of the left part while keeping non-zero relative order.
    reordered_left_part = segregate_and_reorder_left_part(left_part)

    # Concatenate the 'reordered left part' with the original 'right part' to form the final sequence list.
    output_list = reordered_left_part + right_part

    # Convert the resulting list back to a NumPy array.
    # It's important to preserve the original data type (dtype) of the input grid.
    output_grid = np.array(output_list, dtype=input_grid.dtype)

    # Return the transformed NumPy array.
    return output_grid