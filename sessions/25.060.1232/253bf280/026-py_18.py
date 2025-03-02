"""
1.  **Identify Azure Pixels:** Find all pixels with color 8 (azure).
2.  **Identify Pairs:** Group the azure pixels that share the same column (x-coordinate).
3.  **Draw Green Lines Conditionally:** For each pair of vertically aligned azure pixels:
    *   Start drawing a vertical line of color 3 (green) from the row *immediately below* the upper azure pixel.
    *   Continue drawing the line downwards.
    *   Stop drawing the line at the row *immediately above* the lower azure pixel.
    *   **Crucially, if any other azure pixel is encountered *during* the line drawing, stop drawing *before* reaching that azure pixel.**
4. **Preserve Original Azure Pixels**: The azure pixels are preserved.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.array(np.where(grid == color)).T.tolist()

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure pixels
    azure_pixels = find_pixels_by_color(input_grid, 8)

    # Group azure pixels by column
    azure_pixels_by_column = {}
    for r, c in azure_pixels:
        if c not in azure_pixels_by_column:
            azure_pixels_by_column[c] = []
        azure_pixels_by_column[c].append((r, c))

    # Draw green lines conditionally
    for col, pixels in azure_pixels_by_column.items():
        # Sort pixels by row (top to bottom)
        pixels.sort()
        for i in range(len(pixels) - 1):
            start_row = pixels[i][0] + 1
            end_row = pixels[i+1][0]

            # Draw the green line, checking for other azure pixels
            for row in range(start_row, end_row):
                if output_grid[row, col] == 8:  # Check for azure pixel
                    break  # Stop drawing if another azure pixel is found
                output_grid[row, col] = 3

    return output_grid