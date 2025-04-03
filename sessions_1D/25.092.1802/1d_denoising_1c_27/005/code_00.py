"""
Transforms a 1D input grid (represented as a flat list or a list containing one list) 
by identifying contiguous horizontal blocks of the single non-background color. 
It calculates the size of each block and keeps only the block(s) with the maximum size. 
All pixels belonging to smaller blocks are changed to the background color (0). 
The output grid format matches the input grid format.
"""

import numpy as np

def find_contiguous_blocks_1d(arr_1d, target_color):
    """
    Finds contiguous blocks of a specific color in a 1D array.

    Args:
        arr_1d (np.array): The 1D input array.
        target_color (int): The color of the blocks to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block:
              {'start': start_index, 'end': end_index, 'size': size}. 
              Returns empty list if no blocks found.
    """
    blocks = []
    start_index = -1
    n = len(arr_1d)
    for i in range(n):
        pixel = arr_1d[i]
        # Start of a potential block
        if pixel == target_color and start_index == -1:
            start_index = i
        # End of a block (either color changes or end of array)
        if pixel != target_color and start_index != -1:
            end_index = i - 1
            size = end_index - start_index + 1
            blocks.append({'start': start_index, 'end': end_index, 'size': size})
            start_index = -1 # Reset

    # Check if a block extends to the very end of the array
    if start_index != -1:
        end_index = n - 1
        size = end_index - start_index + 1
        blocks.append({'start': start_index, 'end': end_index, 'size': size})

    return blocks

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous block(s)
    of the non-background color.

    Args:
        input_grid (list): A list representing the 1xN input grid.
                           Can be a flat list [p1, p2,...] or a list of list [[p1, p2,...]].

    Returns:
        list: A list representing the 1xN output grid in the same format as the input.
    """
    # --- Input Handling and Preprocessing ---

    # Determine input format and convert to a 1D numpy array
    is_list_of_lists = isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list)
    
    if is_list_of_lists:
        # Handle empty list within list case
        if len(input_grid) == 0 or len(input_grid[0]) == 0: 
             return input_grid # Return empty input as is
        input_arr = np.array(input_grid[0], dtype=int)
    else: # Assume flat list
        # Handle empty flat list case
        if len(input_grid) == 0: 
            return input_grid # Return empty input as is
        input_arr = np.array(input_grid, dtype=int)

    # Define background color
    background_color = 0

    # --- Color and Block Identification ---

    # Find unique non-background colors
    unique_colors = np.unique(input_arr[input_arr != background_color])

    # If no non-background color exists, return the original input format
    if len(unique_colors) == 0:
        return input_grid # Return original format

    # Assume there's only one non-background color as per task description
    primary_color = unique_colors[0]

    # Find all contiguous blocks of the primary color using the helper function
    blocks = find_contiguous_blocks_1d(input_arr, primary_color)

    # If no blocks of the primary color are found, return the original input format
    # (This case is unlikely if unique_colors found something, but safe to check)
    if not blocks:
        return input_grid # Return original format

    # --- Max Size Calculation ---

    # Find the maximum size among all found blocks
    # Handle the case where blocks list might be empty although unique_colors was not
    max_size = 0
    if blocks:
        max_size = max(block['size'] for block in blocks)
        
    # If max_size remains 0 (e.g., only single pixels and they were all removed? - unlikely based on logic but safe)
    # or if no blocks were found initially, return background grid.
    if max_size == 0:
         output_arr = np.full_like(input_arr, background_color)
         # Convert back to original format
         if is_list_of_lists:
             return [output_arr.tolist()]
         else:
             return output_arr.tolist()


    # --- Output Grid Construction ---

    # Create the output grid, initialized with the background color
    output_arr = np.full_like(input_arr, background_color)

    # Iterate through the blocks again
    # Fill the output grid with pixels belonging only to the largest block(s)
    for block in blocks:
        if block['size'] == max_size:
            # Fill the segment corresponding to the largest block with the primary color
            output_arr[block['start'] : block['end'] + 1] = primary_color

    # --- Output Formatting ---

    # Convert the numpy array back to the original input list format
    if is_list_of_lists:
        output_grid = [output_arr.tolist()]
    else:
        output_grid = output_arr.tolist()

    return output_grid