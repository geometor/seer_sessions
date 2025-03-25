"""
1.  **Identify Yellow Pixels:** Locate all yellow (4) pixels in the input grid.

2.  **Determine Bounding Box (Implicit):** Consider pairs of yellow pixels. The transformation occurs within the implicit rectangle defined by the row and column indices of yellow pixels.

3.  **Conditional Red Fill (Horizontal):** For each row, examine pairs of yellow pixels. If *all* pixels between a pair of yellow pixels in that row are white (0), change those white pixels to red (2).

4.  **Conditional Red Fill (Vertical):** For each column, examine pairs of yellow pixels. If *all* pixels between a pair of yellow pixels in that column are white (0), change those white pixels to red (2).

5.  **Interior Fill:** If the yellow pixels form a rectangle (i.e., there are yellow pixels at all four corners of an axis-aligned rectangle), fill the *entire* interior of that rectangle with red (2), provided that all pixels between the yellow pixels on opposite sides of the rectangle are white. This includes both the spaces between the yellow pixels *and* the white pixels inside that rectangle.

6.  **Preservation:** All other pixels (those that are not yellow and were not changed to red) retain their original color in the output grid.
"""

import numpy as np

def get_yellow_pixels(grid):
    # Find coordinates of all yellow pixels (value 4).
    yellow_pixels = np.where(grid == 4)
    return list(zip(yellow_pixels[0], yellow_pixels[1]))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    yellow_pixels = get_yellow_pixels(input_grid)

    # Horizontal Check and Create Red Region
    for row_index in range(input_grid.shape[0]):
        yellow_in_row = [pos for pos in yellow_pixels if pos[0] == row_index]
        yellow_in_row.sort(key=lambda x: x[1])  # Sort by column index
        for i in range(len(yellow_in_row) - 1):
            col1 = yellow_in_row[i][1]
            col2 = yellow_in_row[i+1][1]
            if col1 + 1 != col2:  # not adjacent
               if all(input_grid[row_index, col1 + 1:col2] == 0):
                  output_grid[row_index, col1 + 1:col2] = 2

    # Vertical Check and Create Red Region
    for col_index in range(input_grid.shape[1]):
        yellow_in_col = [pos for pos in yellow_pixels if pos[1] == col_index]
        yellow_in_col.sort(key=lambda x: x[0])  # Sort by row index
        for i in range(len(yellow_in_col) - 1):
            row1 = yellow_in_col[i][0]
            row2 = yellow_in_col[i+1][0]
            if row1 + 1 != row2:  # not adjacent
               if all(input_grid[row1 + 1:row2, col_index] == 0):
                  output_grid[row1 + 1:row2, col_index] = 2

    # Interior Fill
    for (row1, col1) in yellow_pixels:
        for (row2, col2) in yellow_pixels:
            if row1 < row2 and col1 < col2: # Check for top-left and bottom-right corners
                # check for other two corners
                if (row1, col2) in yellow_pixels and (row2, col1) in yellow_pixels:
                    # Check if edges are all white (0)
                    if all(input_grid[row1, col1+1:col2] == 0) and \
                       all(input_grid[row2, col1+1:col2] == 0) and \
                       all(input_grid[row1+1:row2, col1] == 0) and \
                       all(input_grid[row1+1:row2, col2] == 0):
                         output_grid[row1+1:row2, col1+1:col2] = 2 #fill interior


    return output_grid