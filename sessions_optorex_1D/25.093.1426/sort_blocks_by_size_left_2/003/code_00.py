"""
Identifies contiguous blocks of non-zero digits in the input sequence (list/array of integers).
Sorts these blocks primarily by length (descending) and secondarily by their original starting index (ascending).
Constructs the output sequence by placing the sorted blocks, separated by single zeros,
and prepending enough zeros to match the original sequence length.
"""

import numpy as np # Importing numpy as the environment might provide arrays

def _identify_blocks(input_sequence):
    """
    Identifies contiguous blocks of non-zero numbers in the input sequence.

    Args:
        input_sequence: A list or numpy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'elements' (list of ints), 'length' (int),
        and 'start_index' (int).
    """
    blocks = []
    current_block = []
    start_index = -1
    # Iterate through the input sequence with index tracking
    for i, num in enumerate(input_sequence):
        if num != 0:
            # Start of a new block
            if not current_block:
                start_index = i
            # Accumulate the number
            current_block.append(num)
        else:
            # End of the current block (if one exists)
            if current_block:
                # Finalize the block and add to list
                blocks.append({
                    'elements': list(current_block), # Store a copy
                    'length': len(current_block),
                    'start_index': start_index
                })
                # Reset for next block
                current_block = []
                start_index = -1

    # Add the last block if the sequence ends with non-zero numbers
    if current_block:
        blocks.append({
            'elements': list(current_block),
            'length': len(current_block),
            'start_index': start_index
        })
    return blocks

def transform(input_sequence):
    """
    Applies the block identification, sorting, and reconstruction transformation.

    Args:
        input_sequence: A list or numpy array of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # 1. Receive the input_sequence and record its length.
    # Ensure input is treated as a list for consistency within the function
    input_list = list(input_sequence)
    original_length = len(input_list)

    # 2-5. Identify contiguous blocks of non-zero numbers.
    blocks = _identify_blocks(input_list)

    # 6. Sort the blocks: primary key length (desc), secondary key start_index (asc).
    # Use a lambda function for the sort key: returns a tuple for sorting priorities.
    # Negate length for descending order.
    sorted_blocks = sorted(blocks, key=lambda b: (-b['length'], b['start_index']))

    # 7. Calculate total number of non-zero elements (N).
    total_non_zero_elements = sum(b['length'] for b in sorted_blocks)

    # 8. Calculate number of blocks (k).
    num_blocks = len(sorted_blocks)

    # 9. Calculate number of separating zeroes required between blocks.
    # Need k-1 separators if k > 0.
    num_separators = max(0, num_blocks - 1)

    # 10. Calculate number of leading zeroes.
    # Total length = leading_zeros + total_non_zero_elements + num_separators
    num_leading_zeros = original_length - total_non_zero_elements - num_separators
    # Ensure it's not negative (e.g., if input is all zeros or calculation error)
    num_leading_zeros = max(0, num_leading_zeros)

    # 11. Initialize the output_sequence with leading zeroes.
    output_sequence = [0] * num_leading_zeros

    # 12. Iterate through sorted blocks and append elements and separators.
    for i, block in enumerate(sorted_blocks):
        # 12a. Append the elements of the block.
        output_sequence.extend(block['elements'])
        # 12b. Add separator zero if it's not the last block.
        if i < num_blocks - 1:
            output_sequence.append(0)

    # 13. Ensure the output_sequence has the correct length.
    # Pad with zeros if it's somehow too short (shouldn't happen with correct logic).
    while len(output_sequence) < original_length:
        output_sequence.append(0)
    # Truncate if it's somehow too long (also shouldn't happen).
    output_sequence = output_sequence[:original_length]

    # 14. Return the transformed sequence.
    # The environment might expect a specific type (e.g., numpy array),
    # but returning a standard list is generally safe.
    # If a numpy array is strictly required uncomment the next line:
    # return np.array(output_sequence)
    return output_sequence