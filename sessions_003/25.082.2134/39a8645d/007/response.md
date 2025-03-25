```python
"""
1.  **Scan for 3x3 Regions:** Iterate through the input grid, considering each pixel as the top-left corner of a potential 3x3 region.
2.  **Check 3x3 Validity:** For each 3x3 region, check if all nine pixels are non-zero and have the same color. If this condition is met, it's a valid 3x3 object.
3. **Prioritized Object Selection**:
      *If one or more valid 3x3 regions are found, select based on the following criteria.*
      * **Priority 1: Color 4 (Yellow):** If any of the valid 3x3 objects are yellow (color 4), select the *first* one found during the scan (top-left to bottom-right).
      * **Priority 2: First Found:** If no yellow 3x3 objects are found, select the *first* valid 3x3 object of any color encountered during the scan.
4.  **Extraction:** If a 3x3 object is selected, create a 3x3 output grid and copy the selected object into it, maintaining its original pixel arrangement.
5. **No 3x3 object:** If no valid 3x3 is found in the entire scan, return the input unchanged.
"""

import numpy as np

def check_3x3_validity(grid, row, col):
    # Check if the 3x3 region is within bounds
    if row + 3 > grid.shape[0] or col + 3 > grid.shape[1]:
        return False, 0

    # Extract the 3x3 region
    region = grid[row:row+3, col:col+3]

    # Check if all pixels are non-zero and have the same color
    first_pixel_color = region[0, 0]
    if first_pixel_color == 0:
        return False, 0
    
    if np.all(region == first_pixel_color):
        return True, first_pixel_color
    else:
        return False, 0

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Iterate through the grid, checking for 3x3 regions
    target_object = None
    target_color = 0
    target_row = 0
    target_col = 0

    for r in range(rows):
        for c in range(cols):
            is_valid, color = check_3x3_validity(grid, r, c)
            if is_valid:
                if color == 4:  # Priority 1: Yellow (color 4)
                    target_row = r
                    target_col = c
                    target_color = color
                    target_object = grid[r:r+3, c:c+3]
                    break  # Found yellow, stop searching
                elif target_object is None:  # Priority 2: First Found
                    target_row = r
                    target_col = c
                    target_color = color
                    target_object = grid[r:r+3, c:c+3]
        if target_object is not None and target_color==4:
          break

    # If no 3x3 object is found, return the original grid
    if target_object is None:
        return grid.tolist()

    # Create the output grid (3x3) and copy the object
    output_grid = np.zeros((3, 3), dtype=int)
    output_grid[:] = target_object

    return output_grid.tolist()
```