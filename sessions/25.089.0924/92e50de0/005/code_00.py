import numpy as np

"""
Identifies a grid structure based on regularly spaced horizontal and vertical lines of a single color (grid_color), which divide the grid into smaller, equal-sized subgrids (assumed 3x3 based on examples).
Locates a unique pattern within exactly one of these subgrids (the source_pattern in the source_subgrid).
Creates an output grid by copying the input grid.
Replicates the source_pattern into all subgrids in the output grid that share the same row index OR the same column index as the source_subgrid within the grid-of-subgrids structure.
"""

def find_grid_color(grid):
    """
    Attempts to determine the color used for the grid lines.
    Assumes lines are regularly spaced (e.g., every 4th row/col).
    Returns the grid line color, or 0 (background) if no clear line color is found.
    """
    height, width = grid.shape
    # Assume spacing based on examples where lines are at index 3, 7, 11...
    # Subgrids are 3x3, lines + subgrid = 4 spacing
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

def find_source_pattern(grid, grid_color):
    """
    Finds the unique non-background, non-gridline pattern and its location.
    Assumes 3x3 subgrids and spacing of 4.
    Returns the 3x3 pattern (as a numpy array), its subgrid row index, and its subgrid column index.
    Returns (None, -1, -1) if no source pattern is found.
    """
    height, width = grid.shape
    spacing = 4
    subgrid_size = 3
    
    # Calculate the number of full subgrids that fit
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
            # (Handles cases where grid dims aren't perfect multiples)
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
    Transforms the input grid according to the specified pattern replication rule.
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
    source_pattern, source_subgrid_row, source_subgrid_col = find_source_pattern(
        input_array, grid_color
    )

    # If no source pattern found (e.g., input is blank or only grid lines), return the original grid
    if source_pattern is None:
        return output_array.tolist()

    # Step 4: Output grid is already initialized as a copy

    # Step 5, 6, 7: Iterate through subgrids and replicate pattern
    # Calculate number of subgrids again for the loop range
    num_subgrid_rows = height // spacing + (1 if height % spacing >= subgrid_size else 0)
    num_subgrid_cols = width // spacing + (1 if width % spacing >= subgrid_size else 0)


    for r_idx in range(num_subgrid_rows):
        for c_idx in range(num_subgrid_cols):
            
            # Determine if this subgrid should receive the pattern based on row/column match
            replicate = False
            if r_idx == source_subgrid_row or c_idx == source_subgrid_col:
                replicate = True

            if replicate:
                # Calculate top-left pixel coordinates for placement
                start_row = r_idx * spacing
                start_col = c_idx * spacing
                
                # Ensure we don't write outside the bounds of the output grid
                # This check is important if the grid dimensions aren't perfect multiples
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
                    # else: handle potential error if source_pattern wasn't 3x3? 
                    # Based on problem, it should always be 3x3 if found.


    # Step 8: Return the modified grid
    return output_array.tolist()