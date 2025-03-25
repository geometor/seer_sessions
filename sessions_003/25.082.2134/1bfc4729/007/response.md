```python
"""
1.  **Identify and Sort Seeds:** Find all non-zero pixels ("seed pixels") in the input grid. Sort these seed pixels by their row index, from top to bottom.

2.  **Iterate through Seeds:** For each seed pixel:

    *   **Calculate Midpoints:** Determine the midpoint row between the current seed pixel and the seed pixel above it (if any). Also, determine the midpoint row between the current seed pixel and the seed pixel below it (if any).

    *   **Create Top Bar:** Create a horizontal bar of the seed pixel's color.
        *   The bar starts at the top of the grid, or one row below the midpoint between this seed and the previous seed, whichever is *lower*.
        *   The bar ends at the row of the current seed pixel.
        *   The bar extends across all columns, *except* the column containing the seed pixel. At the seed pixel's column, the output grid retains the original input value for all rows.

    *   **Create Bottom Bar:** Create a horizontal bar of the seed pixel's color.
        *   The bar starts one row below the current seed pixel's row.
        *   The bar ends at the bottom of the grid, or at the midpoint between the current seed and the next seed, whichever is *higher*.
        *   The bar extends across all columns, *except* the column containing the seed pixel. At the seed pixel's column, the output grid retains the original input value for all rows.

3. **Preserve Original Columns:** For *every* row in the grid and for *each* seed pixel, ensure that the output grid, at the column of that seed pixel, retains the value from the *input* grid at that location. This step is crucial for creating "breaks" in the bars.
"""

import numpy as np

def get_non_zero_pixels(grid):
    """Finds and returns a list of non-zero pixels with their positions and colors."""
    rows, cols = grid.shape
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_zero_pixels.append((r, c, grid[r, c]))
    return non_zero_pixels

def calculate_midpoint(row1, row2):
    """Calculates the midpoint between two row indices."""
    return (row1 + row2) // 2

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid) # Start with a copy to preserve original values
    rows, cols = input_grid.shape

    # 1. Identify and Sort Seeds
    non_zero_pixels = get_non_zero_pixels(input_grid)
    non_zero_pixels.sort()  # Sorts by row index (ascending)

    # 2. Iterate through Seeds
    for i, (r, c, value) in enumerate(non_zero_pixels):
        # Calculate Midpoints
        start_row_top = 0
        if i > 0:
            start_row_top = calculate_midpoint(non_zero_pixels[i-1][0], r) + 1

        end_row_bottom = rows - 1
        if i < len(non_zero_pixels) - 1:
            end_row_bottom = calculate_midpoint(r, non_zero_pixels[i+1][0])

        # Create Top Bar
        for current_row in range(start_row_top, r + 1):
            for col in range(cols):
                if col != c:  # Preserve original value at seed column
                    output_grid[current_row, col] = value

        # Create Bottom Bar
        for current_row in range(r + 1, end_row_bottom + 1):
            for col in range(cols):
                if col != c:  # Preserve original value at seed column
                    output_grid[current_row, col] = value


    return output_grid
```
