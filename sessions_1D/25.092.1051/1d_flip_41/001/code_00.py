import copy

"""
Identifies two adjacent blocks of non-white pixels in the input row: one block 
consisting of a single pixel and another block consisting of multiple pixels of 
the same color. Swaps the position of the single pixel with the multi-pixel 
block it is adjacent to. Specifically, the single pixel moves to the opposite 
end of the span originally occupied by the multi-pixel block, and the 
multi-pixel block shifts to occupy the remaining space, including the original 
position of the single pixel. Background pixels remain unchanged.
"""

def find_adjacent_blocks(row):
    """
    Finds a single pixel block adjacent to a multi-pixel block.

    Args:
        row: A list of integers representing the input row.

    Returns:
        A tuple containing information about the blocks if found:
        (single_pixel_index, single_pixel_color, 
         multi_block_start, multi_block_end, multi_block_color)
        Returns None if no such adjacent pair is found.
    """
    n = len(row)
    blocks = []
    current_block_start = -1
    current_block_color = -1

    # Iterate through the row to find all non-white blocks
    for i, pixel in enumerate(row):
        if pixel != 0:
            if current_block_start == -1:
                # Start of a new block
                current_block_start = i
                current_block_color = pixel
            elif pixel != current_block_color:
                # End of the current block, start of a new one
                blocks.append((current_block_start, i - 1, current_block_color))
                current_block_start = i
                current_block_color = pixel
        elif current_block_start != -1:
            # End of the current block (hit white pixel)
            blocks.append((current_block_start, i - 1, current_block_color))
            current_block_start = -1
            current_block_color = -1

    # Handle block ending at the edge of the row
    if current_block_start != -1:
        blocks.append((current_block_start, n - 1, current_block_color))

    # Find the adjacent single and multi-pixel blocks
    for i in range(len(blocks)):
        start1, end1, color1 = blocks[i]
        size1 = end1 - start1 + 1

        for j in range(len(blocks)):
            if i == j:
                continue
            start2, end2, color2 = blocks[j]
            size2 = end2 - start2 + 1

            # Check for adjacency
            is_adjacent = (end1 + 1 == start2) or (end2 + 1 == start1)

            if is_adjacent:
                # Check if one is size 1 and the other is size > 1
                if size1 == 1 and size2 > 1:
                    return (start1, color1, start2, end2, color2)
                elif size2 == 1 and size1 > 1:
                    return (start2, color2, start1, end1, color1)
                
    return None # No suitable adjacent pair found


def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A list of lists representing the input grid (expected to be 1xN).

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Ensure it's a single row grid for this specific task
    if len(input_grid) != 1:
        # Handle potential errors or unexpected input formats if necessary
        # For now, assume valid input based on examples
        return copy.deepcopy(input_grid) 

    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy

    # Find the relevant adjacent blocks
    block_info = find_adjacent_blocks(output_row)

    if block_info:
        single_idx, single_color, multi_start, multi_end, multi_color = block_info
        
        # Case 1: Single pixel is to the left of the multi-pixel block
        if single_idx < multi_start:
            # Place the single pixel at the rightmost end of the original multi-block span
            output_row[multi_end] = single_color
            # Shift the multi-pixel block to the left, occupying the original single pixel spot
            for i in range(multi_start, multi_end + 1):
                 output_row[single_idx + (i - multi_start)] = multi_color
                 
        # Case 2: Single pixel is to the right of the multi-pixel block
        else: # single_idx > multi_end
             # Place the single pixel at the leftmost end of the original multi-block span
            output_row[multi_start] = single_color
            # Shift the multi-pixel block to the right, occupying the original single pixel spot
            for i in range(multi_start, multi_end + 1):
                output_row[multi_start + 1 + (i - multi_start)] = multi_color

    # Return the result wrapped in a list, maintaining the grid structure
    return [output_row]
