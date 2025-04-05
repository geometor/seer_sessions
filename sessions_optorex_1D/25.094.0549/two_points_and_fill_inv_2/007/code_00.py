import numpy as np

"""
Transforms a 1-dimensional NumPy array of single-digit integers based on contiguous blocks (runs) of identical non-zero digits.

1.  Create a copy of the input array (`input_sequence`) called `output_sequence`.
2.  Iterate through the `input_sequence` using an index `i`.
3.  If the element at `input_sequence[i]` is 0, skip to the next element.
4.  If the element is non-zero, identify the start (`start_index`) and end (`end_index`) of the contiguous block of that same digit.
5.  Calculate the length of the block (`block_length`).
6.  If `block_length` is greater than 2, set the elements in the `output_sequence` from index `start_index + 1` up to (but not including) `end_index` to 0.
7.  Advance the iteration index `i` to the position immediately after the identified block (`end_index + 1`).
8.  Return the modified `output_sequence`.
"""

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the block transformation rule to the input NumPy array.

    Args:
        input_sequence: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array (it should be based on previous error)
    if not isinstance(input_sequence, np.ndarray):
      # Handle potential list input, although testing showed ndarray
      input_sequence = np.array(input_sequence)

    # 1. Create a copy of the input array
    output_sequence = np.copy(input_sequence)
    n = len(input_sequence)

    # Handle empty input
    if n == 0:
        return output_sequence

    # 2. & 5. Iterate through the sequence using index i
    i = 0
    while i < n:
        # 3. If the element is 0, skip it
        if input_sequence[i] == 0:
            i += 1
            continue

        # 4. Found non-zero, identify the block
        start_index = i
        block_value = input_sequence[i]
        end_index = i

        # Look ahead to find the end of the contiguous block
        j = i + 1
        while j < n and input_sequence[j] == block_value:
            end_index = j
            j += 1

        # 5. Calculate block length
        block_length = end_index - start_index + 1

        # 6. If block length > 2, zero out the middle elements in the output sequence
        if block_length > 2:
            # Iterate through the indices strictly between start_index and end_index
            # Using array slicing for efficiency
            output_sequence[start_index + 1 : end_index] = 0

        # 7. Advance the main iterator past the processed block
        i = end_index + 1

    # 8. Return the modified output sequence
    return output_sequence