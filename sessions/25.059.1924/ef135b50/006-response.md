# ef135b50 • 006 • refine_coder

---
```python
"""
1.  **Identify Red Objects:** Locate all red (2) pixels within the input grid.
2.  **Horizontal Gap Filling:** For each row, if there are two or more distinct red objects, fill the space between them with maroon (9) pixels. This includes spaces that span multiple adjacent rows, as long as the gap area is horizontally contiguous.
3.  **Single Object Rule:** If a row contains only one red object, no changes are made to that row.
4. Iterate Row wise: The filling applies row-wise.
"""

import numpy as np

def find_red_regions_per_row(grid):
    """
    Identifies contiguous red regions within each row.
    Returns a list of lists, where each inner list contains
    the (row, start_col, end_col) of a red region in that row.
    """
    red_regions_by_row = []
    for row_index, row in enumerate(grid):
        regions_in_row = []
        in_region = False
        start_col = None
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                if not in_region:
                    in_region = True
                    start_col = col_index
            elif in_region:
                in_region = False
                regions_in_row.append((row_index, start_col, col_index - 1))
                start_col = None
        if in_region:  # Handle region at the end of the row
            regions_in_row.append((row_index, start_col, len(row) - 1))
        red_regions_by_row.append(regions_in_row)
    return red_regions_by_row

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all red regions in each row.
    red_regions_by_row = find_red_regions_per_row(output_grid)
    
    # Fill gaps between red regions with maroon (9)
    for row_index, regions in enumerate(red_regions_by_row):
      if len(regions) > 1:
        for i in range(len(regions) -1):
          start_fill = regions[i][2] + 1
          end_fill = regions[i+1][1] -1
          for col in range(start_fill, end_fill + 1):
            output_grid[row_index, col] = 9
            # Fill in the row below as well, if within bounds
            if row_index + 1 < rows:
              output_grid[row_index + 1, col] = 9

    return output_grid
```
