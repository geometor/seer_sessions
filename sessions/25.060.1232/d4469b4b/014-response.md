# d4469b4b • 014 • refine_coder

---
```python
"""
1.  **Identify the Blue Region:** Locate the contiguous block of blue pixels within the input grid.
2.  **Determine Bounding Box:** Calculate the bounding box around the blue region, noting its height (`bb_h`) and width (`bb_w`).
3.  **Determine Output Dimensions and Pixel Placement Based on Blue Region Width:**

    *   **If `bb_w` is 3:**
        *   Create an output grid of size (`bb_h` + 1) x (`bb_w` +1).
        *   Fill the grid with gray pixels.
        *   Place white pixels at the four corners: (0, 0), (0, `bb_w`), (`bb_h`, 0), (`bb_h`, `bb_w`).

    *   **If `bb_w` is 4 and the blue region is vertically centered:**
        *   Create an output grid of size (`bb_h` + 1) x (`bb_w`).
        *   Fill the grid with gray pixels.
        *   Place white pixels at the four corners: (0, 0), (0, `bb_w` - 1), (`bb_h`, 0), (`bb_h`, `bb_w` - 1).

    *   **If `bb_w` is 5:**
        *   Create an output grid of size (`bb_h` + 2) x (`bb_w` + 1).
        *   Fill the grid with gray pixels.
        *   Place white pixels at the four corners: (0, 0), (0, `bb_w`), (`bb_h` + 1, 0), (`bb_h` + 1, `bb_w`).

    *   **If `bb_w` is 4 and blue region is closer to the top edge:**
        *    Create an output grid of size (bb_h + 1, bb_w + 2)
        *    Place white pixels on the top two rows in the first two columns and last two columns
        *    Fill remaining pixels with gray

4.  **Return the Output Grid:** The resulting grid with the specified dimensions and pixel values is the output.
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Handle case where color is not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def is_vertically_centered(input_grid, bounding_box):
    """Checks if the blue region is vertically centered."""
    if bounding_box is None:
        return False

    (min_row, min_col), (max_row, max_col) = bounding_box
    bb_h = max_row - min_row + 1
    grid_h = input_grid.shape[0]

    # Calculate space above and below the blue region
    space_above = min_row
    space_below = grid_h - max_row - 1

    return abs(space_above - space_below) <= 1  # Allow for 1-pixel difference


def transform(input_grid):
    input_grid = np.array(input_grid)
    # 1. Identify the Blue Region and 2. Determine Bounding Box
    bounding_box = get_bounding_box(input_grid, 1)
    if bounding_box is None:
        return []  # Return empty if there is no blue region.

    (min_row, min_col), (max_row, max_col) = bounding_box
    bb_h = max_row - min_row + 1
    bb_w = max_col - min_col + 1

    # 3. Determine Output Dimensions
    if bb_w == 3:
        output_h, output_w = bb_h + 1, bb_w + 1
        output_grid = np.full((output_h, output_w), 5, dtype=int)
        output_grid[0, 0] = 0
        output_grid[0, output_w - 1] = 0
        output_grid[output_h - 1, 0] = 0
        output_grid[output_h - 1, output_w - 1] = 0
    elif bb_w == 4 and is_vertically_centered(input_grid, bounding_box):
        output_h, output_w = bb_h + 1, bb_w
        output_grid = np.full((output_h, output_w), 5, dtype=int)
        output_grid[0, 0] = 0
        output_grid[0, output_w - 1] = 0
        output_grid[output_h - 1, 0] = 0
        output_grid[output_h - 1, output_w - 1] = 0
    elif bb_w == 5:
        output_h, output_w = bb_h + 2, bb_w + 1
        output_grid = np.full((output_h, output_w), 5, dtype=int)
        output_grid[0, 0] = 0
        output_grid[0, output_w - 1] = 0
        output_grid[output_h - 1, 0] = 0
        output_grid[output_h - 1, output_w - 1] = 0
    elif bb_w == 4 and not is_vertically_centered(input_grid, bounding_box):
        output_h, output_w = bb_h + 1, bb_w + 2
        output_grid = np.full((output_h, output_w), 5, dtype=int)
        output_grid[0:2, 0:2] = 0  # Top-left corner
        output_grid[0:2, output_w - 2:output_w] = 0  # Top-right corner
    else:
        return []  # Should not happen, based on current examples

    return output_grid.tolist()
```
