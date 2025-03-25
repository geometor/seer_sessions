"""
1.  **Initialization:** Create a copy of the input grid and a "visited" grid.

2.  **Identify Gray Pixels:** Iterate through the input grid.

3.  **Vertical Line Processing:** For each gray pixel:
    *   Check for a vertical line (length >= 2).
    *   If found, change the color of all pixels in the line to blue (1) and mark them as visited.

4.  **Horizontal Line Processing:** For each gray pixel that has not been visited:
    *   Check for a horizontal line.
    *   Determine the length of the horizontal line.
    *   Apply color transformations based on length:
        *   Length 3: red (2)
        *   Length 4: yellow (4)
        *   Length 5: blue (1)
        *   Length 6: yellow (4)
        *   Mark each pixel as "visited".

5.  **Output:** Return the output grid.
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
        """Gets a vertical line of gray pixels starting at (r, c)."""
        if not is_valid(r, c) or input_grid[r, c] != 5:
            return []
        line = []
        # Traverse upwards
        r_up = r
        while is_valid(r_up, c) and input_grid[r_up, c] == 5:
            line.append((r_up, c))
            r_up -= 1

        #traverse downwards, starting one step below
        r_down = r + 1
        while is_valid(r_down, c) and input_grid[r_down, c] == 5:
          line.append((r_down,c))
          r_down += 1
        return line

    def get_horizontal_line(r, c):
        """Gets a horizontal line of gray pixels starting at (r, c)."""
        if not is_valid(r, c) or input_grid[r, c] != 5:
            return []
        line = []

        # Traverse left
        c_left = c
        while is_valid(r, c_left) and input_grid[r, c_left] == 5:
            line.append((r, c_left))
            c_left -= 1

        # Traverse Right, starting one position to the right
        c_right = c + 1
        while is_valid(r, c_right) and input_grid[r, c_right] == 5:
            line.append((r, c_right))
            c_right += 1

        return line

    # Process vertical lines
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5 and not visited[r, c]:
                vertical_line = get_vertical_line(r, c)
                if len(vertical_line) >= 2:
                    for vr, vc in vertical_line:
                        output_grid[vr, vc] = 1  # Change to blue
                        visited[vr, vc] = True

    # Process horizontal lines
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5 and not visited[r, c]:
                horizontal_line = get_horizontal_line(r, c)
                line_len = len(horizontal_line)
                if line_len >= 3:
                    if line_len == 3:
                        color = 2  # Red
                    elif line_len == 4:
                        color = 4  # Yellow
                    elif line_len == 5:
                        color = 1  # Blue
                    elif line_len == 6:
                        color = 4  # Yellow
                    else:
                        color = 5 # this shouldn't happen, based on the rules.  It means the line is > 6
                    for hr, hc in horizontal_line:
                        output_grid[hr, hc] = color
                        visited[hr,hc] = True

    return output_grid