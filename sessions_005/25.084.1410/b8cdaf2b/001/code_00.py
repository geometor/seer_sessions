import numpy as np

"""
Identify the lowest horizontal segment in the input grid containing at least two different non-white colors.
Determine the 'central' color (C1) and the 'flanking' color (C2) within this segment. The flanking color (C2) is the color found at the horizontal extremities of the non-white portion of the segment. The central color (C1) is a non-white color within the segment that is different from C2.
For each pixel in the segment having the flanking color (C2), located at (r_seg, c_flank), trace vertically upwards in column c_flank.
Find the highest row index r_target < r_seg such that the pixel at (r_target, c_flank) is white (0), and all pixels between r_target and r_seg (exclusive) in that column are also white.
Change the color of the pixel at (r_target, c_flank) in the output grid to the central color (C1).
If no such white pixel exists above a flanking pixel (either the column is blocked immediately above or the segment is in the top row), no change is made for that flanking pixel column.
The output grid is the input grid modified with these placed pixels.
"""

def find_key_segment(grid):
    """
    Finds the lowest row containing a contiguous horizontal segment of non-white
    pixels with at least two distinct colors.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (row_index, col_start, col_end) of the segment, or (None, None, None) if not found.
    """
    height, width = grid.shape
    for r in range(height - 1, -1, -1):
        non_white_indices = np.where(grid[r, :] != 0)[0]
        if len(non_white_indices) > 0:
            col_start = np.min(non_white_indices)
            col_end = np.max(non_white_indices)

            # Check for contiguity: all cells between col_start and col_end must be non-white
            is_contiguous = np.all(grid[r, col_start:col_end+1] != 0)

            if is_contiguous:
                segment_pixels = grid[r, col_start:col_end+1]
                unique_colors = set(p for p in segment_pixels if p != 0) # Re-check non-white unique colors
                if len(unique_colors) >= 2:
                    # Found the segment
                    return r, col_start, col_end
    # No segment found matching criteria
    return None, None, None

def get_segment_colors(grid, r_seg, col_start, col_end):
    """
    Determines the central and flanking colors of the key segment.

    Args:
        grid (np.array): The input grid.
        r_seg (int): Row index of the segment.
        col_start (int): Start column index of the segment.
        col_end (int): End column index of the segment.

    Returns:
        tuple: (central_color, flanking_color), or (None, None) if colors cannot be determined as expected.
    """
    color_at_start = grid[r_seg, col_start]
    color_at_end = grid[r_seg, col_end]

    # Based on examples, the color at the absolute start and end of the contiguous non-white segment defines the flanking color.
    if color_at_start != color_at_end:
        # This case is not observed in training data. If it occurs, the rule might be different.
        # Assuming the flanking color must be consistent at both ends.
        return None, None 

    flanking_color = color_at_start # C2

    central_color = None
    # Find a color within the segment bounds (inclusive) that is different from the flanking color.
    for c in range(col_start, col_end + 1):
        pixel = grid[r_seg, c]
        if pixel != 0 and pixel != flanking_color:
            central_color = pixel # C1
            break # Assume only one such central color exists based on examples.

    if central_color is None:
        # This implies the segment only contains the flanking color,
        # which should have been filtered out by find_key_segment needing >= 2 colors.
        return None, None

    return central_color, flanking_color

def find_flanking_pixel_cols(grid, r_seg, col_start, col_end, flanking_color):
    """
    Finds the column indices of all pixels within the segment that have the flanking color.

    Args:
        grid (np.array): The input grid.
        r_seg (int): Row index of the segment.
        col_start (int): Start column index of the segment.
        col_end (int): End column index of the segment.
        flanking_color (int): The flanking color C2.

    Returns:
        list: A list of column indices.
    """
    cols = []
    for c in range(col_start, col_end + 1):
        if grid[r_seg, c] == flanking_color:
            cols.append(c)
    return cols

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # 1. Identify the key segment
    r_seg, col_start, col_end = find_key_segment(grid)

    if r_seg is None:
        # No key segment found, return the original grid
        return output_grid.tolist()

    # 2. Determine Central (C1) and Flanking (C2) colors
    central_color, flanking_color = get_segment_colors(grid, r_seg, col_start, col_end)

    if central_color is None or flanking_color is None:
        # Could not determine colors as expected, return original grid
        return output_grid.tolist()

    # 3. Find all pixels in the segment with the flanking color
    flanking_cols = find_flanking_pixel_cols(grid, r_seg, col_start, col_end, flanking_color)

    # 4. Process each flanking pixel column
    for c_flank in flanking_cols:
        target_row = -1
        # Trace upwards from the row *above* the segment's row
        for r in range(r_seg - 1, -1, -1):
            if grid[r, c_flank] == 0: # If the cell is white (color 0)
                target_row = r       # This is the highest potential target row found so far
            else:                    # If we hit a non-white cell (an obstacle)
                break                # Stop tracing up in this column

        # 5. If a valid target row was found (i.e., at least one white cell above)
        if target_row != -1:
            # Place the central color (C1) at the highest white position found
            output_grid[target_row, c_flank] = central_color

    # Convert the result back to a list of lists
    return output_grid.tolist()