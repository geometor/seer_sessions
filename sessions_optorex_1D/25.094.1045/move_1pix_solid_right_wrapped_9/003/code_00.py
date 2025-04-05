import numpy as np

"""
Transforms a 1D NumPy array of integers based on the longest contiguous block of zeros.

1.  Receive the input as a 1D NumPy array of integers.
2.  Identify all contiguous subarrays containing only zeros. Record start index, end index, and length.
3.  If no zero blocks exist, return the original array.
4.  Find the block(s) with the greatest length. If tied, select the one starting earliest.
5.  Check if the selected block ends at the last index of the array.
6.  If at the end:
    a. Find the index of the first non-zero element before the block (default to index 0 if none).
    b. Remove the first zero of the block.
    c. Insert the removed zero at the found index.
7.  If not at the end:
    a. Get the element immediately following the block.
    b. Remove that element.
    c. Insert the removed element at the starting index of the block.
8.  Return the modified NumPy array.
"""

def find_zero_blocks(seq):
    """Finds all contiguous blocks of zeros in a list."""
    blocks = []
    start_index = -1
    n = len(seq)
    for i, val in enumerate(seq):
        if val == 0 and start_index == -1:
            # Start of a potential block
            start_index = i
        elif val != 0 and start_index != -1:
            # End of the current block
            end_index = i - 1
            blocks.append({'start': start_index, 'end': end_index, 'len': end_index - start_index + 1})
            start_index = -1 # Reset for next block
            
    # Check if the sequence ends with a block of zeros
    if start_index != -1:
        end_index = n - 1
        blocks.append({'start': start_index, 'end': end_index, 'len': end_index - start_index + 1})
        
    return blocks

def find_longest_block(blocks):
    """Finds the longest block of zeros from a list of blocks, selecting the first one in case of a tie."""
    if not blocks:
        return None
        
    max_len = 0
    # Find the maximum length among all blocks
    for block in blocks:
        if block['len'] > max_len:
            max_len = block['len']
            
    # Filter blocks that have the maximum length
    longest_blocks = [block for block in blocks if block['len'] == max_len]
    
    # Select the one with the smallest start index if there are multiple longest blocks
    # The min function naturally selects the first one if start indices are the same,
    # but we sort by start index explicitly if needed, though min handles it.
    selected_block = min(longest_blocks, key=lambda b: b['start'])
    return selected_block

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.
    """
    # Convert numpy array to list for easier manipulation (pop/insert)
    seq = input_grid.tolist()
    n = len(seq)
    
    # Handle empty input
    if n == 0:
        return input_grid # Return original empty array

    # 1. Identify all contiguous blocks of zeros
    zero_blocks = find_zero_blocks(seq)
    
    # 3. Handle case where there are no zeros
    if not zero_blocks:
        return input_grid # Return original array if no zeros

    # 2 & 4. Find the longest block (select first one if tie)
    selected_block = find_longest_block(zero_blocks)
    block_start = selected_block['start']
    block_end = selected_block['end']

    # Create a mutable copy (already done by tolist())
    output_seq = seq 

    # 5. Determine if the selected block is at the end of the sequence
    is_at_end = (block_end == n - 1)

    if is_at_end:
        # 6. Block is at the end
        
        # 6a. Find the index of the first non-zero element before the block
        target_index = 0 # Default if all preceding elements are zero
        found_non_zero = False
        for i in range(block_start):
            if output_seq[i] != 0:
                target_index = i
                found_non_zero = True
                break # Found the first non-zero element
                
        # 6b & 6c. Remove the first zero from the selected block
        # The element at block_start is the first zero.
        moved_zero = output_seq.pop(block_start) 
        
        # 6d. Insert this zero into the sequence at the target index
        # Note: If no non-zero was found before, target_index is 0, which is correct.
        output_seq.insert(target_index, moved_zero)
        
    else:
        # 7. Block is *not* at the end
        # This implies block_end + 1 < n, so an element exists after the block.
        
        # 7a. Identify the element immediately following the selected block
        element_to_move = output_seq[block_end + 1]
        
        # 7b. Remove this element from its position
        # Need to use the original index (block_end + 1) before potential shifts
        output_seq.pop(block_end + 1)
        
        # 7c. Insert the removed element at the starting index of the selected block
        output_seq.insert(block_start, element_to_move)

    # 8. Convert the modified list back to a NumPy array
    output_grid = np.array(output_seq, dtype=input_grid.dtype) # Preserve original dtype
    
    return output_grid