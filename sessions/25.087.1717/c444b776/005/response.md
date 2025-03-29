```python
import numpy as np

"""
Identifies a single horizontal (hr) or vertical (vc) line composed entirely of yellow (4) pixels. 
These lines act as boundaries for copying or reflection based on the location of non-background (0), non-yellow (4) 'pattern' pixels.
Precedence is given to the vertical line condition.

1. Vertical Line Condition:
   - If a vertical yellow line `vc` exists AND all pattern pixels are to its left (column < vc):
     Reflect the portion of the grid left of `vc` horizontally across `vc`.
     The reflection maps a pixel at `(r, c)` to `(r, vc + (vc - c))`.
     Copy `input_grid[r, c]` to `output_grid[r, vc + (vc - c)]` for `0 <= c < vc`.

2. Horizontal Line Condition:
   - Else if a horizontal yellow line `hr` exists AND all pattern pixels are above it (row < hr):
     Perform a direct vertical copy (no flip). Copy the region above `hr` (rows 0 to `hr-1`) 
     to the region below `hr` starting at row `hr+1`.
     The copy maps a pixel at `(r, c)` to `(hr + 1 + r, c)`.
     Copy `input_grid[r, c]` to `output_grid[hr + 1 + r, c]` for `0 <= r < hr`.

3. No Applicable Condition:
   - If neither condition is met, the grid remains unchanged.

The yellow lines themselves and the original source pattern(s) are preserved.
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
    return pattern_pixels # Returns array of [row, col] pairs

def transform(input_grid):
    """
    Applies reflection or direct copy based on yellow lines and pattern location.
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
                for c in range(vc): # Iterate through columns left of the line
                    reflected_c = vc + (vc - c)
                    # Ensure reflected column is within bounds
                    if 0 <= reflected_c < width:
                        # Copy the pixel value from the original grid to the reflected position
                        output_grid[r, reflected_c] = grid_np[r, c]
            # Transformation done, return result
            return output_grid.tolist()

    # Condition 2: Horizontal line exists and pattern is entirely above (and vertical condition was not met)
    pattern_is_above = False
    # Only check this if the vertical reflection didn't happen
    if hr is not None: 
         # Check if all pattern pixels have row < hr
         if np.all(pattern_pixels[:, 0] < hr):
             pattern_is_above = True
             # Perform direct vertical copy for the region above hr
             for r in range(hr): # Iterate through rows above the line (0 to hr-1)
                 source_r = r
                 dest_r = hr + 1 + r # Destination row starts at hr+1
                 # Ensure destination row is within bounds
                 if 0 <= dest_r < height:
                     # Copy the entire source row to the destination row
                     output_grid[dest_r, :] = grid_np[source_r, :]
             # Transformation done, return result
             return output_grid.tolist()

    # Condition 3: Neither condition met, return the initial copy
    return output_grid.tolist()
```