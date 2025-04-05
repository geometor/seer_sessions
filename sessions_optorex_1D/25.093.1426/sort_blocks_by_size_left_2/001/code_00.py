import re

"""
Identifies contiguous blocks of non-zero digits in the input sequence.
Sorts these blocks primarily by length (descending) and secondarily by their original starting index (ascending).
Constructs the output sequence by placing the sorted blocks, separated by single zeros,
and prepending enough zeros to match the original sequence length.
"""

def _parse_input(input_str):
    """Converts the space-separated input string to a list of integers."""
    return [int(x) for x in input_str.strip().split(' ')]

def _identify_blocks(input_sequence):
    """
    Identifies contiguous blocks of non-zero numbers in the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'elements' (list of ints), 'length' (int),
        and 'start_index' (int).
    """
    blocks = []
    current_block = []
    start_index = -1
    for i, num in enumerate(input_sequence):
        if num != 0:
            if not current_block:  # Start of a new block
                start_index = i
            current_block.append(num)
        else:
            if current_block:  # End of the current block
                blocks.append({
                    'elements': list(current_block), # Use list() for a copy
                    'length': len(current_block),
                    'start_index': start_index
                })
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

def _format_output(output_sequence):
    """Converts the output list of integers to a space-separated string."""
    return ' '.join(map(str, output_sequence))

def transform(input_str):
    """
    Applies the block identification, sorting, and reconstruction transformation.

    Args:
        input_str: The space-separated input string of digits.

    Returns:
        The transformed space-separated string of digits.
    """
    # 1. Parse the input string into a list of integers and get length
    input_sequence = _parse_input(input_str)
    original_length = len(input_sequence)

    # 2. Identify contiguous blocks of non-zero numbers
    blocks = _identify_blocks(input_sequence)

    # 3. Sort the blocks: primary key length (desc), secondary key start_index (asc)
    # Use a lambda function for the sort key: returns a tuple for sorting priorities
    # Negate length for descending order
    sorted_blocks = sorted(blocks, key=lambda b: (-b['length'], b['start_index']))

    # 4. Calculate total non-zero elements (N)
    total_non_zero_elements = sum(b['length'] for b in sorted_blocks)

    # 5. Calculate number of blocks (k)
    num_blocks = len(sorted_blocks)

    # 6. Calculate number of separating zeroes
    # Need k-1 separators if k > 0
    num_separators = max(0, num_blocks - 1)

    # 7. Calculate number of leading zeroes
    # Total length = leading_zeros + total_non_zero_elements + num_separators
    num_leading_zeros = original_length - total_non_zero_elements - num_separators
    # Ensure it's not negative (e.g., if input is all zeros)
    num_leading_zeros = max(0, num_leading_zeros)


    # 8. Initialize the output_sequence with leading zeroes
    output_sequence = [0] * num_leading_zeros

    # 9. Iterate through sorted blocks and append elements and separators
    for i, block in enumerate(sorted_blocks):
        output_sequence.extend(block['elements'])
        # Add separator zero if it's not the last block
        if i < num_blocks - 1:
            output_sequence.append(0)

    # Handle edge case: if input was all zeros, output should be all zeros
    # The logic above should handle this, as num_blocks=0, N=0, separators=0, leading_zeros=original_length
    # But double-check the length just in case, though it should be mathematically correct.
    # If the calculation somehow leads to a shorter sequence (e.g. due to unexpected input), pad at the end.
    # This shouldn't happen with the current logic but is a safeguard.
    while len(output_sequence) < original_length:
        output_sequence.append(0)
    # Or truncate if too long (also shouldn't happen)
    output_sequence = output_sequence[:original_length]


    # 10. Convert the output sequence back to a string
    output_str = _format_output(output_sequence)

    return output_str