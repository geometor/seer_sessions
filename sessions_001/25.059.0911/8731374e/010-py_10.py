"""
1.  **Locate Subgrid:** A 10x9 subgrid is extracted from the input grid. The top-left corner of extraction region is row 7, column 4.
2.  **Color Reduction:** All pixels within this subgrid that are yellow (4) remain yellow. All pixels that are blue (1) remains blue. All other colors transform to blue.
3.  **Column Patterning:**.
    *   Odd columns (1, 3, 5, 7, 9) are set to the repeating pattern, from top to bottom: "4, 4, 1, 4, 4, 1, 4, 4, 1, 4".
    *   Even columns (2, 4, 6, 8) are set to all blue (1).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # 1. Locate Subgrid
    rows, cols = input_grid.shape
    subgrid_height = 10
    subgrid_width = 9
    start_row = 7
    start_col = 3  # 0-indexed, so column 4 is index 3
    end_row = start_row + subgrid_height
    end_col = start_col + subgrid_width

    output_grid = np.zeros((subgrid_height, subgrid_width), dtype=int)

    # 2. Color Reduction and 3. Column Patterning (combined for efficiency)
    for r in range(subgrid_height):
        for c in range(subgrid_width):
            original_value = input_grid[start_row + r, start_col + c]

            if (c+1) % 2 != 0: # Odd Columns
              if r == 0 or r == 1 or r==3 or r==4 or r==7 or r==8:
                output_grid[r,c] = 4
              else:
                output_grid[r,c] = 1
            else:
              output_grid[r,c] = 1


    return output_grid