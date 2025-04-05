import collections

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

def find_first_index(sequence, value_to_find):
    """Finds the index of the first occurrence of a value in a list."""
    try:
        return sequence.index(value_to_find)
    except ValueError:
        return -1 # Value not found

def find_first_non_zero_index(sequence):
    """Finds the index of the first non-zero element in a list."""
    try:
        return next(i for i, x in enumerate(sequence) if x != 0)
    except StopIteration:
        return -1 # No non-zero elements found

def transform(input_string: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_string: A space-separated string of integers.

    Returns:
        A space-separated string of integers representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_string.split()]

    # Handle empty input
    if not input_list:
        return ""

    # Make a copy to modify
    output_list = list(input_list)

    # Find the index of the first zero
    first_zero_index = find_first_index(output_list, 0)

    # Initialize the index of the element to move
    index_to_move = 0

    # Apply the core logic based on the position of the first zero
    if first_zero_index > 0:
        # Case 1: First zero is not at the beginning
        index_to_move = first_zero_index - 1
    elif first_zero_index == 0:
        # Case 2: First zero is at the beginning
        # Find the index of the first non-zero element
        first_non_zero_index = find_first_non_zero_index(output_list)
        if first_non_zero_index > 0:
             # Subcase 2a: First non-zero is found after index 0
            index_to_move = first_non_zero_index - 1
        else:
             # Subcase 2b: First non-zero is at index 0 or not found (all zeros)
             # Keep index_to_move = 0 (default)
             pass
    else: # first_zero_index == -1
        # Case 3: No zeros found
        # Keep index_to_move = 0 (default)
        pass

    # Ensure index_to_move is valid (should always be unless list was empty)
    if 0 <= index_to_move < len(output_list):
        # Remove the element at the calculated index
        element_to_move = output_list.pop(index_to_move)
        # Append the removed element to the end
        output_list.append(element_to_move)
    # Else: Index out of bounds, should not happen with current logic and non-empty list

    # Format the result back into a space-separated string
    return " ".join(map(str, output_list))