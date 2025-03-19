# 995c5fa3 • 005 • refine_coder

---
```python
"""
1.  **Identify White Regions:** Find all contiguous blocks of rows that contain *only* white pixels (value 0). These are the "White Row Regions".
2.  **Define Pixel Regions:** The areas *between* the "White Row Regions" (or the edges of the input grid if no white rows exist, or only one exists) are considered "Pixel Regions".
3.  **Create Output:** Create a 3x3 output grid.
4.  **Map Colors:**
    *   The first "Pixel Region" encountered is mapped to Red (2). Fill the *first* row of the output grid with Red.
    *   If a second "Pixel Region" is found, map it to Azure (8). Fill the *second* row of the output grid with Azure.
    *   If a third "Pixel Region" is found, map it to Green (3). Fill the *third* row of the output grid with Green.
    *   If fewer than three "Pixel regions" exist, fill only the number of output rows that correspond to the regions. The output is *always* 3x3. So, if only one pixel region, only the first row is filled (with red); the other two rows will be black (0).
5. **Complete Output** The output grid is always 3x3 and filled with the colors, even if there are not three pixel regions.
"""

import numpy as np

def get_white_regions_bounds(input_grid):
    """
    Identify the row indices of distinct white pixel regions
    """
    white_rows = np.where(np.any(input_grid == 0, axis=1))[0]
    
    bounds = []
    if len(white_rows) == 0:
        return bounds

    start = white_rows[0]
    
    for i in range(len(white_rows)-1):
      if white_rows[i+1] - white_rows[i] > 1:
          bounds.append((start, white_rows[i]))
          start = white_rows[i+1]
    bounds.append((start, white_rows[-1]))

    return bounds

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify bounds of distinct white regions
    bounds = get_white_regions_bounds(input_grid)
    num_regions = len(bounds)

    # Map sections to colors and fill output rows.
    color_map = {
        0: 2,  # First section: red
        1: 8,  # Second section: azure
        2: 3   # Third section: green
    }
    
    # change output pixels 
    for i in range(min(num_regions, 3)):
        output_grid[i,:] = color_map[i]

    return output_grid
```
