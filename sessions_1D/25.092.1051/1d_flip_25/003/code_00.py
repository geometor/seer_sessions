"""
Transformation Rule:
Swap the position of a unique singleton pixel with the last pixel (in reading order) 
of an adjacent block within a 2D grid. The input is expected as a 2D structure 
(e.g., numpy array), and the output should be a flattened 1D list.

1. Receive the input grid as a 2D structure.
2. Determine the dimensions (height, width) of the input grid.
3. Identify the "singleton" pixel: Find the pixel whose color value (ignoring the 
   background color 0) appears only once in the entire grid. Record its color 
   and location (row, column).
4. Identify the "block color": Examine the neighbors (including diagonals, 8-connectivity) 
   of the singleton pixel. Find the color of the first neighbor encountered that is 
   neither the background color (0) nor the singleton's color. This is the color 
   of the adjacent block.
5. Determine the "last block pixel" location: Scan the grid row by row, from top 
   to bottom, and within each row, column by column, from left to right. Record 
   the location (row, column) of the *last* pixel found that matches the identified 
   block color.
6. Perform the swap: Create a copy of the input grid to serve as the output grid. 
   In the output grid, set the color of the pixel at the singleton's original location 
   to the block color. Set the color of the pixel at the last block pixel's location 
   to the singleton's color.
7. Flatten the modified 2D output grid into a 1D list for the final output.
"""

import numpy as np

def _find_singleton(grid):
    """Finds the color and location of the pixel appearing exactly once (excluding background 0)."""
    # Flatten grid excluding background 0 to count non-background colors
    non_background_pixels = grid[grid != 0]
    if non_background_pixels.size == 0:
        raise ValueError("Grid contains only background color 0.")
        
    colors, counts = np.unique(non_background_pixels, return_counts=True)
    
    # Find colors that appear exactly once
    singleton_color_candidates = colors[counts == 1]
    
    if len(singleton_color_candidates) == 0:
        raise ValueError("Could not find any unique non-background color (singleton).")
    if len(singleton_color_candidates) > 1:
         # This could happen if there are multiple distinct single pixels. 
         # The prompt examples only show one. Assume the first found is the target.
         # Or, raise an error if the definition implies strictly one possible singleton.
         # Let's stick to the assumption based on examples: there's exactly one.
         raise ValueError("Found multiple unique non-background colors. Ambiguous singleton.")
         
    singleton_color = singleton_color_candidates[0]
    
    # Find the location of this unique color
    locations = np.argwhere(grid == singleton_color)
    
    # Should be exactly one location based on the count check
    if len(locations) != 1:
         # This is an internal consistency check, should not happen if count logic is right.
        raise ValueError(f"Internal error: Found {len(locations)} locations for singleton color {singleton_color}.")
        
    singleton_loc = tuple(locations[0]) # (row, col)
    return singleton_color, singleton_loc

def _find_adjacent_block_color(grid, singleton_loc):
    """Finds the color of the block adjacent (8-connectivity) to the singleton."""
    rows, cols = grid.shape
    sr, sc = singleton_loc
    singleton_color = grid[sr, sc]
    
    # Check 8 neighbors
    for r_offset in [-1, 0, 1]:
        for c_offset in [-1, 0, 1]:
            # Skip the singleton's own location
            if r_offset == 0 and c_offset == 0:
                continue 
            
            nr, nc = sr + r_offset, sc + c_offset
            
            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_color = grid[nr, nc]
                # Check if the neighbor is not background and not the singleton itself
                if neighbor_color != 0 and neighbor_color != singleton_color:
                    # Found the color of the adjacent block
                    return neighbor_color 
                    
    # If no adjacent block color found after checking all neighbors
    raise ValueError("Could not find an adjacent block color (non-background, non-singleton) for the singleton.")


def _find_last_block_pixel_loc(grid, block_color):
    """Finds the location (row, col) of the last pixel with the block color in reading order."""
    rows, cols = grid.shape
    last_loc = None
    # Iterate row by row, then column by column
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == block_color:
                # Update last_loc every time we find the block color
                last_loc = (r, c) 
    
    # If we never found the block color
    if last_loc is None:
         raise ValueError(f"Could not find any pixels with the block color {block_color}.")
         
    return last_loc

def transform(input_grid):
    """
    Transforms the input grid by swapping a unique singleton pixel with the 
    last pixel (reading order) of an adjacent block.
    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.
    Returns:
        list: A flattened 1D list representing the transformed grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    if input_grid.ndim != 2:
         raise ValueError(f"Input grid must be 2-dimensional, but got {input_grid.ndim} dimensions.")

    # Create the output grid as a copy to modify
    output_grid = np.copy(input_grid)

    # --- Identify Key Elements ---
    # Step 3: Find the singleton pixel's color and location
    singleton_color, singleton_loc = _find_singleton(input_grid)
    
    # Step 4: Find the color of the adjacent block
    block_color = _find_adjacent_block_color(input_grid, singleton_loc)
    
    # Step 5: Find the location of the last pixel belonging to the block (in reading order)
    last_block_loc = _find_last_block_pixel_loc(input_grid, block_color)

    # --- Perform the Transformation ---
    # Step 6: Swap the colors at the singleton location and the last block pixel location
    # Set the original singleton location to the block's color
    output_grid[singleton_loc] = block_color 
    # Set the last block pixel's location to the singleton's color
    output_grid[last_block_loc] = singleton_color

    # --- Output Formatting ---
    # Step 7: Flatten the grid back to a 1D list
    output_grid_flat = output_grid.flatten().tolist()
    
    return output_grid_flat