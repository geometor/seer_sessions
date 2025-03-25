"""
1.  **Identify the grid dimensions:** Determine the number of rows and columns.
2.  **Locate Red Pixels:** Find all pixels with the color value 2 (red).
3.  **Bottom Half Check:** Consider only the red pixels located in the bottom half of the grid (row index greater than or equal to rows // 2).
4. **Alternating Change within Row, By Parity:** For each row in the bottom half, set a "start" variable equal to `(row + 1) % 2`. Iterate through each red pixel. If it is the first red pixel in that row and `(row+col) % 2 == start`, change its color to azure (8). If it is a subsequent red pixel and `(row+col)%2` does *not* match the parity of the previous red pixel in that row, change it to azure. Otherwise, leave the pixel's color as red.
5.  **Output:** Produce the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rule described above."""

    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Initialize output grid

    for i in range(rows // 2, rows):  # Iterate only through the bottom half
        start = (i + 1) % 2
        previous_red_parity = None # Track the parity of the *previous* red pixel in the row

        red_pixels_in_row = []
        for j in range(cols):
            if input_grid[i,j] == 2:
                red_pixels_in_row.append((i,j))

        for index, (row, col) in enumerate(red_pixels_in_row):
            current_parity = (row + col) % 2

            if index == 0: #first red pixel
                if current_parity == start:
                  output_grid[row, col] = 8
                previous_red_parity = current_parity
            else: # subsequent red pixels
                if current_parity != previous_red_parity:
                    output_grid[row,col] = 8
                previous_red_parity = current_parity

    return output_grid