# 469497ad • 020 • refine_coder

---
```python
"""
1.  **Initialize:** Create an output grid filled with white (0).
2.  **Identify Central Square:** Find the largest square of uniform color centered within the input grid. Note its color (which will be blue in these cases) and size.
3. **Determine Corner Regions:** Identify colored regions (pixels that are not white and not the central square's color) in the four quadrants (top-left, top_right, bottom-left, bottom-right) relative to the *input grid's* central square. Note their colors and positions relative to the central square.
4.  **Calculate Output Size:** The output grid size should be large enough to accommodate the expanded central square and the corner regions. The central square expands by 2. Calculate the output size such that the positions of all corner regions, after being positioned relative to the *center of the output*, are within the output grid bounds. A minimum output grid size should be the expanded central_square size + 2.
5.  **Expand Central Square:** Expand the central square by 2 in the output grid, centered.
6.  **Place Corner Regions:** Position the corner regions in the output grid. Maintain their original relative positions (quadrant and offset) to the *center of the output grid*, mirroring the input grid's layout relative to *its* central square.
7.  **Create Gray Frame:** Iterate through the output grid. If a cell is white (0) and is adjacent (horizontally, vertically, or diagonally) to any cell that is not white and not gray, set it to gray (5).
8. **Return:** The transformed output grid.
"""

import numpy as np

def get_central_square(grid):
    """Finds the largest central square of the same color."""
    rows, cols = grid.shape
    center_row, center_col = rows // 2, cols // 2
    center_color = grid[center_row, center_col]
    size = 0

    for i in range(min(center_row, center_col) + 1):
        is_square = True
        for r in range(center_row - i, center_row + i + 1):
            for c in range(center_col - i, center_col + i + 1):
                if not (0 <= r < rows and 0 <= c < cols and grid[r,c] == center_color):
                    is_square = False
                    break
            if not is_square:
                break
        if is_square:
            size = 2 * i + 1
        else:
            break

    start_row, start_col = center_row - (size - 1) // 2, center_col - (size - 1) // 2

    return start_row, start_col, size, center_color

def get_corner_regions(input_grid, start_row, start_col, size):
    """Identifies colored regions in the corners relative to the central square."""
    corner_regions = {
        "top_left": [],
        "top_right": [],
        "bottom_left": [],
        "bottom_right": []
    }
    rows, cols = input_grid.shape
    center_color = input_grid[start_row, start_col]

    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != 0 and color != center_color:
                if r < start_row and c < start_col:  # Top Left
                    corner_regions["top_left"].append((r, c, color))
                elif r < start_row and c >= start_col + size:  # Top Right
                    corner_regions["top_right"].append((r, c, color))
                elif r >= start_row + size and c < start_col:  # Bottom Left
                    corner_regions["bottom_left"].append((r, c, color))
                elif r >= start_row + size and c >= start_col + size:  # Bottom Right
                    corner_regions["bottom_right"].append((r, c, color))
    return corner_regions

def calculate_output_size(input_grid, central_square_size, corner_regions):
    """Calculates the output size based on the expanded central square and corner regions."""
    start_row, start_col, size, _ = get_central_square(input_grid)
    expanded_size = central_square_size + 2

    max_offset_row = 0
    max_offset_col = 0

    # Calculate offsets of the corner regions relative to the central square.
    for region, pixels in corner_regions.items():
        for r, c, _ in pixels:
            if region == "top_left":
                row_offset = start_row - r
                col_offset = start_col - c
            elif region == "top_right":
                row_offset = start_row-r
                col_offset = c - (start_col + size -1)
            elif region == "bottom_left":
                row_offset = r - (start_row + size - 1)
                col_offset = start_col -c
            elif region == "bottom_right":
                row_offset = r - (start_row + size - 1)
                col_offset = c - (start_col + size - 1)
            max_offset_row = max(max_offset_row, row_offset)
            max_offset_col = max(max_offset_col, col_offset)


    output_size = max(expanded_size + 2 * max_offset_row, expanded_size + 2* max_offset_col)

    return output_size

def is_adjacent_to_non_white_non_gray(grid, r, c):
    """Checks if a cell is adjacent to a non-white, non-gray cell."""
    rows, cols = grid.shape
    for i in range(max(0, r - 1), min(rows, r + 2)):
        for j in range(max(0, c - 1), min(cols, c + 2)):
            if (i != r or j != c) and grid[i, j] != 0 and grid[i, j] != 5:
                return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # 1. Initialize output grid with white.
    start_row, start_col, size, center_color = get_central_square(input_grid)
    corner_regions = get_corner_regions(input_grid, start_row, start_col, size)
    output_size = calculate_output_size(input_grid, size, corner_regions)
    output_grid = np.zeros((output_size, output_size), dtype=int)


    # 2. Expand Central Square
    expanded_size = size + 2
    output_center = output_size // 2
    expanded_start_row = output_center - expanded_size // 2
    expanded_start_col = output_center - expanded_size // 2

    for r in range(expanded_size):
        for c in range(expanded_size):
            output_grid[expanded_start_row + r, expanded_start_col + c] = center_color

    # 3. Position Colored Regions
    input_center_row, input_center_col = input_grid.shape[0] // 2, input_grid.shape[1] // 2

    for region, pixels in corner_regions.items():
        for r, c, color in pixels:
            # Calculate the offset relative to the input center
            row_offset = r - input_center_row
            col_offset = c - input_center_col

            # Place the pixel in output grid, maintaining the offset relative to the output center
            output_row = output_center + row_offset
            output_col = output_center + col_offset
            output_grid[output_row, output_col] = color


    # 4. Create Gray Frame
    for r in range(output_size):
        for c in range(output_size):
            if output_grid[r, c] == 0 and is_adjacent_to_non_white_non_gray(output_grid, r, c):
                output_grid[r, c] = 5

    return output_grid
```
