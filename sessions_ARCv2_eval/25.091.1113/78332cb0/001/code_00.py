"""
The transformation rule involves identifying subgrids within the input grid separated by delimiter lines (color 6, magenta). 
The input grid is segmented into these subgrids. 
The subgrids are then extracted and reassembled into the output grid based on the aspect ratio of the input grid.

1. Identify horizontal and vertical delimiter lines (rows/columns composed entirely of magenta, color 6).
2. Use these delimiters to define and extract the non-delimiter subgrids. Store them in a list in top-to-bottom, left-to-right reading order.
3. Determine the input grid's aspect ratio (height vs. width).
4. Apply reordering and assembly rules based on the aspect ratio:
   - If Tall (Height > Width): Stack subgrids vertically in their original order, separated by horizontal magenta lines.
   - If Wide (Width > Height): Reverse the order of subgrids, arrange them horizontally, separated by vertical magenta lines.
   - If Square (Height == Width): Reorder the subgrids (for the observed 2x2 case: Top-Left, Bottom-Right, Top-Right, Bottom-Left), stack them vertically, separated by horizontal magenta lines.
5. Construct the final output grid.
"""

import numpy as np

DELIMITER_COLOR = 6

def _find_delimiter_indices(grid_np):
    """Finds the indices of rows and columns entirely composed of the delimiter color."""
    height, width = grid_np.shape
    row_indices = [r for r in range(height) if np.all(grid_np[r, :] == DELIMITER_COLOR)]
    col_indices = [c for c in range(width) if np.all(grid_np[:, c] == DELIMITER_COLOR)]
    return row_indices, col_indices

def _extract_subgrids(grid_np, row_delimiters, col_delimiters):
    """Extracts subgrids based on delimiter indices, maintaining reading order."""
    subgrids = []
    height, width = grid_np.shape

    # Add boundaries for easier iteration
    row_bounds = [-1] + row_delimiters + [height]
    col_bounds = [-1] + col_delimiters + [width]

    for i in range(len(row_bounds) - 1):
        r_start = row_bounds[i] + 1
        r_end = row_bounds[i+1]
        # Skip if this segment is a delimiter row itself
        if r_start >= r_end:
            continue

        for j in range(len(col_bounds) - 1):
            c_start = col_bounds[j] + 1
            c_end = col_bounds[j+1]
            # Skip if this segment is a delimiter column itself
            if c_start >= c_end:
                continue
                
            subgrid = grid_np[r_start:r_end, c_start:c_end]
            # Ensure we don't extract empty arrays if delimiters are adjacent
            if subgrid.size > 0:
                subgrids.append(subgrid)
                
    return subgrids

def transform(input_grid):
    """
    Transforms the input grid by extracting subgrids separated by magenta lines (6)
    and rearranging them based on the input grid's aspect ratio.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Step 1 & 2: Identify delimiters and extract subgrids
    row_delimiters, col_delimiters = _find_delimiter_indices(input_np)
    subgrids = _extract_subgrids(input_np, row_delimiters, col_delimiters)

    if not subgrids: # Handle cases with no subgrids or only delimiters
        # This case isn't explicitly covered by examples, returning input might be safe,
        # or an empty grid, depending on implied rules. Let's assume input for now.
        # Or perhaps return based on aspect ratio still? Needs clarification.
        # For now, let's try returning a minimal structure if possible or input.
         if height > width : # tall
             return [[DELIMITER_COLOR]*width] if subgrids else input_grid
         elif width > height: # wide
             return [[DELIMITER_COLOR]]*height if subgrids else input_grid
         else: # square
             return [[DELIMITER_COLOR]*width] if subgrids else input_grid


    subgrid_h, subgrid_w = subgrids[0].shape # Assume all subgrids are the same size

    # Step 3 & 4: Determine aspect ratio and apply rules
    if height > width:  # Tall input
        # Stack vertically, original order, horizontal delimiter
        output_components = []
        delimiter_row = np.full((1, subgrid_w), DELIMITER_COLOR, dtype=int)
        for i, sg in enumerate(subgrids):
            output_components.append(sg)
            if i < len(subgrids) - 1:
                output_components.append(delimiter_row)
        output_np = np.vstack(output_components)

    elif width > height:  # Wide input
        # Arrange horizontally, reversed order, vertical delimiter
        subgrids.reverse() # Reverse the order
        output_components = []
        delimiter_col = np.full((subgrid_h, 1), DELIMITER_COLOR, dtype=int)
        for i, sg in enumerate(subgrids):
            output_components.append(sg)
            if i < len(subgrids) - 1:
                output_components.append(delimiter_col)
        output_np = np.hstack(output_components)

    else:  # Square input (assuming 2x2 layout as seen in example 1)
        # Reorder: TL (0), BR (3), TR (1), BL (2) -> indices [0, 3, 1, 2]
        # Check if the number of subgrids matches the expected 4 for the square rule
        if len(subgrids) == 4:
             ordered_subgrids = [subgrids[0], subgrids[3], subgrids[1], subgrids[2]]
        else: 
             # Fallback for square grids not matching the 2x2 pattern: Use 'Tall' logic
             ordered_subgrids = subgrids # Keep original order

        # Stack vertically, specific order, horizontal delimiter
        output_components = []
        delimiter_row = np.full((1, subgrid_w), DELIMITER_COLOR, dtype=int)
        for i, sg in enumerate(ordered_subgrids):
            output_components.append(sg)
            if i < len(ordered_subgrids) - 1:
                output_components.append(delimiter_row)
        output_np = np.vstack(output_components)

    # Step 5: Convert final numpy array back to list of lists
    output_grid = output_np.tolist()
    return output_grid