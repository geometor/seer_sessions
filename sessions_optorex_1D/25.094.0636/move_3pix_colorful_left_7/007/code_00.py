import numpy as np
from typing import List

"""
Transforms a sequence of 12 digits based on the following rule:
Identify the sub-sequence spanning from the first non-zero digit to the last non-zero digit in the input sequence.
Calculate a target start index by subtracting 3 (shift_amount) from the index of the first non-zero digit.
Construct the output sequence of length 12, initially filled with zeros.
Place the identified sub-sequence into the output sequence starting at the target start index.
Handle boundary conditions: If the target start index is negative, truncate the beginning of the sub-sequence before placing it (starting placement at index 0). If placing the sub-sequence exceeds the sequence length, truncate the end of the sub-sequence.
If the input sequence contains no non-zero digits, the output sequence is identical to the input sequence.
"""

def _find_non_zero_boundaries(sequence: np.ndarray) -> tuple[int, int]:
    """
    Finds the indices of the first and last non-zero elements in a NumPy array.

    Args:
        sequence: The input NumPy array.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero elements exist.
    """
    non_zero_indices = np.nonzero(sequence)[0]
    if len(non_zero_indices) == 0:
        return -1, -1
    else:
        return non_zero_indices[0], non_zero_indices[-1]

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list representing the transformed sequence of 12 integers.
    """
    # Define constants
    sequence_length = 12
    shift_amount = 3
    padding_value = 0

    # Convert input list to numpy array for efficient processing
    input_array = np.array(input_sequence, dtype=int)

    # --- Step 1 & 2: Find the boundaries of the non-zero sub-sequence ---
    start_index, end_index = _find_non_zero_boundaries(input_array)

    # --- Step 3: Handle the case where the input is all zeros ---
    if start_index == -1:
        # If no non-zero elements, return the original sequence as a list
        return input_sequence # Or list(input_array) which is equivalent

    # --- Step 4: Extract the sub-sequence ---
    sub_sequence = input_array[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # --- Step 5: Calculate the target starting index for the output ---
    target_start_index = start_index - shift_amount

    # --- Step 6: Create a new output array initialized with zeros ---
    output_array = np.full(sequence_length, padding_value, dtype=int)

    # --- Step 7: Determine placement boundaries and copy sub-sequence ---
    # Calculate the actual start and end indices for the destination (output) array
    dest_start = max(0, target_start_index)
    dest_end = min(sequence_length, target_start_index + sub_len)

    # Calculate the corresponding start and end indices for the source (sub_sequence) array
    source_start = max(0, -target_start_index) # How many elements to skip from the start of sub_sequence
    source_end = source_start + (dest_end - dest_start) # Calculate end based on how many elements actually fit

    # --- Step 8: Place the adjusted sub-sequence into the output array ---
    # Only perform the assignment if there's a valid range (destination start < destination end)
    if dest_start < dest_end:
        output_array[dest_start:dest_end] = sub_sequence[source_start:source_end]

    # --- Step 9: Return the final output sequence as a list ---
    return output_array.tolist()