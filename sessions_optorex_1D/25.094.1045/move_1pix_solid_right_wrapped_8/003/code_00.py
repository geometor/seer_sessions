import math
import numpy as np # Although not strictly necessary for list ops, the error message mentioned numpy

"""
Transforms an input sequence of integers based on the following rules:
1. Find the first index `i` where an element differs from its immediate successor.
2. Identify the value at this index `i` as the `anchor_value`.
3. Define a segment starting from the index `i + 1`.
4. Find the first index `j` (where `j >= i + 1`) where the element's value equals the `anchor_value`. The segment ends at this index `j`.
5. Extract this segment (from `i + 1` to `j`, inclusive).
6. Perform a right rotation on the extracted segment (move the last element to the front).
7. Replace the original segment in the sequence with the rotated segment.
8. Return the modified sequence.
If no adjacent elements differ, or if the sequence is too short, return the original sequence unchanged.
"""

def find_first_difference_index(sequence):
  """Finds the first index i where sequence[i] != sequence[i+1]."""
  # Convert numpy array to list if necessary for easier iteration/comparison
  seq_list = list(sequence)
  for i in range(len(seq_list) - 1):
    if seq_list[i] != seq_list[i+1]:
      return i
  return -1 # Indicate no difference found

def find_first_matching_value_index(sequence, start_index, value_to_match):
  """Finds the first index j >= start_index where sequence[j] == value_to_match."""
  # Convert numpy array to list if necessary
  seq_list = list(sequence)
  for j in range(start_index, len(seq_list)):
    if seq_list[j] == value_to_match:
      return j
  # This case should ideally not be reached based on task description,
  # but returning -1 for robustness.
  return -1 

def rotate_right(segment):
  """Performs a right rotation on the segment (list)."""
  if not segment:
    return []
  # Handle single element segment
  if len(segment) == 1:
      return segment
  # Moves the last element to the first position
  return [segment[-1]] + segment[:-1]

def transform(input_sequence):
    """
    Applies the described rotation transformation to a segment of the input sequence.
    Accepts a list or numpy array as input and returns a numpy array.
    """
    # Convert input to a list for easier manipulation, handle potential numpy array input
    if isinstance(input_sequence, np.ndarray):
        sequence = input_sequence.tolist()
    else:
        # Assume it's already list-like
        sequence = list(input_sequence)

    # Handle sequences too short for comparison
    if len(sequence) < 2:
        return np.array(sequence) # Return as numpy array

    # Find the first index `i` where the element differs from its successor
    first_diff_index = find_first_difference_index(sequence)

    # If no difference is found, return the original sequence as a numpy array
    if first_diff_index == -1:
        return np.array(sequence)

    # Store the value at index `i` as `anchor_value`.
    anchor_value = sequence[first_diff_index]

    # Define the start of the target segment
    start_index = first_diff_index + 1

    # Find the first index `j` >= start_index where the element matches anchor_value
    end_index = find_first_matching_value_index(sequence, start_index, anchor_value)

    # Handle case where matching anchor value isn't found after start_index
    # (Should not happen based on examples, but defensive check)
    if end_index == -1:
        print(f"Warning: Could not find matching anchor value {anchor_value} >= index {start_index}. Returning original.")
        return np.array(sequence) # Return original sequence as numpy array

    # Extract the segment to be rotated
    # Slicing works correctly up to end_index + 1
    segment_to_rotate = sequence[start_index : end_index + 1]

    # Perform a right rotation on the extracted segment
    rotated_segment = rotate_right(segment_to_rotate)

    # Construct the output sequence by concatenating parts
    output_sequence_list = sequence[:start_index] + rotated_segment + sequence[end_index + 1:]

    # Return the modified sequence as a numpy array
    return np.array(output_sequence_list)