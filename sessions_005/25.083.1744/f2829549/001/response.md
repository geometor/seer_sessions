```python
"""
1.  **Identify Orange (7):** Locate all pixels with the value '7' (orange) in the input grid.
2.  **Ignore Column 3:** Ignore column index 3 of the input grid.
3. **Determine output bounds:** Scan Input grid for any value 7. Mark the min/max row index as r_min, r_max. Mark the min/max col index as c_min, c_max
4.  **Create Output Grid:** Create an output grid of (r_max - r_min + 1) x (c_max - c_min+ 1) initialized to all zeros.
5. **Replace 7 with 3:** Scan the input grid, for pixels in input[r, c]:
    *   if r is between r_min and r_max and c is between c_min and c_max:
        *   if the pixel value is '7' output[r-r_min, c-c_min]=3
        *   otherwise output[r - r_min, c - c_min] = 0
"""

import numpy as np

def transform(input_grid):
    # Find all pixels with value '7' (orange)
    orange_pixels = np.where(input_grid == 7)

    # Determine output bounds based on orange pixel locations
    if len(orange_pixels[0]) > 0:  # Check if any orange pixels exist
        r_min = np.min(orange_pixels[0])
        r_max = np.max(orange_pixels[0])
        c_min = np.min(orange_pixels[1])
        c_max = np.max(orange_pixels[1])
    else: # if there are no orange pixels, return an empty grid.
        return np.zeros((0, 0), dtype=int)
    
    #remove column 3 effect if it exist in c_min, c_max
    if c_min < 3 and c_max >3:
      if (3-c_min)>(c_max -3):
        c_max = 2
      else:
        c_min = 4

    # Create output grid initialized to all zeros
    output_grid = np.zeros((r_max - r_min + 1, c_max - c_min + 1), dtype=int)

    # Replace '7' with '3' within the bounding box
    for r in range(r_min, r_max + 1):
        for c in range(c_min, c_max + 1):
            if input_grid[r, c] == 7:
                output_grid[r - r_min, c - c_min] = 3

    return output_grid
```