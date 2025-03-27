import numpy as np

"""
Identifies a horizontal azure (8) divider line in the input grid. 
Locates a 6x6 pattern block (green=3, white=0) and a 2x2 color key block (non-white, non-azure) on opposite sides of the divider.
Creates a 6x6 output grid. 
For each cell in the output grid:
- If the corresponding cell in the pattern block is white (0), the output cell is white (0).
- If the corresponding cell in the pattern block is green (3), the output cell's color is determined by its quadrant within the 6x6 grid and the colors from the 2x2 key block:
    - Top-left quadrant (rows 0-2, cols 0-2): Uses the top-left color of the key block.
    - Top-right quadrant (rows 0-2, cols 3-5): Uses the top-right color of the key block.
    - Bottom-left quadrant (rows 3-5, cols 0-2): Uses the bottom-left color of the key block.
    - Bottom-right quadrant (rows 3-5, cols 3-5): Uses the bottom-right color of the key block.
"""

def find_azure_divider(grid):
    """Finds the row index of the horizontal line made entirely of azure (8)."""
    for r_idx, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return r_idx
    return -1 # Should not happen based on examples

def find_block(grid, size, condition_func, exclude_coords=None):
    """Finds the top-left corner (r, c) of the first block matching size and condition."""
    height, width = grid.shape
    block_rows, block_cols = size
    if exclude_coords is None:
        exclude_coords = (-1, -1, -1, -1) # Dummy coords that won't match

    for r in range(height - block_rows + 1):
        for c in range(width - block_cols + 1):
             # Check if this block overlaps with the excluded area
            if not (r >= exclude_coords[0] and r < exclude_coords[1] and \
                    c >= exclude_coords[2] and c < exclude_coords[3]):
                subgrid = grid[r:r+block_rows, c:c+block_cols]
                if condition_func(subgrid):
                    return r, c
    return -1, -1 # Should not happen

def is_pattern_block(subgrid):
    """Checks if a subgrid contains only green (3) and white (0)."""
    return np.all((subgrid == 0) | (subgrid == 3))

def is_color_key_block(subgrid):
    """Checks if a 2x2 subgrid contains only non-white (0) and non-azure (8) pixels."""
    if subgrid.shape != (2, 2):
        return False
    return np.all((subgrid != 0) & (subgrid != 8))

def transform(input_grid):
    """
    Transforms the input grid based on the pattern and color key separated by an azure line.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Identify the Divider
    divider_row = find_azure_divider(grid)
    if divider_row == -1:
        # Handle error: No divider found (though not expected)
        return [] # Or raise an error

    # 2. Locate the Pattern Block (6x6, only 0s and 3s)
    pattern_r, pattern_c = find_block(grid, (6, 6), is_pattern_block)
    if pattern_r == -1:
         # Handle error: No pattern block found
        return []

    # Determine if pattern is above or below divider
    pattern_is_above = pattern_r < divider_row

    # 3. Locate the Color Key Block (2x2, no 0s or 8s)
    # Search on the opposite side of the divider
    search_area_start_row = divider_row + 1 if pattern_is_above else 0
    search_area_end_row = height if pattern_is_above else divider_row
    
    color_key_r, color_key_c = -1, -1
    temp_grid_slice = grid[search_area_start_row:search_area_end_row, :]
    
    # Need to adjust the row index found back to the original grid's coordinate system
    temp_r, temp_c = find_block(temp_grid_slice, (2, 2), is_color_key_block)
    
    if temp_r != -1:
        color_key_r = temp_r + search_area_start_row
        color_key_c = temp_c
    else:
         # Handle error: No color key block found
        return []


    # 4. Extract Color Pairs
    colorA1 = grid[color_key_r, color_key_c]
    colorB1 = grid[color_key_r, color_key_c + 1]
    colorA2 = grid[color_key_r + 1, color_key_c]
    colorB2 = grid[color_key_r + 1, color_key_c + 1]

    # 5. Extract the Pattern
    pattern_block = grid[pattern_r:pattern_r+6, pattern_c:pattern_c+6]

    # 6. Create Output Grid
    output_grid = np.zeros((6, 6), dtype=int) # Initialize with white (0)

    # 7. Apply Coloring Rule
    for r in range(6):
        for c in range(6):
            if pattern_block[r, c] == 3: # If it's a green pixel in the pattern
                if r < 3: # Top half
                    if c < 3: # Left half
                        output_grid[r, c] = colorA1
                    else: # Right half
                        output_grid[r, c] = colorB1
                else: # Bottom half
                    if c < 3: # Left half
                        output_grid[r, c] = colorA2
                    else: # Right half
                        output_grid[r, c] = colorB2
            # Else: it remains white (0) as initialized

    # Convert back to list of lists for the required output format
    return output_grid.tolist()