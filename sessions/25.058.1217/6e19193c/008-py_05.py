"""
The transformation involves identifying and manipulating orange (7) and gray (5) pixels within the input grid, based on specific conditions.

1. **Orange Rectangles:**  Identify rectangular shapes of orange pixels. These rectangles have a width of 2 and a height of 1.

2. **Gray Lines:** Identify horizontal lines of gray pixels.

3. **Conditional Movement of Orange:**
    - Find the bottom-most row index (`bottom_row`) where a gray line exists.
    - If an orange 2x1 rectangle is found, move it to a new position such that:
      * The new column index matches the original column index of the left-most pixel of the orange rectangle.
      * The new row index is calculated as `bottom_row + column_index - 1`, where `column_index` is the original column index of the left pixel of the orange rectangle. The color of the moved pixel is orange.

4. **Output Grid Initialization:** The output grid starts as all black (0). The transformed orange pixels are then placed onto this black grid.

"""

import numpy as np

def find_orange_rectangles(grid):
    """Finds 2x1 orange rectangles and returns their top-left coordinates."""
    orange_rectangles = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 7 and grid[r + 1, c] == 7 and grid[r, c+1] ==7 and grid[r+1,c+1] == 7:
               orange_rectangles.append((r, c))
    return orange_rectangles

def find_gray_lines(grid):
    """Finds horizontal gray lines and returns their row indices."""
    gray_lines = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 5:
                if np.all(grid[r,:] == 5):
                    gray_lines.append(r)
    return gray_lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find orange rectangles
    orange_rectangles = find_orange_rectangles(input_grid)

    # Find the bottom-most gray line
    gray_lines = find_gray_lines(input_grid)
    bottom_row = max(gray_lines) if gray_lines else -1
    
    # change output pixels 
    if bottom_row != -1:
        for r, c in orange_rectangles:
            new_row = bottom_row + c
            if new_row < rows:
                output_grid[new_row, c:c+2] = 7

    return output_grid.tolist()