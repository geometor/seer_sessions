"""
1.  **Identify the Cross:** Examine the input grid to find the largest contiguous "cross" shape. A cross is defined as a set of connected pixels of the same non-zero color, forming a '+' shape.  Pixels can be connected in all eight directions (horizontally, vertically, and diagonally). If no cross of at least size 5 is detected, output grid is all zeros.

2.  **Calculate Input Cross Center:** If a cross is found, determine its center by averaging the row and column indices of all pixels comprising the cross.

3.  **Map Input Center to Output Center:**  Map the input cross center to the output grid center. The output grid is always 3x3. The input cross center coordinates, relative to input grid size, should be scaled down to the 3x3 output. This is performed by multiplying input center row by 3 and dividing by input rows, rounding down to nearest integer. The column is calculated by multiplying input column by 3 and dividing by input columns, rounding down.

4.  **Create Output Grid:** Initialize a 3x3 output grid filled with zeros (representing black).

5.  **Draw Output Cross:**  Place a gray cross (value 5) centered at the mapped output center coordinates. The gray cross occupies the entire row and column of the calculated output center.  For instance, if the output center is (1,1), the entire second row and second column of the output grid will be filled with 5.

6.  **Handle No Cross:** If no cross is found in the input grid, return the 3x3 grid filled with zeros.
"""

import numpy as np

def find_cross(grid):
    """Finds the largest cross shape in the grid."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_cross_size = 0
    cross_pixels = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return 0

        visited.add((r, c))
        count = 1
        # Explore neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                count += dfs(r + dr, c + dc, color)
        return count

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                size = dfs(r, c, color)
                if size > max_cross_size and size >= 5:  # Cross must be at least size 5
                    max_cross_size = size
                    cross_pixels = list(visited)  # Store the visited pixels
                    visited = set()  # Reset visited for the next cross

    return cross_pixels

def get_cross_center(input_grid):
    """Calculates the center of the cross."""
    cross_pixels = find_cross(input_grid)
    if not cross_pixels:
        return None, None
    cross_row_indices = [r for r, _ in cross_pixels]
    cross_col_indices = [c for _, c in cross_pixels]
    center_row = int(np.mean(cross_row_indices))
    center_col = int(np.mean(cross_col_indices))
    return center_row, center_col

def get_output_center(input_grid):
    """Calculates the output center using correct mapping."""
    center_row, center_col = get_cross_center(input_grid)
    if center_row is None or center_col is None:
        return None, None

    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Correctly map input center to 3x3 output grid
    output_row = int(center_row * 3 / input_rows)
    output_col = int(center_col * 3 / input_cols)

    return output_row, output_col

def transform(input_grid):
    """Transforms the input grid according to the cross rule."""

    # Find the cross in the input grid and get the correctly mapped output center
    output_center_row, output_center_col = get_output_center(input_grid)

    # If no cross, return an empty 3x3 grid
    if output_center_row is None or output_center_col is None:
        return np.zeros((3, 3), dtype=int)

    # Create the 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the center row and column with gray (5) based on the output center
    for i in range(3):
        output_grid[output_center_row, i] = 5
        output_grid[i, output_center_col] = 5

    return output_grid