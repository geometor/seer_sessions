import copy

"""
Transforms a 1xN grid by finding a single maroon (9) marker pixel and a
contiguous block of a single non-white(0), non-maroon(9) color located entirely
to the left of the marker. The block is then moved ('reflected') to the right
side of the marker such that the distance (number of cells) between the
marker and the block's closest edge remains the same. The block's color and
length are preserved. The marker's position remains unchanged.
"""

def find_marker(row):
    """
    Finds the index of the first occurrence of the marker (9) in a list.

    Args:
        row: A list of integers representing the grid row.

    Returns:
        The index of the marker (9), or -1 if not found.
    """
    try:
        # Using list.index() is efficient for finding the first occurrence.
        return row.index(9)
    except ValueError:
        return -1 # Marker not found

def find_block_left_of_marker(row, marker_idx):
    """
    Finds the contiguous block of a single non-0, non-9 color located
    entirely to the left of the marker index.

    Args:
        row: A list of integers representing the grid row.
        marker_idx: The index of the marker (9).

    Returns:
        A tuple: (block_color, block_len, block_right_idx).
        Returns (None, 0, -1) if no such block is found.
        - block_color: The color (int) of the found block.
        - block_len: The length (int) of the found block.
        - block_right_idx: The index (int) of the rightmost pixel of the block.
    """
    block_color = None
    block_right_idx = -1
    block_len = 0
    
    # 1. Scan leftwards from marker_idx - 1 to find the right edge of the block
    #    We only consider indices strictly less than marker_idx.
    for i in range(marker_idx - 1, -1, -1):
        pixel = row[i]
        if pixel != 0 and pixel != 9:
            # Found the first pixel of a potential block (its rightmost edge)
            block_color = pixel
            block_right_idx = i
            block_len = 1
            break # Stop scanning for the right edge once found
            
    # If no non-background, non-marker pixel was found left of the marker
    if block_color is None:
        return None, 0, -1

    # 2. Scan leftwards from block_right_idx - 1 to find the full extent (left edge)
    #    The block must be contiguous and of the *same* color found.
    for i in range(block_right_idx - 1, -1, -1):
        if row[i] == block_color:
            block_len += 1
            # The start index would be 'i', but we only need length and right index
        else:
            # Found a different color or background/marker, the block ends at i+1
            break # Stop scanning left

    return block_color, block_len, block_right_idx

def transform(input_grid):
    """
    Applies the block reflection transformation to the input grid.

    Args:
        input_grid: A list containing a single list of integers (e.g., [[0, 5, 9, 0]]).

    Returns:
        A list containing a single list of integers representing the transformed grid,
        or a copy of the input grid if the transformation cannot be applied (e.g., no marker).
    """
    # Validate input structure and extract the row
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Return input copy if structure is not as expected, or handle error appropriately
        print("Warning: Input grid format is not a list containing a single list.")
        return copy.deepcopy(input_grid) 
        
    input_row = input_grid[0]
    grid_width = len(input_row)

    # Handle empty row edge case
    if grid_width == 0:
        return [[]]

    # 1. Initialize output row with background color
    output_row = [0] * grid_width

    # 2. Find the marker index
    marker_idx = find_marker(input_row)
    if marker_idx == -1:
        # If no marker, per ARC principles, often return input unchanged or minimal change.
        # Here, returning a copy seems reasonable as the core reference point is missing.
        print("Warning: Marker (9) not found. Returning input copy.")
        return copy.deepcopy(input_grid) 

    # 3. Place the marker in the output row
    # This ensures the marker is always present in the output at the same location.
    output_row[marker_idx] = 9

    # 4. Find the block left of the marker in the input row
    block_color, block_len, block_right_idx = find_block_left_of_marker(input_row, marker_idx)

    # 5. If a block was found, calculate its new position and place it
    if block_color is not None:
        # Calculate the distance 'd' - the offset from the block's right edge to the marker
        # d = marker_idx - block_right_idx
        # Example: block ends at 2, marker at 5. d = 5 - 2 = 3.
        distance = marker_idx - block_right_idx

        # Calculate the starting index for the block in the output grid
        # The block starts 'distance' units to the right of the marker.
        # Example: marker at 5, d = 3. Output starts at 5 + 3 = 8.
        output_start_idx = marker_idx + distance

        # Place the block into the output row
        for i in range(block_len):
            current_idx = output_start_idx + i
            # Check if the placement is within the grid bounds
            if 0 <= current_idx < grid_width:
                # Check if we are trying to overwrite the marker.
                # Based on the reflection logic (d >= 1), the block should always
                # start at marker_idx + 1 or further right, so it shouldn't overlap
                # the marker at marker_idx. We place the block color.
                # If overlap logic were needed, prioritize marker or block based on task spec.
                # Here, simple placement is sufficient.
                 output_row[current_idx] = block_color
            # else: Silently ignore parts of the block that fall outside the grid bounds

    # 6. Wrap the completed output row in a list and return
    return [output_row]