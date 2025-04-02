"""
Rearranges segments of a 1D pixel row within a grid.
Assumes the input grid contains exactly one row.
Identifies a 'main colored block' (first contiguous block of non-white, non-orange pixels),
an 'orange marker' (the first orange pixel after the main block), and the sequence
of 'intermediate whites' (all-white pixels strictly between the main block and orange marker).
The output row is constructed by moving the 'intermediate whites' to the beginning,
followed by any original 'leading whites' (pixels before the main block),
the 'main colored block', the 'orange marker', and any 'trailing elements'
(pixels after the orange marker).
The total length of the row remains constant.
"""

import numpy as np # Using numpy primarily for potential type compatibility in ARC env, list operations suffice.

def find_main_block(row):
    """Finds the first contiguous block of non-white, non-orange pixels."""
    n = len(row)
    for i in range(n):
        pixel = row[i]
        if pixel != 0 and pixel != 7:
            # Found the start of a potential main block
            start_index = i
            block_color = pixel
            # Find the end of this contiguous block
            end_index = i
            while end_index + 1 < n and row[end_index + 1] == block_color:
                end_index += 1
            return start_index, end_index, block_color
    return -1, -1, -1 # Not found

def find_orange_marker(row, start_search_index):
    """Finds the index of the first orange (7) pixel at or after start_search_index."""
    n = len(row)
    for i in range(start_search_index, n):
        if row[i] == 7:
            return i
    return -1 # Not found

def transform(input_grid):
    """
    Applies the segment rearrangement transformation to the first row of the input grid.
    """

    # Validate input format - expect a list of lists (grid)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        print("Warning: Invalid input grid format. Expected list of lists.")
        # Attempt to convert if it looks like a numpy array often used in ARC
        if hasattr(input_grid, 'tolist'):
            input_grid = input_grid.tolist()
        else:
             return [] # Cannot proceed

    # Assume the transformation applies only to the first row
    if len(input_grid) == 0:
        return []
        
    row = input_grid[0]
    n = len(row)

    # 1. Find the main colored block
    main_block_start, main_block_end, _ = find_main_block(row)

    # Handle case where no main block is found (return input unchanged as per previous logic)
    if main_block_start == -1:
        print("Warning: No main colored block found. Returning input grid.")
        # Ensure output is in the correct format (list of lists)
        return input_grid

    # 2. Find the orange marker after the main block
    orange_marker_index = find_orange_marker(row, main_block_end + 1)

    # Handle case where no orange marker is found (return input unchanged)
    if orange_marker_index == -1:
        print("Warning: No orange marker found after main block. Returning input grid.")
        return input_grid

    # 3. Identify intermediate whites (segment between main block end and orange marker)
    intermediate_whites_start = main_block_end + 1
    intermediate_whites_end = orange_marker_index
    intermediate_whites = row[intermediate_whites_start:intermediate_whites_end]

    # Optional: Validate that this segment contains only white pixels, as per pattern
    # if any(p != 0 for p in intermediate_whites):
    #    print("Warning: Non-white pixels found in intermediate segment.")
        # Depending on strictness, could return input or filter whites.
        # Sticking to extracting the whole segment between markers as per NL program.

    # 4. Identify other segments
    leading_whites = row[0:main_block_start]
    main_block = row[main_block_start : main_block_end + 1]
    orange_pixel = [row[orange_marker_index]] # Encapsulate in a list for concatenation
    trailing_elements = row[orange_marker_index + 1 : n]

    # 5. Reconstruct the output row
    output_row = intermediate_whites + leading_whites + main_block + orange_pixel + trailing_elements

    # 6. Format output as a grid (list of lists)
    output_grid = [output_row]

    return output_grid