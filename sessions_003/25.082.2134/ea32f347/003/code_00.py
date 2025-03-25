"""
1.  **Identify Gray Pixels:** Find all pixels that are gray (color code 5).
2.  **Check for Vertical Gray Lines:** For each gray pixel, check if it's part of a vertical line of gray pixels. A vertical line is defined as two or more contiguous gray pixels directly above or below each other.
3.  **Transform Vertical Lines:** If a gray pixel is part of a vertical gray line, change the color of *all* pixels in that vertical line to blue (color code 1).
4.  **Check for Horizontal Gray Lines:** For each gray pixel *not* already modified, check if it belongs to a horizontal gray line. A horizontal line is defined as two or more contiguous gray pixels directly to the left or right of each other.
5.  **Transform Horizontal Lines based on Length:**
    *   If the horizontal gray line has a length of 3, change the color of all pixels in the line to red (color code 2).
    *   If the horizontal gray line has a length of 4, change the color of all pixels in the line to yellow (color code 4).
    *   If the horizontal gray line has a length of 5, change the color of all pixels in the line to blue (color code 1).
    *   If the horizontal gray line has a length of 6, change the color of all pixels in the line to yellow (color code 4).
6. **Intersections**: If gray pixels that meet the criteria for both vertical and horizontal lines, the vertical line transformation is applied, *then*, if the pixels haven't changed, apply the horizontal rules.
7.  **All Other Pixels:** Leave all other pixels (non-gray, or gray pixels not part of any vertical or horizontal line as defined above) unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def get_vertical_line(r, c):
        if not is_valid(r, c) or input_grid[r, c] != 5:
            return []
        line = []
        while is_valid(r, c) and input_grid[r, c] == 5:
            line.append((r, c))
            r += 1
        return line

    def get_horizontal_line(r, c):
        if not is_valid(r, c) or input_grid[r, c] != 5:
            return []
        line = []

        # Traverse left
        c_left = c
        while is_valid(r, c_left) and input_grid[r, c_left] == 5:
            line.append((r, c_left))
            c_left -= 1

        # Traverse Right, starting one position to the right to avoid double-counting the starting cell
        c_right = c + 1
        while is_valid(r, c_right) and input_grid[r, c_right] == 5:
            line.append((r, c_right))
            c_right += 1

        return line

    # First, process all vertical lines
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5 and not visited[r, c]:
                vertical_line = get_vertical_line(r, c)
                if len(vertical_line) > 1:
                    for vr, vc in vertical_line:
                        output_grid[vr, vc] = 1  # Change to blue
                        visited[vr, vc] = True

    # Then, process horizontal lines for remaining gray pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5 and not visited[r, c]:
                horizontal_line = get_horizontal_line(r, c)
                if len(horizontal_line) >= 3:  # Horizontal lines of length 2 are not considered.
                    if len(horizontal_line) == 3:
                        color = 2  # Red
                    elif len(horizontal_line) == 4:
                        color = 4  # Yellow
                    elif len(horizontal_line) == 5:
                        color = 1  # Blue
                    elif len(horizontal_line) == 6:
                        color = 4 # Yellow
                    else:
                        color = 5 # Default - should not occur
                    for hr, hc in horizontal_line:
                        output_grid[hr, hc] = color
                        visited[hr,hc] = True #mark as visited

    return output_grid