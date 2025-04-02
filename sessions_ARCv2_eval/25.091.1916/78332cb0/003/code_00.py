import numpy as np

def find_separators(grid):
    """Finds indices of horizontal and vertical separator lines/columns."""
    height, width = grid.shape
    h_separators = []
    v_separators = []
    separator_color = 6

    # Check for horizontal separators (full rows of separator_color)
    for r in range(height):
        if np.all(grid[r, :] == separator_color):
            h_separators.append(r)

    # Check for vertical separators (full columns of separator_color)
    for c in range(width):
        if np.all(grid[:, c] == separator_color):
            v_separators.append(c)

    return h_separators, v_separators

def transform(input_grid):
    """
    Transforms an input grid by rearranging subgrids based on separator orientation.

    The transformation rule depends on the type of magenta (6) separators present:
    1. If only vertical separators exist: Subgrids (read left-to-right) are stacked
       vertically in the same order, separated by horizontal magenta lines.
    2. If only horizontal separators exist: Subgrids (read top-to-bottom) are arranged
       horizontally in reverse order (bottom becomes left), separated by vertical
       magenta columns.
    3. If both horizontal and vertical separators exist (cross shape): The four
       subgrids (quadrants TL, BL, TR, BR) are stacked vertically in the order
       TL, BR, TR, BL, separated by horizontal magenta lines.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    separator_color = 6

    # Find separators
    h_separators, v_separators = find_separators(input_grid_np)

    # Determine separator type
    has_horizontal = len(h_separators) > 0
    has_vertical = len(v_separators) > 0

    subgrids = []
    output_grid = np.array([[]]) # Default empty grid

    # --- Case 1: Vertical Separators Only ---
    if has_vertical and not has_horizontal:
        # Define column boundaries for extraction, including grid edges
        col_boundaries = [0] + [v + 1 for v in v_separators] + [width]
        
        # Extract subgrids from left to right
        for i in range(len(col_boundaries) - 1):
            c_start = col_boundaries[i]
            # Adjust end boundary to exclude the separator column itself
            c_end = col_boundaries[i+1] - (1 if i < len(v_separators) else 0)
            if c_start < c_end: # Ensure valid slice
                subgrids.append(input_grid_np[:, c_start:c_end])

        if not subgrids: return [[]] # Handle case where no subgrids are found

        # Get dimensions from the first subgrid (assume uniformity)
        sg_h, sg_w = subgrids[0].shape
        num_subgrids = len(subgrids)
        
        # Calculate output dimensions: stacked vertically with horizontal separators
        out_h = num_subgrids * sg_h + (num_subgrids - 1)
        out_w = sg_w
        # Initialize output grid (using a background color like 7 might be safer than -1)
        output_grid = np.full((out_h, out_w), 7, dtype=int) 

        # Populate output grid: stack subgrids vertically, preserving order
        current_row = 0
        for i, sg in enumerate(subgrids):
            if sg.shape[0] == sg_h and sg.shape[1] == sg_w: # Basic shape check
                output_grid[current_row:current_row + sg_h, :] = sg
                current_row += sg_h
                # Add horizontal separator if not the last subgrid
                if i < num_subgrids - 1:
                    output_grid[current_row, :] = separator_color
                    current_row += 1
            else:
                 # Handle potential error: subgrids have different sizes
                 print(f"Warning: Subgrid {i} has unexpected shape {sg.shape}, expected ({sg_h}, {sg_w}).")
                 # Decide how to handle this - skip, error out, pad? For now, skip placing.


    # --- Case 2: Horizontal Separators Only ---
    elif has_horizontal and not has_vertical:
        # Define row boundaries for extraction, including grid edges
        row_boundaries = [0] + [h + 1 for h in h_separators] + [height]

        # Extract subgrids from top to bottom
        for i in range(len(row_boundaries) - 1):
            r_start = row_boundaries[i]
            # Adjust end boundary to exclude the separator row itself
            r_end = row_boundaries[i+1] - (1 if i < len(h_separators) else 0)
            if r_start < r_end: # Ensure valid slice
                subgrids.append(input_grid_np[r_start:r_end, :])

        if not subgrids: return [[]]

        # Reverse the order for horizontal arrangement
        subgrids.reverse()

        # Get dimensions from the first subgrid (assume uniformity)
        sg_h, sg_w = subgrids[0].shape
        num_subgrids = len(subgrids)

        # Calculate output dimensions: arranged horizontally with vertical separators
        out_h = sg_h
        out_w = num_subgrids * sg_w + (num_subgrids - 1)
        # Initialize output grid
        output_grid = np.full((out_h, out_w), 7, dtype=int)

        # Populate output grid: arrange subgrids horizontally in reversed order
        current_col = 0
        for i, sg in enumerate(subgrids):
             if sg.shape[0] == sg_h and sg.shape[1] == sg_w: # Basic shape check
                output_grid[:, current_col:current_col + sg_w] = sg
                current_col += sg_w
                # Add vertical separator if not the last subgrid
                if i < num_subgrids - 1:
                    output_grid[:, current_col] = separator_color
                    current_col += 1
             else:
                 # Handle potential error
                 print(f"Warning: Subgrid {i} has unexpected shape {sg.shape}, expected ({sg_h}, {sg_w}).")


    # --- Case 3: Both Horizontal and Vertical Separators (Cross) ---
    elif has_horizontal and has_vertical:
        # Assume one horizontal and one vertical separator for the cross based on examples
        # If multiple exist, this logic might need refinement, but examples show single cross.
        h_sep = h_separators[0]
        v_sep = v_separators[0]

        # Extract the four quadrants relative to the separators
        tl = input_grid_np[0:h_sep, 0:v_sep]
        bl = input_grid_np[h_sep+1:height, 0:v_sep]
        tr = input_grid_np[0:h_sep, v_sep+1:width]
        br = input_grid_np[h_sep+1:height, v_sep+1:width]

        # Order subgrids: TL, BR, TR, BL (as determined from Example 1 analysis)
        ordered_subgrids = [tl, br, tr, bl]

        # Filter out any potentially empty grids if separators are at edges (unlikely based on examples)
        subgrids = [sg for sg in ordered_subgrids if sg.size > 0]

        if not subgrids: return [[]]

        # Get dimensions from the first valid subgrid (assume uniformity)
        sg_h, sg_w = subgrids[0].shape
        num_subgrids = len(subgrids)

        # Calculate output dimensions: stacked vertically with horizontal separators
        out_h = num_subgrids * sg_h + (num_subgrids - 1)
        out_w = sg_w
        # Initialize output grid
        output_grid = np.full((out_h, out_w), 7, dtype=int)

        # Populate output grid: stack subgrids vertically in the specific TL, BR, TR, BL order
        current_row = 0
        for i, sg in enumerate(subgrids):
            if sg.shape[0] == sg_h and sg.shape[1] == sg_w: # Basic shape check
                output_grid[current_row:current_row + sg_h, :] = sg
                current_row += sg_h
                # Add horizontal separator if not the last subgrid
                if i < num_subgrids - 1:
                    output_grid[current_row, :] = separator_color
                    current_row += 1
            else:
                 # Handle potential error
                 print(f"Warning: Subgrid {i} has unexpected shape {sg.shape}, expected ({sg_h}, {sg_w}).")


    # --- Case 4: No Separators ---
    else:
        # If no separators, the behavior isn't defined by examples.
        # Returning the input grid as is, or an empty grid might be options.
        # Let's return the input grid copy for now.
        output_grid = input_grid_np.copy()

    # Convert final numpy array to list of lists for the expected ARC format
    return output_grid.tolist()