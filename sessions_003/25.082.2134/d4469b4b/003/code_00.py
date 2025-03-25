"""
1.  **Find the Cross:** Identify the largest contiguous "cross" shape in the input grid. A cross is a set of connected non-zero pixels of the same color, forming a '+' shape, where pixels can be connected in eight directions (including diagonals).
2.  **Locate Cross Center:** Calculate the center of the identified cross by averaging the row and column indices of all pixels belonging to the cross.
3.  **Determine Output Center:**  Map the input cross center to the output grid center using the following rule:
    *   Divide the input grid into 9 equal-sized regions (3x3).  This will be a conceptual division.
    *   Determine which of the 9 regions contains the input cross center.
    *   The output cross center will be the center of the corresponding region in the 3x3 output grid. The mapping is as follows (input_region_row, input_region_col) -> (output_row, output_col):
        * (0,0) -> (0,0)
        * (0,1) -> (0,1)
        * (0,2) -> (0,2)
        * (1,0) -> (1,0)
        * (1,1) -> (1,1)
        * (1,2) -> (1,2)
        * (2,0) -> (2,0)
        * (2,1) -> (2,1)
        * (2,2) -> (2,2)

4. **Construct the Output Grid:** Create a 3x3 output grid. Fill it with 0 (black/background) by default.
5. **Create Output Cross:** Place a gray (value 5) cross in the output grid, centered at output center determined in step 3. The gray cross fills the entire center row and center column of the 3x3 output grid.
6.  **No Cross:** If no cross is found in the input grid, return a 3x3 grid filled with 0s.
"""

import numpy as np

def find_cross(grid):
    """Finds the largest cross shape in the grid."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_cross_size = 0
    cross_color = 0
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
                if size > max_cross_size and size >=5:  #cross must be at least size 5
                    max_cross_size = size
                    cross_color = color
                    cross_pixels = list(visited) #store the visited
                    visited = set() #reset to empty

    return cross_pixels, cross_color

def get_cross_center(input_grid):
    """Calculates the center of the cross."""
    cross_pixels, _ = find_cross(input_grid)
    if not cross_pixels:
        return None, None
    cross_row_indices = [r for r, _ in cross_pixels]
    cross_col_indices = [c for _, c in cross_pixels]
    center_row = int(np.mean(cross_row_indices))
    center_col = int(np.mean(cross_col_indices))
    return center_row, center_col

def get_output_center(input_grid):
    """Calculates the output center using 3x3 region mapping."""
    center_row, center_col = get_cross_center(input_grid)
    if center_row is None or center_col is None:
        return None, None

    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Determine the input region (0, 1, or 2 for row and col)
    region_row = min(2, int(center_row / (input_rows / 3)))
    region_col = min(2, int(center_col / (input_cols / 3)))

    return region_row, region_col


def transform(input_grid):
    """Transforms the input grid according to the cross rule."""

    # Find the cross in the input grid and get output center
    output_center_row, output_center_col = get_output_center(input_grid)

    # if no cross, return empty output grid
    if output_center_row is None or output_center_col is None:
        return np.zeros((3, 3), dtype=int)

    # Create the 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the center row and column with gray (5)
    for i in range(3):
        output_grid[output_center_row, i] = 5
        output_grid[i, output_center_col] = 5

    return output_grid