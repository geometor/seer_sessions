```python
"""
1.  **Identify the Bounding Box:** Find the smallest rectangle (bounding box) that completely encloses all non-black pixels in the input grid.
2.  **Map to Output Grid:**  Map the contents of the bounding box to a 3x3 output grid.
    *   The top row of the bounding box maps to the top row of the output grid.
    *   The bottom row of the bounding box maps to the bottom row of the output grid.
    *   The leftmost column of the bounding box maps to the leftmost column of the output grid.
    *   The rightmost column of the bounding box maps to the rightmost column of the output grid.
    *   The mapping is done proportionally, filling in the intermediate cells.
3. **Handle Colors.** Preserve colors found. Iterate through non-black pixels inside the bounding box, row by row. For any output grid position, the color placed there comes from the *first* corresponding input pixel encountered during the iteration.
4.  **Empty Input:** If the input grid contains only black pixels, return a 3x3 grid filled with black pixels (all zeros).
"""

import numpy as np

def get_bounding_box(grid):
    """Calculates the minimal bounding box for given coordinates."""
    coords = np.argwhere(grid != 0)
    if len(coords) == 0:
        return (0, 0, 0, 0)
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Get bounding box coordinates
    min_row, min_col, max_row, max_col = get_bounding_box(input_grid)
    width = max_col - min_col + 1
    height = max_row - min_row + 1

    # Handle empty input
    if width == 0 or height == 0:
        return output_grid

    # Iterate through the bounding box and map to the output grid
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            # Map input bounding box indices to output grid indices
            output_row = (i - min_row) * 3 // height
            output_col = (j - min_col) * 3 // width

            # Ensure indices are within bounds
            output_row = max(0, min(output_row, 2))
            output_col = max(0, min(output_col, 2))

            # Fill the output grid, only if the cell is currently empty (prioritize earlier pixels)
            if output_grid[output_row, output_col] == 0:
                output_grid[output_row, output_col] = input_grid[i, j]


    return output_grid
```