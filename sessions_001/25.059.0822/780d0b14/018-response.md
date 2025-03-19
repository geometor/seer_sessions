# 780d0b14 • 018 • refine_coder

---
```python
"""
The input grid is divided into vertically stacked, distinct rectangular regions of uniform color.
The output grid is a Nx1 or Nx2 grid where each row represents one of these regions. If there are 2
regions side by side, the output has 2 columns. If there is only one region
in a row, the output is that color.
"""

import numpy as np

def get_regions(grid):
    # Find the boundaries of the colored regions.
    rows, cols = grid.shape
    h_lines = []
    v_lines = []

    # Find horizontal lines
    for r in range(1, rows):
        if np.all(grid[r] != grid[r-1]):
            h_lines.append(r)

    # Find vertical lines
    for c in range(1, cols):
        if np.all(grid[:, c] != grid[:, c-1]):
            v_lines.append(c)
    
    regions = []
    r_start = 0
    for r_end in h_lines:
        c_start = 0
        for c_end in v_lines:
            region_color = grid[r_start, c_start]
            regions.append(((r_start, c_start, r_end, c_end), region_color))
            c_start = c_end
        # account for single last region
        if c_start < cols:
          region_color = grid[r_start, c_start]
          regions.append(((r_start, c_start, r_end, cols), region_color))

        r_start = r_end

    #account for the last region
    if r_start < rows:
        c_start = 0
        for c_end in v_lines:
            region_color = grid[r_start, c_start]
            regions.append(((r_start, c_start, rows, c_end), region_color))
            c_start = c_end
        if c_start < cols:
            region_color = grid[r_start,c_start]
            regions.append(((r_start, c_start, rows, cols), region_color))

    return regions
            

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Get the distinct regions and their colors
    regions = get_regions(grid)
    
    # Determine output grid size
    num_rows = 0
    max_cols = 0
    rows = set()

    for region in regions:
        rows.add(region[0][0])
    num_rows = len(rows)

    for row in rows:
        cols_in_row = 0
        for region in regions:
            if region[0][0] == row:
                cols_in_row += 1
        max_cols = max(max_cols, cols_in_row)

    
    # Create the output grid
    output_grid = np.zeros((num_rows, max_cols), dtype=int)

    # sort regions by top row
    regions.sort(key=lambda x: (x[0][0], x[0][1]))

    # iterate regions
    row_index = 0
    col_index = 0
    current_row = 0
    for region in regions:
        if region[0][0] != current_row:
            row_index += 1
            col_index = 0
            current_row = region[0][0]
        output_grid[row_index, col_index] = region[1]
        col_index += 1


    return output_grid.tolist()
```
