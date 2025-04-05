"""
Rearranges a sequence of numbers (provided as a NumPy array) by consolidating 
contiguous non-zero blocks to the right end. The blocks are sorted by their 
length in descending order (stable sort) before being placed. Single zeros 
are used to separate the blocks in the output. Leading zeros are added to 
pad the sequence to match the original input length.
"""
import numpy as np

# Helper function to identify non-zero blocks
def _identify_non_zero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list or 1D NumPy array of numbers.

    Returns:
        A list of lists, where each inner list is a non-zero block.
    """
    # Convert numpy array to list for easier processing if needed
    if isinstance(sequence, np.ndarray):
        sequence = sequence.tolist()
        
    blocks = []
    current_block = []
    in_block = False
    for num in sequence:
        if num != 0:
            # Start or continue a block
            if not in_block:
                in_block = True
                current_block = [num]
            else:
                current_block.append(num)
        else:
            # End of a block (if currently in one)
            if in_block:
                blocks.append(current_block)
                in_block = False
                current_block = []
                
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks.append(current_block)
        
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input sequence according to the specified rules.
    """
    # 1. Receive input (already a NumPy array) and determine original length
    input_sequence = input_grid 
    original_length = len(input_sequence)

    # 2. Identify all contiguous blocks of non-zero numbers
    # The helper function preserves the content of each block.
    blocks = _identify_non_zero_blocks(input_sequence)

    # 3. Sort the identified blocks by length in descending order (stable sort)
    # Python's sorted() is stable, preserving relative order for equal lengths.
    sorted_blocks = sorted(blocks, key=len, reverse=True)

    # 4. Construct the core part of the output sequence (blocks + separators)
    core_output = []
    num_blocks = len(sorted_blocks)
    # Iterate through the sorted blocks.
    for i, block in enumerate(sorted_blocks):
        # Append the elements of the current block.
        core_output.extend(block)
        # If it's not the last block, append a single zero separator.
        if i < num_blocks - 1:
            core_output.append(0)

    # 5. Calculate the number of leading zeros needed for padding
    core_length = len(core_output)
    padding_zeros_count = original_length - core_length
    
    # Ensure padding count is not negative (e.g., if input was all zeros)
    padding_zeros_count = max(0, padding_zeros_count)

    # 6. Create the final output sequence by prepending padding zeros
    output_sequence = [0] * padding_zeros_count + core_output

    # 7. Return the final sequence as a NumPy array
    return np.array(output_sequence)