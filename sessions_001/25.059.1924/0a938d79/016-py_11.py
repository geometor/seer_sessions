"""
1.  **Identify Key Pixels:** Locate the single red (2) and green (3) pixels in the input grid.
2.  **Expand Red:** Replace all pixels in the row containing the red pixel with the value 2 (red).
3.  **Expand Green:** Replace all pixels in the row containing the green pixel with the value 3 (green).
4.  **Alternate and Repeat:** Starting from the row of the Red Pixel, alternate filling subsequent rows with red (2) and green (3) downwards and upwards, creating repeating two row chunks of one red, and one green, row.
5. **Maintain Grid Size:** The output grid retains the same dimensions (width and height) as the input grid.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if pixel == color:
                return (i, j)  # (row, col)
    return None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Initialize output grid with the same dimensions and filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find the red and green pixels
    red_pos = find_pixel(input_grid, 2)
    green_pos = find_pixel(input_grid, 3)

    if red_pos is None or green_pos is None:
      return output_grid

    # Expand red and green rows in place
    output_grid[red_pos[0], :] = 2
    output_grid[green_pos[0], :] = 3


    # Alternate and repeat the pattern, moving upwards
    current_color = 2
    for r in range(red_pos[0] -2, -1, -2):
        output_grid[r,:] = current_color
        current_color = 3 if current_color == 2 else 2
        if r -1 >= 0:
           output_grid[r-1,:] = current_color

    # Alternate and repeat the pattern, moving downwards.
    current_color = 3
    for r in range(red_pos[0] + 2, output_grid.shape[0],2):
        output_grid[r,:] = current_color
        current_color = 3 if current_color == 2 else 2
        if r + 1 < output_grid.shape[0]:
            output_grid[r+1, :] = current_color
            


    return output_grid