import re

"""
Parses an input string of 12 space-separated integers. Replaces contiguous blocks 
of the digit '5' in the first 10 elements based on the values of the last two 
elements (at indices 10 and 11). If one block of '5's exists, its elements are 
replaced with the value at index 11. If two blocks exist, the first block's elements 
are replaced with the value at index 10, and the second block's elements are 
replaced with the value at index 11. Elements other than '5' in the first 10 
positions, and the elements at indices 10 and 11, remain unchanged. Returns the 
transformed list of 12 integers.
"""

def find_five_blocks(sequence):
    """
    Finds contiguous blocks of the digit 5 in the first 10 elements of a sequence.

    Args:
        sequence: A list of integers (length at least 10).

    Returns:
        A list of tuples, where each tuple represents a block
        and contains (start_index, end_index_exclusive).
        Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    # Iterate through the first 10 elements
    for i in range(10):
        if sequence[i] == 5 and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif sequence[i] != 5 and in_block:
            # End of a block (before index i)
            in_block = False
            blocks.append((start_index, i))
            start_index = -1

    # Handle case where a block extends to the end (index 9)
    if in_block:
        blocks.append((start_index, 10)) # End index is exclusive

    return blocks

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
        Returns None or raises an error if input format is invalid.
    """
    # 1. Parse the input string into a list of 12 integers
    try:
        input_sequence = [int(x) for x in input_str.split()]
        if len(input_sequence) != 12:
            raise ValueError("Input string must contain exactly 12 integers.")
    except ValueError as e:
        # Handle potential errors during parsing or length check
        print(f"Error parsing input: {e}")
        return None # Or raise the error depending on desired behavior

    # 2. Create a copy of input_sequence called output_sequence
    output_sequence = list(input_sequence)

    # 3. Get the first control value, val1, from input_sequence at index 10
    val1 = input_sequence[10]

    # 4. Get the second control value, val2, from input_sequence at index 11
    val2 = input_sequence[11]

    # 5. Find all contiguous blocks of '5's in the first 10 elements
    five_blocks = find_five_blocks(input_sequence)

    # 6. Count the number of blocks found
    num_blocks = len(five_blocks)

    # 7. Apply transformations based on the number of blocks
    if num_blocks == 1:
        # If exactly one block was found
        start, end = five_blocks[0]
        # Iterate from start up to (but not including) end
        for i in range(start, end):
            # Set output_sequence element to val2
            output_sequence[i] = val2
    elif num_blocks == 2:
        # If exactly two blocks were found
        # Process first block
        start1, end1 = five_blocks[0]
        for i in range(start1, end1):
            # Set output_sequence element to val1
            output_sequence[i] = val1
        # Process second block
        start2, end2 = five_blocks[1]
        for j in range(start2, end2):
            # Set output_sequence element to val2
            output_sequence[j] = val2
    
    # Note: If num_blocks is 0 or > 2, no changes are made to the '5's, 
    #       though the examples only cover 1 or 2 blocks.
    #       Elements at index 10 and 11, and non-'5' elements in 0-9,
    #       are already correct due to the initial copy.

    # 8. Return the output_sequence
    return output_sequence