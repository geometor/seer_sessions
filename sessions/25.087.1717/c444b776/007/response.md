```python
import numpy as np

"""
Identifies a single horizontal (hr) or vertical (vc) line composed entirely of yellow (4) pixels.
Performs a transformation (reflection or copy) based on the line type and the location of non-background (0), non-yellow (4) 'pattern' pixels relative to the line.
Vertical line reflection takes precedence over horizontal line copying.

1. Vertical Reflection (Priority):
   - If a vertical yellow line `vc` exists:
     - If ALL pattern pixels are to the left (column < vc):
       Reflect the entire region left of `vc` (all rows, columns 0 to vc-1) horizontally across `vc`.
       A pixel at `(r, c)` is reflected to `(r, vc + (vc - c))`.
     - Else if ALL pattern pixels are to the right (column > vc):
       Reflect the entire region right of `vc` (all rows, columns vc+1 to width-1) horizontally across `vc`.
       A pixel at `(r, c)` is reflected to `(r, vc - (c - vc))`.

2. Horizontal Copy (Fallback):
   - Else if a horizontal yellow line `hr` exists (and vertical reflection conditions were not met):
     - If ALL pattern pixels are above (row < hr):
       Copy the entire region above `hr` (all columns, rows 0 to hr-1) vertically to the area below `hr`, starting at row `hr+1`.
       A pixel at `(r, c)` is copied to `(hr + 1 + r, c)`.
     - Else if ALL pattern pixels are below (row > hr):
       Copy the entire region below `hr` (all columns, rows hr+1 to height-1) vertically to the area above `hr`, starting at row `hr-1` and going upwards.
       A pixel at `(r, c)` is copied to `(hr - 1 - (r - (hr + 1)), c)` which simplifies to `(2*hr - r, c)`.

3. No Applicable Transformation:
   - If no yellow line exists, or if pattern pixels exist but do not meet the positional criteria (e.g., on both sides of a line), the grid remains unchanged.

The yellow lines themselves and the original source pattern(s) are preserved in the output.
The transformation overwrites pixels in the destination area.
"""

def find_horizontal_line(grid):
    """Finds the row index of the first complete horizontal line of yellow pixels."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == 4):
            return r
    return None

def find_vertical_line(grid):
    """Finds the column index of the first complete vertical line of yellow pixels."""
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
    Applies reflection or copy based on yellow lines and pattern location.
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

    # --- Apply transformation logic (Vertical has priority) ---

    # 1. Check Vertical Reflection
    if vc is not None:
        pattern_cols = pattern_pixels[:, 1]
        # Check if all pattern pixels are to the left
        if np.all(pattern_cols < vc):
            # Reflect left region to right
            for r in range(height):
                for c in range(vc): # Iterate columns left of the line
                    reflected_c = vc + (vc - c)
                    if 0 <= reflected_c < width: # Check bounds
                        output_grid[r, reflected_c] = grid_np[r, c]
            return output_grid.tolist() # Transformation done
        # Check if all pattern pixels are to the right
        elif np.all(pattern_cols > vc):
            # Reflect right region to left
            for r in range(height):
                for c in range(vc + 1, width): # Iterate columns right of the line
                    reflected_c = vc - (c - vc)
                    if 0 <= reflected_c < width: # Check bounds
                         output_grid[r, reflected_c] = grid_np[r, c]
            return output_grid.tolist() # Transformation done

    # 2. Check Horizontal Copy (Fallback)
    if hr is not None:
        pattern_rows = pattern_pixels[:, 0]
        # Check if all pattern pixels are above
        if np.all(pattern_rows < hr):
             # Copy region above to below
            for r in range(hr): # Iterate rows above the line (0 to hr-1)
                source_r = r
                dest_r = hr + 1 + r # Destination row starts at hr+1
                if 0 <= dest_r < height: # Check bounds
                    output_grid[dest_r, :] = grid_np[source_r, :]
            return output_grid.tolist() # Transformation done
        # Check if all pattern pixels are below
        elif np.all(pattern_rows > hr):
            # Copy region below to above
            for source_r in range(hr + 1, height): # Iterate rows below the line
                # dest_r = hr - 1 - (source_r - (hr + 1)) # Calculate destination row upwards from hr-1
                dest_r = 2 * hr - source_r # Simplified calculation
                if 0 <= dest_r < height: # Check bounds
                    output_grid[dest_r, :] = grid_np[source_r, :]
            return output_grid.tolist() # Transformation done

    # 3. No Applicable Transformation
    # If none of the conditions above were met and triggered a return,
    # return the initial grid copy unchanged.
    return output_grid.tolist()
```