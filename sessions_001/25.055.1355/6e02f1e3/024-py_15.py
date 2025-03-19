"""
1. **Identify Objects:** Find all contiguous vertical lines of green (3) pixels.  A contiguous line is defined as a set of green pixels where each pixel (except the topmost) is directly below another green pixel.
2. **Top Row Transformation:** For each identified object, change the color of the topmost green pixel to gray (5).
3. **Remaining Rows Transformation:** For each identified object, change the color of all green pixels *below* the topmost pixel to white (0).
4. **Preserve Other Pixels:** All other pixels in the grid that are not part of the identified green vertical lines should retain their original color.  (This is implicit in the examples, but good to state explicitly).
5. **Output Dimensions:** the output grid dimensions are identical to the input.
"""

import numpy as np

def find_vertical_lines(grid, color=3):
    """
    Finds contiguous vertical lines of a specified color in a grid.
    Returns a list of lists, where each inner list contains the (row, col)
    coordinates of pixels belonging to a single vertical line.
    """
    lines = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_line):
        visited.add((r, c))
        current_line.append((r, c))

        # Check the cell below
        next_r = r + 1
        if is_valid(next_r, c) and grid[next_r, c] == color and (next_r, c) not in visited:
            dfs(next_r, c, current_line)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_line = []
                dfs(r, c, current_line)
                lines.append(current_line)

    return lines

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all vertical lines of green (3) pixels
    vertical_lines = find_vertical_lines(output_grid, color=3)

    # Process each vertical line
    for line in vertical_lines:
        # Find the topmost pixel's coordinates
        topmost_pixel = min(line, key=lambda p: p[0])

        # Change the topmost pixel to gray (5)
        output_grid[topmost_pixel[0], topmost_pixel[1]] = 5

        # Change the remaining pixels in the line to white (0)
        for r, c in line:
            if (r, c) != topmost_pixel:
                output_grid[r, c] = 0

    return output_grid