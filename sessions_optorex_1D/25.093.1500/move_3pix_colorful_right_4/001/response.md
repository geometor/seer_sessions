```python
import re

"""
Identifies the first contiguous block of non-zero digits in a sequence of 12 digits.
Shifts this block 3 positions to the right within a new sequence of 12 zeros.
If no non-zero block exists, returns the sequence of zeros.
The relative order of the digits within the block is preserved.
"""

def find_nonzero_block(sequence):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
        end_index is inclusive.
    """
    start_index = -1
    end_index = -1
    in_block = False
    for i, digit in enumerate(sequence):
        if digit != 0 and not in_block:
            start_index = i
            in_block = True
        if digit == 0 and in_block:
            end_index = i - 1
            break
        # Handle block extending to the end
        if digit != 0 and in_block and i == len(sequence) - 1:
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        return start_index, end_index
    elif start_index != -1 and end_index == -1: # Handle single non-zero digit at the end
         return start_index, start_index
    else:
        return None

def transform(input_str: str) -> str:
    """
    Transforms the input sequence string by shifting the first non-zero block right by 3 positions.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed space-separated integers.
    """
    # Parse the input string into a list of integers
    # Example: "0 1 3 7 3 5 1 7 3 0 0 0" -> [0, 1, 3, 7, 3, 5, 1, 7, 3, 0, 0, 0]
    input_sequence = [int(x) for x in input_str.split()]
    sequence_length = len(input_sequence)

    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length

    # Find the non-zero block in the input sequence
    block_indices = find_nonzero_block(input_sequence)

    # If a block is found, perform the shift
    if block_indices:
        start_index, end_index = block_indices
        shift_amount = 3
        new_start_index = start_index + shift_amount

        # Extract the block
        block = input_sequence[start_index : end_index + 1]

        # Place the block into the output sequence at the new position
        # Ensure the placement doesn't exceed the bounds (though examples suggest it won't)
        for i, digit in enumerate(block):
            target_index = new_start_index + i
            if target_index < sequence_length:
                output_sequence[target_index] = digit
            # else: block goes out of bounds, part of it is truncated (not observed in examples)

    # If no block is found, the output remains all zeros (or could return input if required)
    # The current logic correctly handles the all-zero input case implicitly,
    # as find_nonzero_block returns None, and output_sequence remains [0]*12.
    # Example train_2's input '3 0 0 0 ...' -> block = [3], start=0, end=0. new_start=3. output[3]=3.
    # Example train_4's input '... 3 0 0 0' -> block = [3], start=8, end=8. new_start=11. output[11]=3.

    # Format the output sequence back into a space-separated string
    output_str = " ".join(map(str, output_sequence))
    return output_str

```