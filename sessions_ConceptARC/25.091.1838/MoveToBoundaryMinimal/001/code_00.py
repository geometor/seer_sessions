import numpy as np
from collections import Counter

"""
Identify the background color (white, 0).
Identify all non-background pixels.
Find the pixel color that appears exactly once; this is the 'mover' pixel. Record its color and initial coordinates (row_start, col_start).
Identify the remaining non-background pixels; these form the 'barrier' line. Determine if the barrier is horizontal or vertical. Record the barrier's row or column coordinate.
Determine the target coordinates (row_end, col_end) for the 'mover' pixel:
  If the barrier is vertical at column `col_barrier`:
    The target row is `row_start`.
    The target column is `col_barrier - 1` if `col_start < col_barrier`, otherwise `col_barrier + 1`.
  If the barrier is horizontal at row `row_barrier`:
    The target column is `col_start`.
    The target row is `row_barrier - 1` if `row_start < row_barrier`, otherwise `row_barrier + 1`.
Create the output grid as a copy of the input grid.
Set the pixel at the 'mover' pixel's initial coordinates (row_start, col_start) in the output grid to the background color (white, 0).
Set the pixel at the calculated target coordinates (row_end, col_end) in the output grid to the 'mover' pixel's color.
"""

def find_colored_pixels(grid, background_color=0):
    """Finds coordinates of all non-background pixels, grouped by color."""
    color_coords = {}
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color:
                if color not in color_coords:
                    color_coords[color] = []
                color_coords[color].append((r, c))
    return color_coords

def analyze_barrier(coords):
    """Determines if a set of coordinates forms a horizontal or vertical line."""
    rows = {r for r, c in coords}
    cols = {c for r, c in coords}
    
    is_horizontal = len(rows) == 1 and len(cols) > 1
    is_vertical = len(cols) == 1 and len(rows) > 1
    
    orientation = None
    coord_val = None
    
    if is_horizontal:
        orientation = "horizontal"
        coord_val = list(rows)[0] # The common row
    elif is_vertical:
        orientation = "vertical"
        coord_val = list(cols)[0] # The common column
        
    return orientation, coord_val

def transform(input_grid):
    """
    Moves a single uniquely colored pixel towards a line barrier of another color, 
    stopping one cell away from the barrier.
    """
    output_grid = np.copy(input_grid)
    background_color = 0
    
    # 1. & 2. Identify non-background pixels and group by color
    color_coords = find_colored_pixels(input_grid, background_color)
    
    mover_color = -1
    mover_coords = None
    barrier_color = -1
    barrier_coords = None
    
    # 3. & 4. Find mover (count=1) and potential barrier (count>1)
    for color, coords in color_coords.items():
        if len(coords) == 1:
            mover_color = color
            mover_coords = coords[0]
        elif len(coords) > 1:
            # Assuming only one barrier color exists besides the mover
            barrier_color = color
            barrier_coords = coords
            
    if mover_coords is None or barrier_coords is None:
        # Handle error: Did not find a unique mover and/or a barrier candidate
        print("Error: Could not identify mover pixel or barrier line.")
        return output_grid # Return original grid or handle error appropriately

    # 4. Determine barrier orientation and coordinate
    barrier_orientation, barrier_coord_val = analyze_barrier(barrier_coords)
    
    if barrier_orientation is None:
        # Handle error: Barrier is not a simple horizontal or vertical line
        print("Error: Barrier is not a horizontal or vertical line.")
        return output_grid

    mover_row_start, mover_col_start = mover_coords
    target_row_end, target_col_end = -1, -1

    # 5. Determine target coordinates
    if barrier_orientation == "vertical":
        target_row_end = mover_row_start
        barrier_col = barrier_coord_val
        # Move right if mover is left, move left if mover is right
        target_col_end = barrier_col - 1 if mover_col_start < barrier_col else barrier_col + 1
    elif barrier_orientation == "horizontal":
        target_col_end = mover_col_start
        barrier_row = barrier_coord_val
        # Move down if mover is above, move up if mover is below
        target_row_end = barrier_row - 1 if mover_row_start < barrier_row else barrier_row + 1

    if target_row_end == -1 or target_col_end == -1:
         print("Error: Could not calculate target position.")
         return output_grid # Or handle more gracefully

    # 6. Create output grid (already copied)
    
    # 7. Set mover's original position to background
    output_grid[mover_row_start, mover_col_start] = background_color
    
    # 8. Set target position to mover's color
    # Check bounds just in case, though logic should prevent out-of-bounds
    height, width = output_grid.shape
    if 0 <= target_row_end < height and 0 <= target_col_end < width:
        output_grid[target_row_end, target_col_end] = mover_color
    else:
        print(f"Warning: Calculated target position ({target_row_end}, {target_col_end}) is out of bounds.")


    return output_grid