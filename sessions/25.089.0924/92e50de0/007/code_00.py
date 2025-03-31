import numpy as np

"""
Identifies a grid structure based on regularly spaced horizontal and vertical lines of a single color (grid_color), which divide the grid into smaller, equal-sized 3x3 subgrids with a spacing of 4 pixels.
Locates a unique 3x3 pattern (source_pattern) within exactly one of these subgrids (the source_subgrid, identified by its row/column index r_idx, c_idx).
Creates an output grid by copying the input grid.
Replicates the source_pattern into specific subgrids in the output grid based on a parity rule: the pattern is copied to a subgrid at (r, c) if it's in the same row as the source (r == source_r_idx) and its column index c has the same parity (even/odd) as the source's column index (source_c_idx), OR if it's in the same column as the source (c == source_c_idx) and its row index r has the same parity as the source's row index (source_r_idx).
"""

def find_grid_color(grid):
    """
    Attempts to determine the color used for the grid lines.
    Assumes lines are regularly spaced (every 4th row/col).
    Returns the grid line color, or 0 (background) if no clear line color is found.
    """
    height, width = grid.shape
    spacing = 4 
    
    # Check specific likely line coordinates first for efficiency
    potential_coords = []
    if height > spacing - 1:
        potential_coords.extend([(spacing - 1, 0), (spacing - 1, min(spacing - 1, width - 1))])
    if width > spacing - 1:
         potential_coords.append((0, spacing - 1))

    for r, c in potential_coords:
        if 0 <= r < height and 0 <= c < width:
            color = grid[r, c]
            if color != 0: # If not background
                return color

    # Fallback: Scan likely line locations if specific checks failed
    for r in range(spacing - 1, height, spacing):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                return color
                
    for c in range(spacing - 1, width, spacing):
        for r in range(height):
             color = grid[r, c]
             if color != 0:
                 return color
                 
    # If no non-zero color found on expected lines, assume no grid or only background lines
    return 0 

def find_source_pattern_info(grid, grid_color):
    """
    Finds the unique non-background, non-gridline pattern and its location.
    Assumes 3x3 subgrids and spacing of 4.
    Returns the 3x3 pattern (as a numpy array), its subgrid row index, and its subgrid column index.
    Returns (None, -1, -1) if no source pattern is found.
    """
    height, width = grid.shape
    spacing = 4
    subgrid_size = 3
    
    # Calculate the number of subgrid rows/cols based on where a 3x3 grid could start
    num_subgrid_rows = height // spacing + (1 if height % spacing >= subgrid_size else 0)
    num_subgrid_cols = width // spacing + (1 if width % spacing >= subgrid_size else 0)

    for r_idx in range(num_subgrid_rows):
        for c_idx in range(num_subgrid_cols):
            # Define the top-left corner of the subgrid content area
            start_row = r_idx * spacing
            start_col = c_idx * spacing
            
            # Define the actual extent of the subgrid, careful of grid boundaries
            end_row = min(start_row + subgrid_size, height)
            end_col = min(start_col + subgrid_size, width)
            
            # Extract the subgrid slice
            subgrid = grid[start_row:end_row, start_col:end_col]

            # Check if the extracted slice is actually 3x3 
            # (Handles cases where grid dims aren't perfect multiples of spacing)
            if subgrid.shape != (subgrid_size, subgrid_size):
                 continue # Skip incomplete subgrids at the edges

            # Check if this subgrid contains a pattern color (not background, not grid color)
            is_source = False
            if np.any((subgrid != 0) & (subgrid != grid_color)):
                 is_source = True

            if is_source:
                # Return a copy of the pattern to avoid modification issues
                return np.copy(subgrid), r_idx, c_idx
                
    # If loop completes without finding a source
    return None, -1, -1 

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Define grid parameters (assuming constant from examples)
    spacing = 4
    subgrid_size = 3

    # Step 1: Find the color used for grid lines
    grid_color = find_grid_color(input_array)

    # Step 2 & 3: Find the unique source pattern and its subgrid coordinates
    source_pattern, source_subgrid_row, source_subgrid_col = find_source_pattern_info(
        input_array, grid_color
    )

    # If no source pattern found (e.g., input is blank or only grid lines), return the original grid
    if source_pattern is None:
        return output_array.tolist()

    # Step 4: Output grid is already initialized as a copy (output_array)

    # Step 5, 6, 7: Iterate through subgrids and replicate pattern based on parity rule
    num_subgrid_rows = height // spacing + (1 if height % spacing >= subgrid_size else 0)
    num_subgrid_cols = width // spacing + (1 if width % spacing >= subgrid_size else 0)

    for r_idx in range(num_subgrid_rows):
        for c_idx in range(num_subgrid_cols):
            
            # Determine if this subgrid should receive the pattern based on the parity rule
            replicate = False
            # Check Row Match + Column Parity Match
            if r_idx == source_subgrid_row and c_idx % 2 == source_subgrid_col % 2:
                replicate = True
            # Check Column Match + Row Parity Match
            elif c_idx == source_subgrid_col and r_idx % 2 == source_subgrid_row % 2:
                 replicate = True

            if replicate:
                # Calculate top-left pixel coordinates for placement
                start_row = r_idx * spacing
                start_col = c_idx * spacing
                
                # Calculate bottom-right bounds, respecting grid boundaries
                end_row = min(start_row + subgrid_size, height)
                end_col = min(start_col + subgrid_size, width)
                
                # Calculate the actual size of the pattern slice needed from source_pattern
                pattern_h = end_row - start_row
                pattern_w = end_col - start_col

                # Place the pattern slice (handles edge cases where subgrid space is < 3x3)
                if pattern_h > 0 and pattern_w > 0:
                    # Ensure source_pattern has the expected dimensions before slicing
                    if source_pattern.shape == (subgrid_size, subgrid_size):
                       output_array[start_row:end_row, start_col:end_col] = source_pattern[:pattern_h, :pattern_w]
                    # else: This case shouldn't happen if find_source_pattern_info worked correctly

    # Step 8: Return the modified grid as a list of lists
    return output_array.tolist()