import numpy as np
import collections # Although not strictly needed with the current numpy approach, good to keep in mind

"""
Transformation Rule:

1. Receive the input sequence (which can be a list or NumPy array of integers).
2. Identify the `last_element` of the input sequence.
3. Create a `base_sequence` containing all elements from the input sequence *except* the `last_element`, preserving their relative order.
4. Evaluate the value of the `last_element`:
   a. If the `last_element` is 0:
      i. Find the index (`insertion_index`) of the first non-zero element within the `base_sequence`.
      ii. If the `base_sequence` contains only zeros or is empty, set the `insertion_index` to 0.
      iii. Construct the `output_sequence` by inserting the `last_element` (0) into the `base_sequence` at the determined `insertion_index`.
   b. If the `last_element` is not 0:
      i. Set the `insertion_index` to 0.
      ii. Construct the `output_sequence` by inserting the `last_element` at the beginning (index 0) of the `base_sequence`.
5. Return the constructed `output_sequence`.
"""

def find_first_non_zero_index(data_sequence):
    """
    Finds the index of the first non-zero element in a sequence (list or numpy array).
    Returns 0 if all elements are zero or the sequence is empty.
    """
    # Use np.nonzero which returns a tuple of arrays, one for each dimension.
    # For a 1D array, we look at the first element of the tuple.
    non_zero_indices = np.nonzero(data_sequence)[0]
    if non_zero_indices.size > 0:
        # Return the first index found
        return non_zero_indices[0]
    else:
        # If no non-zero element is found (or sequence is empty), return 0
        return 0

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array sequence.
    """
    # Handle empty or single-element sequences
    if input_sequence.size <= 1:
        return input_sequence.copy() # Return a copy to avoid modifying original

    # 1. & 2. Separate the last element and the base sequence
    # Ensure input is treated as a numpy array
    if not isinstance(input_sequence, np.ndarray):
         input_sequence = np.array(input_sequence)

    last_element = input_sequence[-1]
    base_sequence = input_sequence[:-1]

    # 4. Evaluate the last element and determine insertion logic
    if last_element == 0:
        # 4.a Find the index for insertion (first non-zero or 0)
        insertion_index = find_first_non_zero_index(base_sequence)
        # Construct the output sequence using numpy insertion
        # np.insert(array, index, value)
        output_sequence = np.insert(base_sequence, insertion_index, last_element)
    else:
        # 4.b Insert the non-zero last element at the beginning
        # np.insert automatically handles index 0 correctly
        output_sequence = np.insert(base_sequence, 0, last_element)

    # 5. Return the constructed sequence
    return output_sequence
