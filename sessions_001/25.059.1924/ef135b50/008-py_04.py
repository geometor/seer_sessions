"""
1. **Identify Red Objects:** In each row, identify contiguous regions of red (2) pixels. Each of these contiguous regions is considered a single red "object."

2. **Horizontal Gap Filling (Row-wise):** For each row *independently*:
    - If a row contains two or more distinct red objects, fill the space *between* those objects with maroon (9) pixels.
    - "Between" means the pixels directly between the end of one red object and the start of the next red object in the same row.
    - Do *not* fill any pixels in rows above or below.

3. **Single Object Rows:** If a row contains only one red object, or no red objects, no changes are made to that row.
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

    # Find all red regions in each row.
    red_regions_by_row = find_red_regions_per_row(output_grid)
    
    # Fill gaps between red regions with maroon (9) - strictly horizontal
    for row_index, regions in enumerate(red_regions_by_row):
      if len(regions) > 1:
        for i in range(len(regions) -1):
          start_fill = regions[i][2] + 1
          end_fill = regions[i+1][1] -1
          for col in range(start_fill, end_fill + 1):
            output_grid[row_index, col] = 9

    return output_grid