import numpy as np

"""
Transforms an input grid by identifying subgrids separated by magenta (6) lines (either horizontal or vertical, or both). 
The subgrids are then extracted, reordered based on the type of separation, and recombined into an output grid with magenta separators inserted.

Separation Types and Reordering:
1.  Horizontal Separators Only: Subgrids (originally stacked vertically) are reordered bottom-to-top and concatenated horizontally with vertical magenta separators.
2.  Vertical Separators Only: Subgrids (originally arranged horizontally) maintain their left-to-right order and are stacked vertically with horizontal magenta separators.
3.  Both Horizontal and Vertical Separators (assuming a 2x2 grid): Subgrids (TL, TR, BL, BR) are reordered as TL, BR, TR, BL and stacked vertically with horizontal magenta separators.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    separator_color = 6

    # --- 1. Find Separators ---
    h_sep_indices = [r for r in range(height) if np.all(grid[r, :] == separator_color)]
    v_sep_indices = [c for c in range(width) if np.all(grid[:, c] == separator_color)]

    # --- 2. Determine Split Type ---
    split_type = None
    if h_sep_indices and v_sep_indices:
        split_type = "both"
    elif h_sep_indices:
        split_type = "horizontal_only"
    elif v_sep_indices:
        split_type = "vertical_only"
    else:
        # Should not happen based on examples, but handle defensively
        return input_grid # Or raise an error

    # --- 3. Extract Subgrids ---
    subgrids = []
    row_starts = [0] + [r + 1 for r in h_sep_indices]
    row_ends = [r for r in h_sep_indices] + [height]
    col_starts = [0] + [c + 1 for c in v_sep_indices]
    col_ends = [c for c in v_sep_indices] + [width]

    for r_start, r_end in zip(row_starts, row_ends):
        for c_start, c_end in zip(col_starts, col_ends):
            if r_start < r_end and c_start < c_end: # Ensure valid slice
                subgrid = grid[r_start:r_end, c_start:c_end]
                # Check if the subgrid actually contains non-separator colors before adding
                if not np.all(subgrid == separator_color):
                     subgrids.append(subgrid)

    if not subgrids:
        # Handle case where separators might exist but no valid subgrids are found
        return [] # Or raise error, or return input_grid

    subgrid_h, subgrid_w = subgrids[0].shape

    # --- 4. Reorder Subgrids ---
    ordered_subgrids = []
    if split_type == "both":
        # Assuming a 2x2 arrangement: TL, TR, BL, BR -> TL, BR, TR, BL
        if len(subgrids) == 4:
             ordered_subgrids = [subgrids[0], subgrids[3], subgrids[1], subgrids[2]]
        else:
             # Fallback or error if not 2x2
             ordered_subgrids = subgrids # Default to original order if assumption fails
    elif split_type == "horizontal_only":
        # Reverse vertical order (bottom-to-top)
        ordered_subgrids = subgrids[::-1]
    elif split_type == "vertical_only":
        # Maintain horizontal order (left-to-right)
        ordered_subgrids = subgrids

    # --- 5. Construct Output Grid ---
    output_grid = None
    if split_type == "both" or split_type == "vertical_only":
        # Stack vertically, separate with horizontal lines
        separator_line = np.full((1, subgrid_w), separator_color, dtype=int)
        parts_to_stack = []
        for i, sg in enumerate(ordered_subgrids):
            parts_to_stack.append(sg)
            if i < len(ordered_subgrids) - 1:
                parts_to_stack.append(separator_line)
        if parts_to_stack:
            output_grid = np.vstack(parts_to_stack)

    elif split_type == "horizontal_only":
        # Concatenate horizontally, separate with vertical lines
        separator_line = np.full((subgrid_h, 1), separator_color, dtype=int)
        parts_to_stack = []
        for i, sg in enumerate(ordered_subgrids):
            parts_to_stack.append(sg)
            if i < len(ordered_subgrids) - 1:
                parts_to_stack.append(separator_line)
        if parts_to_stack:
             output_grid = np.hstack(parts_to_stack)

    # Convert back to list of lists if output_grid was created
    if output_grid is not None:
        return output_grid.tolist()
    else:
        # Handle cases where no output was constructed (e.g., error state)
        return [] # Or input_grid.tolist() or raise an error
