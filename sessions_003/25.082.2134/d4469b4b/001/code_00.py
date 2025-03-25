"""
1.  **Identify the "Cross":** Examine the input grid to locate the largest connected "cross" shape. A "cross" is defined as a set of contiguous non-zero pixels where all pixels touch each other at minimum diagonally, forming the visual shape of cross.
2.  **Determine Cross Color:** Note the color (numerical value) of the pixels forming the identified cross.
3. **Create cross center:** cross center is constructed on input, get the row and col indices for non-zero values, average them, respectively.
4.  **Project cross center onto output:** using the averaged cross center location, project the location onto output and make it color gray.
5. **Construct Output Grid:** Create a 3x3 output grid. All cells will have a default color of 0. Fill the center row and center column with gray (value 5). the center row number is determine using cross center row / input height * 3. The center column number is cross center col / input width * 3.
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


def transform(input_grid):
    """Transforms the input grid according to the cross rule."""

    # Find the cross in the input grid
    cross_pixels, cross_color = find_cross(input_grid)

    # if no cross, return empty output grid
    if not cross_pixels:
        return np.zeros((3, 3), dtype=int)

    # Calculate the center of the cross
    cross_row_indices = [r for r, _ in cross_pixels]
    cross_col_indices = [c for _, c in cross_pixels]
    center_row = int(np.mean(cross_row_indices))
    center_col = int(np.mean(cross_col_indices))


    # Create the 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # project cross center location onto output grid
    output_center_row = int(center_row / len(input_grid) * 3)
    output_center_col = int(center_col / len(input_grid[0]) * 3)

    # Fill the center row and column with gray (5)
    for i in range(3):
        output_grid[output_center_row, i] = 5
        output_grid[i, output_center_col] = 5

    return output_grid