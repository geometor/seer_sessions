"""
1.  **Identify the Center:** The output grid is a 3x3 square. Find the center cell of the input grid. In this case the center of the input is at position (1,3).

2.  **Extract Central Object:** Observe the color number in that center cell. The color number there is 5 (grey).

3.  **Count Blue Objects Adjacent to Center:** Count the number of blue (1) objects adjacent to the center gray object (5) at (1, 3) in the input grid. Adjacent includes cells touching by sides, cells touching by corners.

4.  **Place Count Value in Center of output:** Create a 3x3 grid filled with white (0) objects.

5. **Modify output:** IF the number of adjacent blue object is an odd number, split the input in 3 horizontal stripes of width 1, centered on the center of the input. Place a red object at the intersection of each stripe and the first column from the left. If the number is even, split the input in 3 vertical stripes of width 1, centered on the center of the input. Place a red object at the intersection of each stripe and the middle line.
"""

import numpy as np

def count_adjacent_objects(grid, center_row, center_col, target_color):
    # helper function
    # Count the number of objects of a target color adjacent to a center cell
    count = 0
    rows, cols = grid.shape
    for i in range(max(0, center_row - 1), min(rows, center_row + 2)):
        for j in range(max(0, center_col - 1), min(cols, center_col + 2)):
            if (i != center_row or j != center_col) and grid[i, j] == target_color:
                count += 1
    return count

def transform(input_grid):
    # Initialize a 3x3 output grid filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the center cell of the input grid.
    center_row, center_col = 1, 3

    # Count the number of blue (1) objects adjacent to the center.
    blue_count = count_adjacent_objects(input_grid, center_row, center_col, 1)

    # if the number of blue objects is odd.
    if blue_count %2 != 0:
        output_grid[1,0] = 2
        output_grid[2,2] = 2

    else:
        output_grid[0,1] = 2
        output_grid[1,2] = 2
        output_grid[2,1] = 2


    return output_grid