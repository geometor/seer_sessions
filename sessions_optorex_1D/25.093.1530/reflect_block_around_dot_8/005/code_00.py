"""
Transforms an input 1D sequence (list or NumPy array) of 12 integers based on a reflection rule centered around the element '2'.

1.  Accepts a 1D sequence of 12 integers.
2.  Creates a new 1D sequence of length 12, initialized with zeros.
3.  Finds the index (pivot_index) of the element '2' in the input.
4.  Places '2' into the output sequence at the pivot_index.
5.  Iterates through the input sequence. For each non-zero element that is not '2':
    a.  Calculates its new index by reflecting its position across the pivot index using the formula: new_index = (2 * pivot_index) - current_index.
    b.  Places the element into the output sequence at the new_index.
6.  Returns the completed output sequence.
"""

import numpy as np

def find_pivot_index(sequence, pivot_value=2):
  """
  Finds the index of the first occurrence of the pivot value in a 1D sequence.

  Args:
    sequence: The input 1D NumPy array or list.
    pivot_value: The value to find the index of (defaults to 2).

  Returns:
    The index of the first occurrence of pivot_value.

  Raises:
    ValueError: If the pivot_value is not found in the sequence.
  """
  indices = np.where(np.array(sequence) == pivot_value)[0] # Convert to array just in case
  if len(indices) == 0:
    raise ValueError(f"Pivot value {pivot_value} not found in sequence")
  return indices[0] # Return the index of the first occurrence

def reflect_position(current_index, pivot_index):
  """
  Calculates the reflected index across the pivot.

  Args:
    current_index: The original index of the element.
    pivot_index: The index of the pivot element.

  Returns:
    The calculated reflected index.
  """
  return (2 * pivot_index) - current_index

def transform(input_sequence):
    """
    Applies the reflection transformation to the input sequence.

    Args:
        input_sequence: A 1D list or NumPy array of 12 integers.

    Returns:
        A 1D NumPy array of 12 integers representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence)

    # Handle potential multi-dimensional input by attempting to flatten
    # This addresses the error seen previously if input is shape (1, 12)
    if input_array.ndim > 1:
        if input_array.shape[0] == 1: # Check if it's a single row
             input_array = input_array.flatten()
        else:
            # Handle cases with more complex shapes if necessary,
            # for now, raise an error as the problem implies 1D input.
            raise ValueError(f"Input sequence must be 1-dimensional, but got shape {input_array.shape}")


    # Determine the length of the sequence
    n = len(input_array)
    if n == 0: # Handle empty input case
      return np.array([])

    # Initialize the output sequence with zeros using NumPy
    output_sequence = np.zeros(n, dtype=input_array.dtype)

    try:
      # Find the index of the pivot element '2'
      pivot_index = find_pivot_index(input_array, 2)
    except ValueError as e:
      # Handle the case where the pivot '2' is missing (shouldn't happen based on examples)
      print(f"Error: {e}. Cannot perform transformation without pivot.")
      # Return the original sequence or an empty one, depending on desired behavior
      # Returning input as a fallback, though error is more informative.
      return input_array

    # Place the pivot element '2' in the output sequence at the same index
    # Check bounds just in case, though find_pivot_index should ensure it's valid if no error raised
    if 0 <= pivot_index < n:
        output_sequence[pivot_index] = 2
    else:
        # This case should not happen if find_pivot_index works correctly.
        print(f"Warning: Pivot index {pivot_index} is out of bounds for length {n}.")
        # Depending on requirements, might return early or continue without pivot placement

    # Iterate through the input sequence to place the other non-zero elements
    for i, value in enumerate(input_array):
        # Skip zeros and the pivot element itself (already placed)
        if value != 0 and value != 2:
            # Calculate the new index by reflecting across the pivot
            new_index = reflect_position(i, pivot_index)

            # Ensure the new index is within the bounds of the sequence
            if 0 <= new_index < n:
                # Place the element's value at the reflected position in the output
                output_sequence[new_index] = value
            else:
                # Handle cases where reflection goes out of bounds.
                # Based on examples, this is not expected.
                print(f"Warning: Calculated new index {new_index} for value {value} at original index {i} is out of bounds.")

    # Return the fully constructed output sequence
    return output_sequence