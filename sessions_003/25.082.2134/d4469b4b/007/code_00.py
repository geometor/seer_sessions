"""
1.  **Find the Cross:** Examine the input grid to identify the largest "cross" shape. A cross consists of orthogonally connected pixels (up, down, left, right – *no diagonals*) of the same non-zero color. The cross must have at least 5 connected pixels to be valid. If there is no cross, the output is a 3x3 grid of zeros.

2.  **Determine the Center:** The cross is made of a horizontal line and a vertical line. Determine the center of the cross to be the intersection point of the longest horizontal line and the longest vertical line of the same color.

3. **Map Input Center to 3x3 Output:** Scale the input cross's center coordinates to fit within the 3x3 output grid. This is done as follows:
    -   Output Row = floor(Input Center Row * 3 / Input Grid Rows)
    -   Output Column = floor(Input Center Column * 3 / Input Grid Columns)

4.  **Construct Output:** Create a 3x3 output grid filled with zeros.

5.  **Draw Gray Cross:** In the output grid, place a gray pixel (value 5) at every cell along the calculated output center row and output center column.

6. **Handle No Cross:** If no valid cross is found, output a 3x3 grid filled with zeros.
"""

import numpy as np

def find_cross(grid):
    """Finds the largest cross shape in the grid (orthogonally connected)."""
    rows, cols = grid.shape
    visited = set()
    max_cross_size = 0
    best_center = None
    cross_color = 0

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def get_line(r, c, dr, dc, color):
        """Gets a line of connected pixels in a given direction."""
        line = []
        while is_valid(r, c) and grid[r, c] == color:
            line.append((r, c))
            visited.add((r,c))
            r += dr
            c += dc
        return line

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                # Get horizontal and vertical lines
                horizontal_line = get_line(r, c, 0, 1, color) + get_line(r, c - 1, 0, -1, color)
                vertical_line = get_line(r, c, 1, 0, color) + get_line(r - 1, c, -1, 0, color)
                
                if len(horizontal_line) >=3 or len(vertical_line) >=3:
                    
                    #find intersection
                    intersection = set(horizontal_line) & set(vertical_line)
                    if intersection:

                        center = list(intersection)[0]

                        # Calculate cross size (assuming a perfect cross)
                        cross_size = len(horizontal_line) + len(vertical_line) -1
                        if cross_size > max_cross_size:
                            max_cross_size = cross_size
                            best_center = center
                            cross_color = color

    if max_cross_size >= 5:
      return best_center, cross_color
    else:
      return None, None


def transform(input_grid):
    """Transforms the input grid according to the cross rule."""
    input_grid = np.array(input_grid)
    center, cross_color = find_cross(input_grid)

    # If no cross, return an empty 3x3 grid
    if center is None:
        return np.zeros((3, 3), dtype=int)

    input_rows, input_cols = input_grid.shape
    # Map input center to 3x3 output grid
    output_row = int(center[0] * 3 / input_rows)
    output_col = int(center[1] * 3 / input_cols)


    # Create the 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the center row and column with gray (5)
    for i in range(3):
        output_grid[output_row, i] = 5
        output_grid[i, output_col] = 5

    return output_grid