"""
1.  **Background:** Identify color 7 (orange) as the background. Pixels of this color in the input grid remain unchanged in the output grid.

2.  **Center Column:**
    *   Find the center column of the grid (index = `cols // 2`).
    *   Examine each pixel in the center column of the *input* grid.
        *   If a pixel's value is 3 (green):
            *   If the pixel's row index is *less than* the center row index (`rows // 2`), change the corresponding pixel in the *output* grid to 2 (red).
            *   If the pixel's row index is *greater than* the center row index (`rows // 2`), change the corresponding pixel in the *output* grid to 4 (yellow).
            *   If the pixels row index is equal to the center row index (`rows // 2`), do not perform this transformation.
        * If a pixel has value of 9, 4, or 5:
            * It is unchanged.

3.  **Corners and Edges:**
    *   Iterate through all pixels on the edges of the grid (where `row == 0` or `row == rows - 1` or `col == 0` or `col == cols - 1`).
    * For each edge pixel in the *input* grid:
        *   Examine its neighboring pixels (including diagonals) in the *input* grid.
        *   If *any* of these neighboring pixels have the background color (7), perform the following:
            *   Create a list of the colors of the *non-background* neighboring pixels.
            *  If the list of non-background neighbors is empty do not perform the transform.
            *   Find the most frequent color (mode) in this list.
            *   Set the corresponding pixel in the *output* grid to this mode color.

4. **Other Pixels**
    * If a pixel does not meet the condition for the central column or edges, and is not the background color, do not change it, copy the input color to the output.

5.  **Output:** The output grid is created by applying the above rules to the input grid.
"""

import numpy as np
from scipy.stats import mode

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            # Background remains unchanged
            if input_grid[r, c] == 7:
                continue

            # Center Column Transformations
            if c == center_col:
                if input_grid[r, c] == 3:
                    if r < center_row:
                        output_grid[r, c] = 2  # Change to red
                    elif r > center_row:
                        output_grid[r, c] = 4  # Change to yellow
                #For colors 4, 5 and 9, they are unchanged
                else:
                    output_grid[r,c] = input_grid[r,c]


            # Edge Transformations
            elif r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                neighbors = get_neighbors(input_grid, r, c)
                if 7 in neighbors:  # Check if any neighbor is background
                    non_background_neighbors = [val for val in neighbors if val != 7]
                    if non_background_neighbors: #Ensure list is not empty
                         output_grid[r,c] = mode(non_background_neighbors)[0]
                    else: #If list is empty do not perform the transformation
                         output_grid[r,c] = input_grid[r,c]
                else:
                    output_grid[r,c] = input_grid[r,c] # added to ensure the edge colors are copied
            # Other pixels
            else:
                 output_grid[r,c] = input_grid[r,c]

    return output_grid