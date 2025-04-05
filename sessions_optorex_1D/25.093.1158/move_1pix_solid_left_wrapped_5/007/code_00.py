import numpy as np
from typing import List, Union, Optional

"""
Transforms a sequence of integers by moving a specific element to the end.
The element to move is determined based on the position of the first zero
and, if the first zero is at the beginning, the position of the first non-zero element.

Rule:
1. Find the index of the first '0' (first_zero_index).
2. If first_zero_index > 0, move the element at index `first_zero_index - 1`.
3. If first_zero_index == 0:
    a. Find the index of the first non-zero element (first_non_zero_index).
    b. If first_non_zero_index > 0, move the element at index `first_non_zero_index - 1`.
    c. Otherwise (first non-zero is at index 0, or all are zeros), move the element at index 0.
4. If first_zero_index == -1 (no zeros), move the element at index 0.
5. The selected element is removed from its original position and appended to the end.
"""

def _find_first_index(sequence: List[int], value_to_find: int) -> int:
    """Finds the index of the first occurrence of a value in a list."""
    try:
        return sequence.index(value_to_find)
    except ValueError:
        return -1 # Value not found

def _find_first_non_zero_index(sequence: List[int]) -> int:
    """Finds the index of the first non-zero element in a list."""
    try:
        return next(i for i, x in enumerate(sequence) if x != 0)
    except StopIteration:
        return -1 # No non-zero elements found

def transform(input_sequence: Union[List[int], np.ndarray]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Convert input to list if it's a NumPy array for easier manipulation
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    elif isinstance(input_sequence, list):
        input_list = input_sequence
    else:
        # Handle other potential types or raise an error
        try:
            input_list = list(input_sequence)
        except TypeError:
            raise TypeError("Input must be a list, NumPy array, or list-like sequence.")

    # Handle empty input
    if not input_list:
        return []

    # Create a mutable copy of the input_sequence called output_list
    output_list = list(input_list)

    # Find the index of the first occurrence of the zero_element (0)
    first_zero_index = _find_first_index(output_list, 0)

    # Initialize index_to_move to 0.
    index_to_move = 0

    # Conditional Logic to Determine index_to_move:
    if first_zero_index > 0:
        # Case a: First zero is not at the start
        index_to_move = first_zero_index - 1
    elif first_zero_index == 0:
        # Case b: First element is zero
        # Find the index of the first non_zero_element
        first_non_zero_index = _find_first_non_zero_index(output_list)
        if first_non_zero_index > 0:
            # Case b.ii: First non-zero is not at the start
            index_to_move = first_non_zero_index - 1
        # else:
            # Case b.iii: First non-zero is at index 0 or sequence is all zeros
            # Keep index_to_move = 0 (default)
            # pass
    # else: # first_zero_index == -1
        # Case c: No zeros in the sequence
        # Keep index_to_move = 0 (default)
        # pass

    # Perform the move: remove element and append it
    # Ensure index_to_move is valid (should always be for non-empty lists based on logic)
    if 0 <= index_to_move < len(output_list):
        # Remove the element at index_to_move and store it
        element_to_move = output_list.pop(index_to_move)
        # Append element_to_move to the end
        output_list.append(element_to_move)

    # Return the modified output_list
    return output_list