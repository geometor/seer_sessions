"""
Transforms an input sequence of integers based on the following rules:
1. Find the first index `i` where an element differs from its immediate successor.
2. If no such difference exists or the sequence is too short, return the original sequence.
3. Identify the value at index `i` as the `anchor_value`.
4. Define a segment starting from the index `i + 1` (`start_index`).
5. Find the first index `j` (`end_index`), where `j >= start_index`, such that the element's value equals the `anchor_value`.
6. Extract this segment (from `start_index` to `end_index`, inclusive).
7. Perform a right rotation on the extracted segment (move the last element to the front, shifting others right).
8. Reconstruct the sequence by concatenating the part before the segment, the rotated segment, and the part after the segment.
9. Return the modified sequence as a numpy array.
"""

import numpy as np

# Helper function to find the first index where adjacent elements differ
def _find_first_difference_index(sequence: list) -> int:
    """Finds the first index i where sequence[i] != sequence[i+1]."""
    for i in range(len(sequence) - 1):
        if sequence[i] != sequence[i+1]:
            return i
    return -1 # Indicate no difference found

# Helper function to find the first index >= start_index matching a given value
def _find_first_matching_value_index(sequence: list, start_index: int, value_to_match: int) -> int:
    """Finds the first index j >= start_index where sequence[j] == value_to_match."""
    for j in range(start_index, len(sequence)):
        if sequence[j] == value_to_match:
            return j
    # This case should ideally not be reached based on task description/examples,
    # but returning -1 indicates it wasn't found.
    return -1

# Helper function to perform a right rotation on a list segment
def _rotate_right(segment: list) -> list:
    """Performs a right rotation on the segment (list)."""
    if not segment or len(segment) <= 1:
        return segment # No rotation needed for empty or single-element lists
    # Moves the last element to the first position
    return [segment[-1]] + segment[:-1]

def transform(input_sequence):
    """
    Applies a segment rotation transformation to the input sequence.
    Accepts a list or numpy array as input and returns a numpy array.
    """
    # Convert input to a list for consistent manipulation, handle numpy arrays
    if isinstance(input_sequence, np.ndarray):
        sequence = input_sequence.tolist()
    else:
        # Assume it's already list-like, ensure it's a mutable list
        sequence = list(input_sequence)

    # Rule 2 (part 1): Handle sequences too short for comparison
    if len(sequence) < 2:
        return np.array(sequence) # Return as numpy array

    # Rule 1: Find the first index `i` where the element differs from its successor
    first_diff_index = _find_first_difference_index(sequence)

    # Rule 2 (part 2): If no difference is found, return the original sequence
    if first_diff_index == -1:
        return np.array(sequence)

    # Rule 3: Get the value at index `i`
    anchor_value = sequence[first_diff_index]

    # Rule 4: Define the start of the target segment
    start_index = first_diff_index + 1

    # Rule 5: Find the first index `j` >= start_index where the element matches anchor_value
    end_index = _find_first_matching_value_index(sequence, start_index, anchor_value)

    # Defensive check: handle case where matching anchor value isn't found
    # (This shouldn't occur based on the problem's examples)
    if end_index == -1:
        # This indicates an unexpected input pattern or flaw in understanding
        print(f"Warning: Could not find matching anchor value {anchor_value} >= index {start_index}. Returning original sequence.")
        return np.array(sequence)

    # Rule 6: Extract the segment to be rotated
    # Slicing sequence[start_index : end_index + 1] correctly includes the element at end_index
    segment_to_rotate = sequence[start_index : end_index + 1]

    # Rule 7: Perform a right rotation on the extracted segment
    rotated_segment = _rotate_right(segment_to_rotate)

    # Rule 8: Construct the output sequence by concatenating parts
    # Part before segment: sequence[:start_index]
    # Rotated segment: rotated_segment
    # Part after segment: sequence[end_index + 1:]
    output_sequence_list = sequence[:start_index] + rotated_segment + sequence[end_index + 1:]

    # Rule 9: Return the modified sequence as a numpy array
    return np.array(output_sequence_list)