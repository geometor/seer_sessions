"""
The transformation rule involves identifying subgrids within the input grid separated by delimiter lines (color 6, magenta). The orientation of these delimiter lines (Horizontal, Vertical, or Both) determines how the subgrids are extracted and reassembled.

1. Identify horizontal delimiter rows and vertical delimiter columns (composed entirely of magenta, color 6).
2. Determine the dominant delimiter orientation based on whether only horizontal, only vertical, or both types exist.
3. Extract the non-delimiter subgrids based on the delimiter locations, maintaining top-to-bottom, left-to-right reading order.
4. Apply reordering and assembly rules based on the delimiter orientation:
   - If Horizontal Only: Reverse the order of subgrids, arrange them horizontally, separated by vertical magenta lines.
   - If Vertical Only: Keep the original order of subgrids, stack them vertically, separated by horizontal magenta lines.
   - If Both: Reorder the subgrids (for the observed 2x2 case: Top-Left, Bottom-Right, Top-Right, Bottom-Left - indices [0, 3, 1, 2]), stack them vertically, separated by horizontal magenta lines. If not 4 subgrids, stack in original order.
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
    row_bounds = [-1] + sorted(list(set(row_delimiters))) + [height]
    col_bounds = [-1] + sorted(list(set(col_delimiters))) + [width]
    
    processed_rows = set(row_delimiters)
    processed_cols = set(col_delimiters)

    for i in range(len(row_bounds) - 1):
        r_start = row_bounds[i] + 1
        r_end = row_bounds[i+1]
        # Skip if this segment is exactly a delimiter row
        if r_start >= r_end or (r_end - r_start == 1 and r_start in processed_rows):
             continue

        for j in range(len(col_bounds) - 1):
            c_start = col_bounds[j] + 1
            c_end = col_bounds[j+1]
            # Skip if this segment is exactly a delimiter column
            if c_start >= c_end or (c_end - c_start == 1 and c_start in processed_cols):
                 continue
                
            # Check if the potential subgrid region overlaps with any delimiter
            is_delimiter_region = False
            for r in range(r_start, r_end):
                if r in processed_rows:
                    is_delimiter_region = True
                    break
            if is_delimiter_region: continue
            for c in range(c_start, c_end):
                if c in processed_cols:
                    is_delimiter_region = True
                    break
            if is_delimiter_region: continue

            subgrid = grid_np[r_start:r_end, c_start:c_end]
            # Ensure we don't extract empty arrays 
            if subgrid.size > 0:
                # Double check it doesn't contain ONLY delimiter color if it spans across where a delimiter *could* be
                if not np.all(subgrid == DELIMITER_COLOR):
                     subgrids.append(subgrid)

    # Filter out any subgrids that might have been captured incorrectly (e.g., consist only of delimiters)
    # This can happen with complex delimiter layouts not seen in examples. Refined extraction handles most cases.
    final_subgrids = [sg for sg in subgrids if not np.all(sg == DELIMITER_COLOR)]

    return final_subgrids


def transform(input_grid):
    """
    Transforms the input grid by extracting subgrids separated by magenta lines (6)
    and rearranging them based on the orientation of the delimiter lines in the input.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Step 1: Identify delimiter lines
    row_delimiters, col_delimiters = _find_delimiter_indices(input_np)

    # Step 2: Determine delimiter orientation
    delimiter_orientation = "None"
    if row_delimiters and not col_delimiters:
        delimiter_orientation = "Horizontal"
    elif col_delimiters and not row_delimiters:
        delimiter_orientation = "Vertical"
    elif row_delimiters and col_delimiters:
        delimiter_orientation = "Both"

    # Step 3 & 4: Extract subgrids in reading order
    subgrids = _extract_subgrids(input_np, row_delimiters, col_delimiters)

    # Handle cases with no subgrids found
    if not subgrids:
        # Return empty grid or original? Let's return empty list for now.
        return [] 

    # Assume all subgrids are the same size and get dimensions from the first one
    subgrid_h, subgrid_w = subgrids[0].shape 

    # Step 5 & 6: Apply transformation rule based on delimiter orientation
    output_np = None

    if delimiter_orientation == "Horizontal":
        # Reverse order, arrange horizontally, use vertical delimiters
        subgrids.reverse() # Reverse the order
        output_components = []
        delimiter_col = np.full((subgrid_h, 1), DELIMITER_COLOR, dtype=int)
        for i, sg in enumerate(subgrids):
            output_components.append(sg)
            if i < len(subgrids) - 1:
                output_components.append(delimiter_col)
        if output_components: # Ensure list is not empty before hstack
             output_np = np.hstack(output_components)

    elif delimiter_orientation == "Vertical":
        # Preserve order, stack vertically, use horizontal delimiters
        output_components = []
        delimiter_row = np.full((1, subgrid_w), DELIMITER_COLOR, dtype=int)
        for i, sg in enumerate(subgrids):
            output_components.append(sg)
            if i < len(subgrids) - 1:
                output_components.append(delimiter_row)
        if output_components: # Ensure list is not empty before vstack
            output_np = np.vstack(output_components)

    elif delimiter_orientation == "Both":
        # Specific reorder (TL, BR, TR, BL) if 4 subgrids, otherwise treat as Vertical
        if len(subgrids) == 4:
             # Indices based on reading order: 0=TL, 1=TR, 2=BL, 3=BR
             # Desired order: TL (0), BR (3), TR (1), BL (2)
             ordered_subgrids = [subgrids[0], subgrids[3], subgrids[1], subgrids[2]]
        else: 
             # Fallback for non 2x2 grids with both delimiters: Use Vertical logic
             ordered_subgrids = subgrids 

        # Stack vertically, potentially reordered, use horizontal delimiters
        output_components = []
        delimiter_row = np.full((1, subgrid_w), DELIMITER_COLOR, dtype=int)
        for i, sg in enumerate(ordered_subgrids):
            output_components.append(sg)
            if i < len(ordered_subgrids) - 1:
                output_components.append(delimiter_row)
        if output_components: # Ensure list is not empty before vstack
            output_np = np.vstack(output_components)
            
    else: # delimiter_orientation == "None" or unexpected case
         # No delimiters found, or failed to extract subgrids properly. Return input? Empty?
         # Returning input seems safest if no transformation is defined.
         return input_grid


    # Convert final numpy array back to list of lists
    if output_np is not None:
        output_grid = output_np.tolist()
    else:
        # Fallback if construction failed (e.g., empty components list)
        output_grid = [] # Or return input_grid?

    return output_grid