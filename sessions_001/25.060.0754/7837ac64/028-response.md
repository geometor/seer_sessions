# 7837ac64 • 028 • refine_coder

---
```python
"""
1.  **Identify the Azure Structure:** Find all pixels with color 8 (azure). These pixels form a grid-like structure (which can be complete or incomplete rows/columns) that divides the input grid into regions.
2.  **Locate Key Pixels:** Within each region defined by the azure structure, identify the presence and relative positions of blue (1) and red (2) pixels.
3.  **Create 3x3 Output:** Construct a 3x3 output grid.
4.  **Map to Output:**
    *   Iterate through the regions defined by the azure structure in a consistent order (e.g., top-left to bottom-right, treating intersecting azure lines/rows as defining the boundaries).
    *   For each region:
        *   If a region contains a blue (1) pixel, place a '1' in the corresponding cell of the 3x3 output grid.
        *   If a region contains a red (2) pixel, place a '2' in the corresponding cell of the 3x3 output grid.
        *   If a region has no blue or red, the output is a '0'.
    * If the azure structure does not fully define all 9 regions (e.g. only 1 horizontal line), then assume all the space on a particular side forms a region.
5. Fill remaining cells with '0'.
"""

import numpy as np

def find_azure_structure(grid):
    # Find row and column indices where azure (8) pixels exist.
    rows = np.where(np.any(grid == 8, axis=1))[0]
    cols = np.where(np.any(grid == 8, axis=0))[0]
    return rows, cols

def get_region_contents(grid, row_start, row_end, col_start, col_end):
    # Extract the contents of a region defined by the given boundaries.
    region = grid[row_start:row_end, col_start:col_end]
    return region

def transform(input_grid):
    # Create 3x3 Output
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify the Azure Structure
    azure_rows, azure_cols = find_azure_structure(input_grid)

    # Define region boundaries based on azure structure.
    row_bounds = [0] + list(azure_rows) + [input_grid.shape[0]]
    col_bounds = [0] + list(azure_cols) + [input_grid.shape[1]]

    # Map to Output
    output_row = 0
    output_col = 0
    for i in range(len(row_bounds) - 1):
        for j in range(len(col_bounds) - 1):
            # Extract each region
            region = get_region_contents(input_grid, row_bounds[i], row_bounds[i+1], col_bounds[j], col_bounds[j+1])

            # Check region contents and map to output.
            if np.any(region == 1):
                output_grid[output_row, output_col] = 1
            elif np.any(region == 2):
                output_grid[output_row, output_col] = 2

            output_col += 1
            if output_col == 3:
                output_col = 0
                output_row += 1
            if output_row == 3:
                break  # Stop if we've filled the 3x3 grid
        if output_row == 3:
            break

    return output_grid
```
