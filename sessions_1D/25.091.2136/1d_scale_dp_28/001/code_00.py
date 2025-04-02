import numpy as np

def transform(input_grid):
    """
    Identifies a single yellow (4) pixel in a 1D input grid.
    Scans leftwards from the yellow pixel to find a contiguous block of white (0) pixels (the gap).
    Continues scanning left until a non-white, non-yellow pixel is found (the source color).
    Fills the identified gap with the source color.
    Returns the modified grid.
    """
    # Ensure input is a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Since the examples show 1D arrays (or 1xN grids), flatten if necessary
    # or assume it's already 1D as presented. Let's work with it as 1D.
    # If it were always 1xN, we'd select the first row: grid_1d = grid[0]
    # But the input format suggests it might already be parsed as 1D.
    if grid.ndim > 1 and grid.shape[0] == 1:
        grid_1d = grid[0]
    elif grid.ndim == 1:
        grid_1d = grid
    else:
        # Handle unexpected dimensions if necessary, 
        # but based on examples, assume 1D or 1xN
        # For now, raise an error or return input unchanged if format is wrong.
        # Let's assume it's 1D for simplicity based on the examples' presentation.
         grid_1d = grid # Assume it's passed correctly as 1D

    # Initialize output_grid as a copy of the input
    output_grid_1d = grid_1d.copy()

    # 1. Find the location (index) of the single yellow (4) pixel.
    yellow_indices = np.where(grid_1d == 4)[0]
    if len(yellow_indices) == 0:
        # No yellow pixel found, return the original grid (or handle as error)
        # Reshape back if necessary before returning
        if grid.ndim > 1 and grid.shape[0] == 1:
             return output_grid_1d.reshape(1, -1)
        return output_grid_1d
        
    yellow_index = yellow_indices[0] # Assume only one yellow pixel as per examples

    # 2. Scan leftwards from the position immediately before the yellow pixel.
    current_index = yellow_index - 1
    gap_indices = []
    source_color = -1 # Initialize source color sentinel

    # 3. Identify the sequence of white (0) pixels (the gap).
    while current_index >= 0 and grid_1d[current_index] == 0:
        gap_indices.append(current_index)
        current_index -= 1

    # 4. Continue scanning leftwards until the first non-white pixel is found.
    # The loop above stops when grid_1d[current_index] != 0 or current_index < 0.
    # Check if we stopped because we found a non-white pixel.
    if current_index >= 0:
        # Check if the pixel found is not yellow (it should be the source color)
        if grid_1d[current_index] != 4: 
             source_color = grid_1d[current_index]
        # Else: handle case where block next to gap is yellow (unlikely based on examples)

    # 5. Modify the output grid: Change the color of all pixels within the identified gap.
    if source_color != -1 and gap_indices: # Proceed only if a source color and gap were found
        for idx in gap_indices:
            output_grid_1d[idx] = source_color

    # Reshape back to 1xN if the original input was 2D (1xN)
    if grid.ndim > 1 and grid.shape[0] == 1:
        return output_grid_1d.reshape(1, -1)
        
    # 6. Return the modified 1D grid.
    return output_grid_1d
