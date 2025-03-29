import numpy as np

"""
Identifies horizontal (hr) and/or vertical (vc) lines composed entirely of yellow (4) pixels.
These lines act as potential axes of symmetry or boundaries for copying.
The transformation depends on the position of non-background (0), non-yellow (4) 'pattern' pixels relative to these lines.
Precedence is given to the vertical line condition.

1. If a vertical line `vc` exists AND all pattern pixels are to its left (column < vc):
   Reflect the portion of the grid left of `vc` horizontally across `vc`.
   The reflection formula for a pixel at (r, c) is (r, vc + (vc - c)).

2. Else if a horizontal line `hr` exists AND all pattern pixels are above it (row < hr):
   Perform a vertical flip-copy. The entire region above `hr` (rows 0 to hr-1) is copied,
   flipped vertically, and placed below `hr` (starting at row hr+1).
   The copy formula for a pixel at (hr - i, c) is (hr + i, c), for 1 <= i <= hr.

3. If neither of the above conditions is met, the grid remains unchanged.

The yellow lines themselves and the original source pattern(s) are preserved in the output.
"""

def find_horizontal_line(grid):
    """Finds the row index of a horizontal line of yellow pixels."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == 4):
            return r
    return None

def find_vertical_line(grid):
    """Finds the column index of a vertical line of yellow pixels."""
    height, width = grid.shape
    for c in range(width):
        if np.all(grid[:, c] == 4):
            return c
    return None

def find_pattern_pixels(grid):
    """Finds coordinates of all non-background (0) and non-yellow (4) pixels."""
    pattern_pixels = np.argwhere((grid != 0) & (grid != 4))
    return pattern_pixels # Returns list of [row, col] pairs

def transform(input_grid):
    """
    Applies reflection or flip-copy based on yellow lines and pattern location.
    """
    # Convert input list of lists to a NumPy array
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    
    # Initialize output grid as a copy of the input
    output_grid = np.copy(grid_np)

    # Find potential yellow lines
    hr = find_horizontal_line(grid_np)
    vc = find_vertical_line(grid_np)

    # Find pattern pixels (non-background, non-yellow)
    pattern_pixels = find_pattern_pixels(grid_np)

    # If there are no pattern pixels, no transformation is needed
    if len(pattern_pixels) == 0:
        return output_grid.tolist()

    # --- Apply transformation logic based on conditions ---

    # Condition 1: Vertical line exists and pattern is entirely to the left
    pattern_is_left = False
    if vc is not None:
        # Check if all pattern pixels have column < vc
        if np.all(pattern_pixels[:, 1] < vc):
            pattern_is_left = True
            # Perform horizontal reflection for the region left of vc
            for r in range(height):
                for c in range(vc):
                    reflected_c = vc + (vc - c)
                    # Ensure reflected column is within bounds
                    if 0 <= reflected_c < width:
                        # Copy the pixel from the original grid to the reflected position
                        # We copy *all* pixels in the source region, not just pattern pixels,
                        # to correctly handle background and parts of the yellow line if they were there.
                        output_grid[r, reflected_c] = grid_np[r, c]
            # Transformation done, return result
            return output_grid.tolist()

    # Condition 2: Horizontal line exists and pattern is entirely above (and vertical condition was not met)
    pattern_is_above = False
    if hr is not None and not pattern_is_left: # Only check if vertical reflection didn't happen
         # Check if all pattern pixels have row < hr
         if np.all(pattern_pixels[:, 0] < hr):
             pattern_is_above = True
             # Perform vertical flip-copy for the region above hr
             for i in range(1, hr + 1): # i ranges from 1 to hr
                 source_r = hr - i
                 dest_r = hr + i
                 # Ensure source row is valid (implicitly true if i >= 1)
                 # Ensure destination row is within bounds
                 if 0 <= source_r < height and 0 <= dest_r < height:
                     # Copy the entire source row to the destination row
                     output_grid[dest_r, :] = grid_np[source_r, :]
             # Transformation done, return result
             return output_grid.tolist()

    # Condition 3: Neither condition met, return the initial copy
    return output_grid.tolist()