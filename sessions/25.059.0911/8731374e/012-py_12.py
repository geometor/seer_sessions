"""
1.  **Identify the Subgrid:** Find the smallest rectangular region within the input grid that contains all non-zero pixels. This region is bounded by rows and columns containing only zero-valued pixels (white).
2. **Apply color transformation within the subgrid:**
    *   If input pixel within the subgrid is yellow(4), keep its value.
    *   If input pixel within the subgrid is blue(1), keep its value.
    *  If input pixel is not blue or yellow, change them to blue.
3.  **Apply Column-Based Patterning (within the subgrid):**
    *   **Odd Columns:** Starting from the top, apply the repeating pattern "4, 4, 1" down the column, and repeat the pattern if necessary.
    *   **Even Columns:** Set all pixels in even-numbered columns to blue (1).
"""

import numpy as np

def _find_subgrid(grid):
    """Finds the bounding box of non-zero pixels."""
    rows, cols = grid.shape
    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # 1. Identify the Subgrid
    min_row, max_row, min_col, max_col = _find_subgrid(input_grid)
    subgrid_height = max_row - min_row + 1
    subgrid_width = max_col - min_col + 1
    output_grid = np.zeros((subgrid_height, subgrid_width), dtype=int)

    # 2. Apply color transformation and 3. Column Patterning
    for r in range(subgrid_height):
        for c in range(subgrid_width):
            original_value = input_grid[min_row + r, min_col + c]

            # Apply color transformation
            if original_value == 4 or original_value == 1:
                transformed_value = original_value
            else:
                transformed_value = 1

            # Column Patterning
            if (c + 1) % 2 != 0:  # Odd column
                if (r % 3) == 0 or (r % 3) == 1:
                    output_grid[r, c] = 4 if transformed_value == 4 else transformed_value #preserve yellow
                else:
                    output_grid[r, c] = 1
            else:  # Even column
                output_grid[r, c] = 1

    return output_grid