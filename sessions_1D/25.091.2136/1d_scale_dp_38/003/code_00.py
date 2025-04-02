import copy

"""
Identifies the first contiguous block of a non-white color (C1) in a 1D sequence 
and the very next non-white pixel (C2) that appears after this block. If the 
sequence of pixels strictly between the end of block C1 and the position of pixel C2 
consists entirely of white pixels (0), this sequence (the "gap") is filled with 
the color C1. Otherwise, the sequence remains unchanged.
"""

def find_first_non_white_block(grid):
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white block in a 1D grid (list).

    Args:
        grid: A list of integers representing pixel colors.

    Returns:
        A tuple (start_index, end_index, color) if a block is found, 
        otherwise (None, None, None).
    """
    start_index = -1
    end_index = -1
    color = -1
    in_block = False
    
    for i, pixel in enumerate(grid):
        # Start of a new block
        if pixel != 0 and not in_block:
            start_index = i
            end_index = i 
            color = pixel
            in_block = True
        # Continuation of the current block
        elif pixel == color and in_block:
            end_index = i
        # End of the current block (different color encountered)
        elif pixel != color and in_block:
            # We found the first block, stop searching
            break 
            
    if start_index == -1:
        # No non-white block found at all
        return None, None, None
    else:
        # Return the details of the first block found
        return start_index, end_index, color

def find_next_non_white_pixel(grid, start_search_index):
    """
    Finds the index and color of the first non-white pixel at or after 
    a given starting index in a 1D grid (list).

    Args:
        grid: A list of integers representing pixel colors.
        start_search_index: The index from which to start searching (inclusive).

    Returns:
        A tuple (index, color) if a non-white pixel is found, 
        otherwise (None, None).
    """
    for i in range(start_search_index, len(grid)):
        if grid[i] != 0:
            return i, grid[i] # Found the next non-white pixel
            
    return None, None # No non-white pixel found after the start index

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule: fills the gap 
    between the first non-white block and the next non-white pixel with the 
    block's color, if the gap is entirely white.

    Args:
        input_grid: A list or tuple of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # 1. Initialize the output grid as a mutable copy (list) of the input grid.
    # Ensure it's a list, even if input is tuple or numpy array slice
    output_grid = list(input_grid) 
    grid_len = len(output_grid)

    # 2. & 4. Find the first non-white block (C1).
    start_C1, end_C1, color_C1 = find_first_non_white_block(output_grid)

    # 3. If no non-white block is found, return the original grid.
    if start_C1 is None:
        return output_grid

    # 5. Find the next non-white pixel (C2) after the first block.
    search_start_index_C2 = end_C1 + 1
    index_C2, color_C2 = find_next_non_white_pixel(output_grid, search_start_index_C2)

    # 6. If no second non-white pixel is found, return the original grid.
    if index_C2 is None:
        return output_grid

    # 7. Define the gap indices.
    gap_start_index = end_C1 + 1
    gap_end_index = index_C2 - 1 # Inclusive end index for slicing/ranging

    # 8. Check if a gap exists.
    if gap_start_index > gap_end_index:
        # No gap between the block and the next pixel
        return output_grid

    # 9. Check if all pixels within the gap are white (0).
    is_gap_white = True
    for i in range(gap_start_index, gap_end_index + 1):
        if output_grid[i] != 0:
            is_gap_white = False
            break

    # 10. If the gap exists and is all white, fill it with color C1.
    if is_gap_white:
        for i in range(gap_start_index, gap_end_index + 1):
            output_grid[i] = color_C1

    # 11. Return the final (potentially modified) output grid.
    return output_grid