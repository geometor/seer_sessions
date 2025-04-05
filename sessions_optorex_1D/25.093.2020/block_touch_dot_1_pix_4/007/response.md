```python
import math # common libraries are available
import numpy as np # common libraries are available

"""
Transforms a sequence of integers based on the following rule:
1. Find the start and end indices (`block_start_index`, `block_end_index`) of the first contiguous block of non-zero numbers.
2. If no non-zero block exists, the sequence remains unchanged.
3. Search the sequence *after* this block (from index `block_end_index + 1` onwards) for the first index `i` where `sequence[i]` is 0 and `sequence[i+1]` is non-zero.
4. If no such index `i` is found after the block, the sequence remains unchanged.
5. If such an index `i` is found, move the element `sequence[i]` (the zero) to the `block_start_index`. The elements originally from `block_start_index` to `i-1` are shifted one position to the right to accommodate the inserted zero.
6. Only the first non-zero block and the first qualifying zero found after it trigger this transformation.
"""


def parse_input(input_data) -> list[int]:
    """Parses the input into a list of integers."""
    # Handle potential numpy array input specifically
    if isinstance(input_data, np.ndarray):
        # Flatten if multi-dimensional, though examples suggest 1D/row focus
        input_list = input_data.flatten().tolist()
    # Handle string input
    elif isinstance(input_data, str):
        # Split the string by spaces and convert each part to an integer
        try:
            input_list = [int(x) for x in input_data.split()]
        except ValueError:
             # Handle case where input might already be formatted weirdly by test harness
             # This is a speculative fix based on previous errors.
             print(f"Warning: Could not parse '{input_data}' as space-separated ints. Attempting single int parse.")
             try:
                 # If it's just a single number string
                 input_list = [int(input_data)]
             except ValueError:
                 # If it contains non-numeric characters after split fail
                 print(f"Error: Final attempt failed to parse input '{input_data}'. Returning empty list.")
                 input_list = [] # Or raise a more specific error
    # Handle list input (ensure elements are integers)
    elif isinstance(input_data, list):
        input_list = [int(x) for x in input_data]
    else:
        raise TypeError(f"Unsupported input type: {type(input_data)}")
    return input_list

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_first_non_zero_block(sequence: list[int]) -> tuple[int, int]:
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.

    Args:
        sequence: The list of integers.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    n = len(sequence)

    # Find the start of the first block
    for i in range(n):
        if sequence[i] != 0:
            start_index = i
            break

    # If no non-zero number was found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of this block
    end_index = start_index
    for i in range(start_index + 1, n):
        if sequence[i] != 0:
            end_index = i
        else:
            # The block ends at the previous index
            break

    return start_index, end_index

def find_first_zero_pattern_after(sequence: list[int], start_scan_index: int) -> int:
    """
    Finds the index 'i' of the first '0 followed by non-zero' pattern,
    starting the scan from a given index.

    Args:
        sequence: The list of integers.
        start_scan_index: The index from which to start scanning (inclusive).

    Returns:
        The index `i` where sequence[i] == 0 and sequence[i+1] != 0,
        or -1 if no such pattern is found from the start_scan_index onwards.
    """
    n = len(sequence)
    # Iterate from the start scan index up to the second-to-last element
    for i in range(start_scan_index, n - 1):
        # Check the pattern: current element is 0, next is non-zero
        if sequence[i] == 0 and sequence[i+1] != 0:
            return i # Found the pattern at index i

    # If the loop completes without finding the pattern
    return -1

def transform(input_data) -> str:
    """
    Applies the transformation rule to the input sequence.
    Input can be a space-separated string, a list of ints, or a numpy array.
    Output is a space-separated string.
    """
    # 1. Parse Input
    # Convert input (string, list, or np.array) into a list of integers
    sequence = parse_input(input_data)
    if not sequence: # Handle empty list from parse error
        return ""

    # Create a mutable copy for potential modification
    output_sequence = list(sequence)

    # 2. Identify First Non-Zero Block
    # Find the start and end indices of the first sequence of non-zero numbers
    block_start_index, block_end_index = find_first_non_zero_block(output_sequence)

    # 3. Handle No Block Case
    # If no non-zero block was found, the sequence remains unchanged
    if block_start_index == -1:
        return format_output(output_sequence)

    # 4. Search for Pattern After Block
    # Define the starting point for the next search: immediately after the block
    scan_start_index = block_end_index + 1
    # Find the index of the first '0 followed by non-zero' after the block
    zero_to_move_index = find_first_zero_pattern_after(output_sequence, scan_start_index)

    # 5. Handle No Pattern Case
    # If the specific zero pattern wasn't found after the block, the sequence remains unchanged
    if zero_to_move_index == -1:
        return format_output(output_sequence)

    # 6. Perform Move Operation
    # Only execute if both the block and the pattern were found
    # a. Store the zero value and remove it from its current position
    zero_value = output_sequence.pop(zero_to_move_index)
    # b. Insert the stored zero at the beginning of the identified non-zero block
    output_sequence.insert(block_start_index, zero_value)

    # 7. Output Result
    # Convert the potentially modified list back into a space-separated string
    return format_output(output_sequence)
```