```python
import re

def find_non_zero_block_indices(int_list):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero numbers are found.
    """
    start_index = -1
    end_index = -1
    for i, num in enumerate(int_list):
        if num != 0:
            if start_index == -1:
                start_index = i
            end_index = i # Keep updating end_index for the last non-zero
    return start_index, end_index

def transform(input_str):
    """
    Identifies a contiguous block of non-zero digits in the input sequence,
    shifts this block 3 positions to the left (or to the beginning if the shift
    would result in a negative index), and fills the remaining positions with zeros,
    primarily at the end.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing space-separated single-digit integers representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize the output list with zeros
    output_list = [0] * n

    # Find the start and end indices of the non-zero block
    start_index, end_index = find_non_zero_block_indices(input_list)

    # If no non-zero block is found (all zeros), return the input string as is
    # or a string of zeros of the same length. Let's return formatted zeros.
    if start_index == -1:
        return " ".join(map(str, output_list))

    # Extract the non-zero block
    non_zero_block = input_list[start_index : end_index + 1]
    block_len = len(non_zero_block)

    # Calculate the new starting index for the block, shifting left by 3
    # Ensure the new start index is not negative
    new_start_index = max(0, start_index - 3)

    # Calculate the new end index (exclusive) for slicing
    # Ensure it doesn't exceed the list bounds
    new_end_index_exclusive = min(n, new_start_index + block_len)

    # Place the non-zero block into the output list at the new position
    # Adjust length if shifting causes truncation (though not expected based on examples)
    place_len = new_end_index_exclusive - new_start_index
    output_list[new_start_index : new_end_index_exclusive] = non_zero_block[:place_len] # Place the block (or part of it if truncated)

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
```