```python
import math
import collections

"""
The transformation rule identifies a single contiguous block of identical digits (not '0' or '2'), 
referred to as the "object block", and potentially swaps its position with an adjacent block 
of '0's (an "empty block"). The direction of the potential swap is determined by the relative 
positions of the object block and the number '2' (the "boundary marker"). The object block 
moves towards the '2' by swapping with the adjacent empty block that lies between it and the '2'. 
If the object block is already adjacent to the '2', or if there isn't an adjacent empty block 
between the object block and the '2', or if there isn't exactly one object block, 
no swap occurs, and the input remains unchanged.
"""

def _find_blocks(sequence):
    """Parses a sequence into a list of blocks."""
    if not sequence:
        return []
    
    blocks = []
    current_value = sequence[0]
    start_index = 0
    for i in range(1, len(sequence)):
        if sequence[i] != current_value:
            blocks.append({
                'value': current_value,
                'start': start_index,
                'end': i - 1,
                'length': i - start_index
            })
            current_value = sequence[i]
            start_index = i
    # Add the last block
    blocks.append({
        'value': current_value,
        'start': start_index,
        'end': len(sequence) - 1,
        'length': len(sequence) - start_index
    })
    return blocks

def _swap_block_contents(seq_list, block1, block2):
    """Swaps the contents of two blocks within a list representation of the sequence."""
    # Extract contents
    content1 = seq_list[block1['start']:block1['end'] + 1]
    content2 = seq_list[block2['start']:block2['end'] + 1]
    
    # Ensure lengths match for direct swap logic (should always match based on how blocks are defined)
    if block1['length'] != len(content1) or block2['length'] != len(content2):
        # This case should ideally not happen with contiguous blocks
        # but added as a safeguard or placeholder for more complex swaps later
        print("Warning: Block length mismatch during swap.") 
        return seq_list # Return original if something is wrong

    new_seq = seq_list[:] # Create a copy

    # Place content2 where content1 was
    for i in range(block2['length']):
        new_seq[block1['start'] + i] = content2[i]
        
    # Place content1 where content2 was
    for i in range(block1['length']):
         new_seq[block2['start'] + i] = content1[i]

    return new_seq


def transform(input_sequence):
    """
    Applies the block swapping transformation based on the object block's position 
    relative to the boundary marker '2'.

    Args:
        input_sequence: A list of integers.

    Returns:
        A list of integers representing the potentially transformed sequence.
    """
    
    # 1. Parse the input sequence into blocks
    blocks = _find_blocks(input_sequence)
    
    # 2. Identify the boundary marker ('2') block
    boundary_marker_block = None
    boundary_marker_index = -1
    for i, block in enumerate(blocks):
        if block['value'] == 2:
            boundary_marker_block = block
            boundary_marker_index = i
            break
            
    # If no boundary marker, return original sequence
    if boundary_marker_block is None:
        return input_sequence

    # 3. Identify all object blocks (not '0' or '2')
    object_blocks = []
    object_block_indices = []
    for i, block in enumerate(blocks):
        if block['value'] != 0 and block['value'] != 2:
            object_blocks.append(block)
            object_block_indices.append(i)

    # 4. If not exactly one object block, return original sequence
    if len(object_blocks) != 1:
        return input_sequence
        
    the_object_block = object_blocks[0]
    the_object_block_index = object_block_indices[0]

    # 5. Determine relative position and find adjacent empty block if needed
    
    output_sequence = list(input_sequence) # Work on a copy

    # 6. If object block is to the left of the boundary marker
    if the_object_block_index < boundary_marker_index:
        # Check block immediately to the right of the object block
        potential_empty_block_index = the_object_block_index + 1
        if potential_empty_block_index < len(blocks): # Ensure index is valid
            potential_empty_block = blocks[potential_empty_block_index]
            # Check if it's an empty block and located before the boundary marker
            if potential_empty_block['value'] == 0 and potential_empty_block_index < boundary_marker_index:
                 # Swap the contents in the sequence list
                 content_obj = output_sequence[the_object_block['start'] : the_object_block['end'] + 1]
                 content_empty = output_sequence[potential_empty_block['start'] : potential_empty_block['end'] + 1]
                 
                 output_sequence[the_object_block['start'] : the_object_block['start'] + potential_empty_block['length']] = content_empty
                 output_sequence[potential_empty_block['start'] : potential_empty_block['start'] + the_object_block['length']] = content_obj


    # 7. If object block is to the right of the boundary marker
    elif the_object_block_index > boundary_marker_index:
        # Check block immediately to the left of the object block
        potential_empty_block_index = the_object_block_index - 1
        if potential_empty_block_index >= 0: # Ensure index is valid
             potential_empty_block = blocks[potential_empty_block_index]
             # Check if it's an empty block and located after the boundary marker
             if potential_empty_block['value'] == 0 and potential_empty_block_index > boundary_marker_index:
                  # Swap the contents in the sequence list
                 content_obj = output_sequence[the_object_block['start'] : the_object_block['end'] + 1]
                 content_empty = output_sequence[potential_empty_block['start'] : potential_empty_block['end'] + 1]

                 output_sequence[potential_empty_block['start'] : potential_empty_block['start'] + the_object_block['length']] = content_obj
                 output_sequence[the_object_block['start'] : the_object_block['start'] + potential_empty_block['length']] = content_empty


    # 8. Return the (potentially) modified sequence
    return output_sequence

```