```python
"""
Rearranges a sequence of numbers (provided as a NumPy array) by consolidating 
contiguous non-zero blocks to the right end. The blocks are sorted by their 
length in descending order (stable sort) before being placed. Single zeros 
are used to separate the blocks in the output. Leading zeros are added to 
pad the sequence to match the original input length.
"""

import numpy as np

# Helper function to identify non-zero blocks and their start indices
def _identify_non_zero_blocks_with_indices(sequence: np.ndarray) -> list[tuple[int, list[int]]]:
    """
    Identifies contiguous blocks of non-zero numbers and their start indices.

    Args:
        sequence: A 1D NumPy array of numbers.

    Returns:
        A list of tuples, where each tuple contains the start index 
        and the list of numbers in a non-zero block.
    """
    blocks_with_indices = []
    current_block = []
    in_block = False
    start_index = -1

    # Iterate through the sequence with index
    for i, num in enumerate(sequence):
        if num != 0:
            # Start or continue a block
            if not in_block:
                in_block = True
                current_block = [num]
                start_index = i # Record start index
            else:
                current_block.append(num)
        else:
            # End of a block (if currently in one)
            if in_block:
                blocks_with_indices.append((start_index, list(current_block))) # Store index and block
                in_block = False
                current_block = []
                start_index = -1
                
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks_with_indices.append((start_index, list(current_block))) # Store index and block
        
    return blocks_with_indices

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence.
    """
    # 1. Receive input (already a NumPy array) and determine original length
    input_sequence = input_grid 
    original_length = len(input_sequence)

    # 2. Identify all contiguous blocks of non-zero numbers and their start indices
    # The helper function preserves the content of each block and its starting position.
    blocks_with_indices = _identify_non_zero_blocks_with_indices(input_sequence)

    # 3. Sort the identified blocks: primary key = length (desc), secondary key = index (asc) for stability.
    # Python's sorted() is stable. We explicitly use the index as a secondary key 
    # to ensure stability if the primary key (negative length) is the same.
    sorted_blocks_with_indices = sorted(blocks_with_indices, key=lambda x: (-len(x[1]), x[0]))
    
    # Extract just the blocks in the correctly sorted order
    sorted_blocks = [block for index, block in sorted_blocks_with_indices]

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
    # Initialize output_grid as a list first
    output_sequence_list = [0] * padding_zeros_count + core_output

    # 7. Convert the final sequence to a NumPy array
    output_grid = np.array(output_sequence_list, dtype=input_grid.dtype) # Match input dtype
    
    return output_grid
```