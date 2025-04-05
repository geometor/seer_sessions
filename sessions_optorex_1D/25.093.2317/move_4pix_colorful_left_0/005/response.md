```python
import math # Included based on template, though not used in this specific logic.

"""
Transforms an input sequence of digits by identifying the contiguous block 
between the first and last non-zero digits, and shifting this block 4 positions 
to the left within a sequence of the same length, padding the remaining 
positions with zeros.
"""

def find_first_nonzero_index(data):
    """
    Finds the index of the first non-zero element in a list of numbers.

    Args:
        data: A list of numbers.

    Returns:
        The index of the first non-zero element, or None if all elements are zero.
    """
    for i, x in enumerate(data):
        # Check if the element is not zero
        if x != 0:
            return i
    # Return None if no non-zero element is found after checking all elements
    return None

def find_last_nonzero_index(data):
    """
    Finds the index of the last non-zero element in a list of numbers.

    Args:
        data: A list of numbers.

    Returns:
        The index of the last non-zero element, or None if all elements are zero.
    """
    # Iterate backwards from the end of the list to find the last non-zero element efficiently
    for i in range(len(data) - 1, -1, -1):
        # Check if the element is not zero
        if data[i] != 0:
            return i
    # Return None if no non-zero element is found (e.g., list contains only zeros)
    return None

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence. It identifies the block
    of digits between the first and last non-zero elements, shifts this block
    4 positions to the left, and places it into an output sequence of the same
    length, padded with zeros.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Determine the length of the input sequence
    n = len(input_sequence)

    # Initialize the output sequence with zeros of the same length as the input
    output_sequence = [0] * n

    # --- Step 1: Find the boundaries of the non-zero block ---
    # Find the index of the first non-zero digit
    first_nz_idx = find_first_nonzero_index(input_sequence)

    # If no non-zero digits are found (e.g., input is all zeros),
    # the output is already correctly initialized as all zeros.
    if first_nz_idx is None:
        return output_sequence

    # Find the index of the last non-zero digit.
    # This is guaranteed to exist if first_nz_idx is not None.
    last_nz_idx = find_last_nonzero_index(input_sequence)

    # --- Step 2: Extract the block ---
    # Extract the contiguous block of digits from the input sequence.
    # This block includes all digits from the first non-zero to the last non-zero, inclusive.
    # Python slicing input_sequence[start:end] extracts elements from start up to (but not including) end.
    # So, we need last_nz_idx + 1 as the end index for slicing.
    digit_block = input_sequence[first_nz_idx : last_nz_idx + 1]
    block_len = len(digit_block)

    # --- Step 3: Calculate the position for the block in the output ---
    # Calculate the target starting index for the block in the output sequence.
    # The rule observed from examples is to shift the block 4 positions to the left.
    output_start_idx = first_nz_idx - 4

    # --- Step 4: Place the block into the output sequence, handling boundaries ---
    # Calculate the effective start index for copying into the output sequence (must be >= 0)
    start_copy_idx_out = max(0, output_start_idx)
    
    # Calculate the effective end index for copying into the output sequence (must be <= n)
    # The theoretical end is output_start_idx + block_len
    end_copy_idx_out = min(n, output_start_idx + block_len)

    # Calculate the corresponding start index within the digit_block to copy from.
    # If output_start_idx was negative, we need to skip elements from the beginning of the block.
    start_copy_idx_block = max(0, -output_start_idx)

    # Calculate the corresponding end index within the digit_block to copy from.
    # This depends on how many elements actually fit into the output sequence.
    num_elements_to_copy = end_copy_idx_out - start_copy_idx_out
    end_copy_idx_block = start_copy_idx_block + num_elements_to_copy

    # Perform the copy only if there are elements to copy (i.e., the calculated range is valid)
    if num_elements_to_copy > 0:
        # Extract the relevant part of the digit_block
        block_to_copy = digit_block[start_copy_idx_block:end_copy_idx_block]
        # Assign this part to the calculated slice in the output sequence
        output_sequence[start_copy_idx_out:end_copy_idx_out] = block_to_copy

    # --- Step 5: Return the result ---
    return output_sequence
```