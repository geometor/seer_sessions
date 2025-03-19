# 780d0b14 • 020 • refine_coder

---
```python
"""
1.  **Identify Regions:** The input grid is composed of rectangular regions. Each region is a contiguous block of pixels of the same color. The boundaries of these regions are defined by changes in color along rows or columns.
2. **Determine Output Dimensions:**
    - Count the number of regions stacked *vertically*. Regions are stacked if there is a change in color when moving downwards through grid rows.
    - If all regions span the full width of the input, the output will be a single column (Nx1).
    - Count the number of regions horizontally adjacent. If there is 1 horizontal region, then the column number will be 1.
    - If there are *any* horizontally adjacent regions at all, the output will have the same number of columns equal to the maximum number of horizontal regions found.
3.  **Populate Output:**
    *   The output grid will have N rows, where N is the number of vertically stacked regions divided by the number of columns in the input.
    *   Each cell in the output grid represents a region from the input grid. The value (color) of the output cell is the color of the corresponding input region.

    *   The regions are processed top-to-bottom and left-to-right.

    * If regions are side by side, then they will be output side-by-side.
    * If regions all span entire width of input, the number of columns will be 1.
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
