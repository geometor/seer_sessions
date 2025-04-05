import re # Used for potential pattern matching if needed, although simple iteration is used here.

"""
Transforms a sequence of integers based on the longest contiguous block of zeros.

1. Find all contiguous blocks of zeros in the input sequence.
2. Identify the block(s) with the maximum length. If there's a tie, choose the block that starts at the earliest index.
3. If no zero blocks exist, return the original sequence.
4. Check if the selected block ends at the last index of the sequence.
5. If the block is at the end:
   a. Find the index of the first non-zero element that appears *before* the start of the block. If all elements before the block are zero, use index 0.
   b. Remove the first zero from the selected block (at the block's start index).
   c. Insert this zero at the index found in step 5a.
6. If the block is *not* at the end:
   a. Get the element immediately following the end of the block.
   b. Remove that element from its position.
   c. Insert the removed element at the starting index of the selected block.
7. Return the modified sequence as a space-separated string.
"""

def find_zero_blocks(seq):
    """Finds all contiguous blocks of zeros in a sequence."""
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
    """Finds the longest block of zeros, selecting the first one in case of a tie."""
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
    selected_block = min(longest_blocks, key=lambda b: b['start'])
    return selected_block
    
def find_first_preceding_non_zero_index(seq, block_start):
    """Finds the index of the first non-zero element before the block_start index."""
    target_index = 0 # Default if all preceding elements are zero
    found = False
    for i in range(block_start):
        if seq[i] != 0:
            target_index = i
            found = True
            break # Found the first non-zero element
            
    # If no non-zero element was found before the block, target_index remains 0.
    # This handles cases like [0, 0, 0, 5, 5, 0, 0] -> block starts at 5, target_index should be 0.
    # And [1, 2, 0, 0, 0] -> block starts at 2, first non-zero is at index 0. target_index = 0.
    # And [0, 1, 2, 0, 0, 0] -> block starts at 3, first non-zero is at index 1. target_index = 1.
            
    # Correction: The logic finds the index of the *first* non-zero element *overall* that is before the block.
    # Let's re-verify the description and examples.
    # Train 1: [0, 0, 5, ..., 0, 0, 0] -> Block starts at 7. First non-zero before 7 is at index 2. Target = 2. Correct.
    # Train 3: [0, 4, ..., 0, 0, 0] -> Block starts at 7. First non-zero before 7 is at index 1. Target = 1. Correct.
    # Train 4: [0, 0, 0, 1, ..., 0, 0, 0] -> Block starts at 8. First non-zero before 8 is at index 3. Target = 3. Correct.
    # The function implementation seems correct based on the examples.
    
    return target_index

def transform(input_str):
    """
    Applies the transformation rule to the input sequence string.
    """
    # Parse input string into a list of integers
    seq = [int(x) for x in input_str.split()]
    n = len(seq)
    
    # Handle empty input
    if n == 0:
        return ""

    # 1. Identify all contiguous blocks of zeros
    zero_blocks = find_zero_blocks(seq)
    
    # 3. Handle case where there are no zeros
    if not zero_blocks:
        return input_str # Return original sequence as string

    # 2. Find the longest block (select first one if tie)
    selected_block = find_longest_block(zero_blocks)
    block_start = selected_block['start']
    block_end = selected_block['end']

    # Create a mutable copy of the sequence
    output_seq = list(seq) 

    # 4. Determine if the selected block is at the end of the sequence
    is_at_end = (block_end == n - 1)

    if is_at_end:
        # 5. Block is at the end
        
        # 5a. Find the index of the first non-zero element before the block
        # If all preceding are 0, target_index will be 0.
        target_index = 0 
        for i in range(block_start):
            if output_seq[i] != 0:
                target_index = i
                break # Found the first non-zero element
                
        # 5b. Take the first zero from the selected block
        # 5c. Remove this zero from its original position
        moved_zero = output_seq.pop(block_start) 
        
        # 5d. Insert this zero into the sequence at the target index
        output_seq.insert(target_index, moved_zero)
        
    else:
        # 6. Block is *not* at the end
        # This implies block_end + 1 < n, so an element exists after the block.
        
        # 6a. Identify the element immediately following the selected block
        element_to_move = output_seq[block_end + 1]
        
        # 6b. Remove this element from its position
        output_seq.pop(block_end + 1)
        
        # 6c. Insert the removed element at the starting index of the selected block
        output_seq.insert(block_start, element_to_move)

    # 7. Return the modified sequence as a space-separated string
    output_str = " ".join(map(str, output_seq))
    return output_str
