import numpy as np

"""
Transforms the input grid based on the following rules:

1. Identifies a "Central Structure," which is a contiguous horizontal sequence of non-white pixels in the first row (row 0).
2. Identifies "Peripheral Pixels," which are all other non-white pixels in the grid (rows > 0).
3. Associates each Peripheral Pixel with a column in the Central Structure based on matching colors.
4. Replicates the Central Structure pattern vertically downwards into rows above the topmost Peripheral Pixel.
5. Draws horizontal lines connecting each Peripheral Pixel to its associated column in the Central Structure.
6. Draws vertical lines downwards from each column of the Central Structure. The line extends to the row of the lowest Peripheral Pixel associated with that column's color. If no Peripheral Pixel is associated with a column's color, the vertical line extends to the bottom of the grid.
"""

def find_central_structure(grid):
    """
    Finds the contiguous horizontal block of non-white pixels in the first row.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (start_col, end_col, structure_map)
               start_col: Starting column index of the structure.
               end_col: Ending column index of the structure (inclusive).
               structure_map: Dictionary mapping column index to color {col: color}.
               Returns (None, None, None) if no structure is found.
    """
    rows, cols = grid.shape
    if rows == 0:
        return None, None, None

    row0 = grid[0, :]
    non_white_indices = np.where(row0 != 0)[0]

    if len(non_white_indices) == 0:
        return None, None, None

    start_col = non_white_indices[0]
    end_col = non_white_indices[0]
    structure_map = {}

    # Check for contiguity
    for i in range(len(non_white_indices) - 1):
        if non_white_indices[i+1] != non_white_indices[i] + 1:
             # If non-contiguous non-white cells are found in row 0,
             # the definition might be ambiguous. Based on examples,
             # we assume the first contiguous block is the structure.
             # Or potentially just the segment between the first and last non-zero.
             # Let's assume the first contiguous block for now.
             end_col = non_white_indices[i]
             break
    else:
        # If the loop finishes without breaking, the structure is fully contiguous
        end_col = non_white_indices[-1]

    # Build the map for the identified structure range
    for c in range(start_col, end_col + 1):
        color = grid[0, c]
        if color != 0: # Should always be true within this range based on logic
             structure_map[c] = color
        # If there are zeros within the start/end range, the definition might need refinement.
        # Based on examples, the structure seems solid non-zero.

    if not structure_map: # If only zeros were found between start and end (unlikely)
        return None, None, None

    return start_col, end_col, structure_map

def find_peripheral_pixels(grid):
    """
    Finds all non-white pixels not in the first row.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples [(row, col, color), ...].
    """
    rows, cols = grid.shape
    peripheral_pixels = []
    for r in range(1, rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                peripheral_pixels.append((r, c, color))
    return peripheral_pixels


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    output_grid = np.copy(input_grid_np)

    # 1. Identify the Central Structure
    start_col, end_col, structure_map = find_central_structure(input_grid_np)

    if start_col is None:
        # No central structure found, return the original grid?
        # Based on examples, a structure always exists.
        return input_grid # Or raise an error, depending on expected behavior

    # Create reverse map for color to target column
    color_to_target_col = {color: c for c, color in structure_map.items()}

    # 2. Identify Peripheral Pixels
    peripheral_pixels = find_peripheral_pixels(input_grid_np)

    # 3. Determine Target Column for each Peripheral Pixel & find min_p_row
    min_p_row = rows # Default to grid height if no peripherals
    peripherals_with_targets = []
    if peripheral_pixels:
        min_p_row = min(p[0] for p in peripheral_pixels)
        for r, c, color in peripheral_pixels:
            target_col = color_to_target_col.get(color)
            if target_col is not None:
                 peripherals_with_targets.append({'row': r, 'col': c, 'color': color, 'target_col': target_col})
            # else: handle case where peripheral color not in structure (ignore for now)


    # 4. Replicate the Central Structure vertically
    for r_rep in range(1, min_p_row):
        for c_struct in range(start_col, end_col + 1):
             output_grid[r_rep, c_struct] = structure_map[c_struct]

    # 5 & 6. Draw Horizontal and Vertical Lines
    max_row_for_column = {c: -1 for c in structure_map.keys()}

    # 5a. Process peripherals: draw horizontal lines and update max rows
    for p in peripherals_with_targets:
        p_row, p_col, p_color, c_target = p['row'], p['col'], p['color'], p['target_col']

        # Draw horizontal line segment
        if p_col < c_target:
            for c_fill in range(p_col + 1, c_target): # Fill between pixel and target col
                 output_grid[p_row, c_fill] = p_color
        elif p_col > c_target:
            for c_fill in range(c_target + 1, p_col): # Fill between target col and pixel
                 output_grid[p_row, c_fill] = p_color

        # Update max row for the target column
        max_row_for_column[c_target] = max(max_row_for_column[c_target], p_row)

    # 6a. Draw vertical lines based on max rows or grid height
    for c_struct in range(start_col, end_col + 1):
        struct_color = structure_map[c_struct]
        
        # Determine end row for the vertical line
        r_end = max_row_for_column.get(c_struct, -1) # Use .get() in case a structure col had no associated peripherals
        if r_end == -1: # No peripheral pixel targeted this column
            r_end = rows - 1 # Extend to the bottom
            
        # Draw vertical line segment downwards from row 1
        # Note: Row 0 is already set, replication handles rows 1 to min_p_row-1
        # This loop potentially redraws over replicated parts, which is fine.
        # It also fills below the lowest peripheral pixel row if needed.
        for r_fill in range(1, r_end + 1):
            # We only fill if the target row is below any potential replication
            # No, the logic should just fill down to r_end. Replication happens first.
            output_grid[r_fill, c_struct] = struct_color


    return output_grid.tolist()