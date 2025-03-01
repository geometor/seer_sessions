"""
1.  **Identify Markers:** Locate all red (2) and magenta (6) pixels within the input grid.
2.  **Check for Both Colors:** If both red and magenta pixels are present in the input grid, proceed to step 3. Otherwise, the output grid is identical to the input grid (no transformation).
3.  **Determine Bounding Box:** Define a rectangular bounding box.  The top-left corner of the box is determined by the minimum row and minimum column of *all* red and magenta pixels. The bottom-right corner is determined by the maximum row and maximum column of *all* red and magenta pixels.
4.  **Fill Bounding Box:**  Within the output grid (initially filled with zeros), set all pixels *inside* the bounding box to blue (1).
5.  **Preserve Markers:** Copy the red (2) and magenta (6) pixels from the input grid to their exact same positions in the output grid, overwriting the blue fill at those specific locations.
"""

import numpy as np

def find_cells_by_color(grid, color):
    """Finds the positions of cells with the specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Markers
    red_cells = find_cells_by_color(input_grid, 2)
    magenta_cells = find_cells_by_color(input_grid, 6)

    # 2. Check for Both Colors
    if len(red_cells) > 0 and len(magenta_cells) > 0:
        # 3. Determine Bounding Box
        min_row = min(red_cells[:, 0].min(), magenta_cells[:, 0].min())
        min_col = min(red_cells[:, 1].min(), magenta_cells[:, 1].min())
        max_row = max(red_cells[:, 0].max(), magenta_cells[:, 0].max())
        max_col = max(red_cells[:, 1].max(), magenta_cells[:, 1].max())

        # 4. Fill Bounding Box
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                output_grid[r, c] = 1

        # 5. Preserve Markers
        for r, c in red_cells:
            output_grid[r, c] = 2
        for r, c in magenta_cells:
            output_grid[r, c] = 6

        return output_grid.tolist()
    else:
        # no transformation
        return input_grid.tolist()