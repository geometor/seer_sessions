"""
1.  **Identify the Object:** Find the contiguous region of non-background (non-zero) pixels within the input grid. This constitutes the single object. Note the color of the object.

2.  **Double Dimensions:** Create an output grid with dimensions exactly double those of the input grid. Initialize all pixels in the output grid to the background color (0).

3. **Draw a 2x Scaled Outline:**
    - Iterate through the input grid, pixel by pixel.
    - If the current pixel from the input grid contains the object color, determine if the pixel is an edge pixel:
        - A pixel is an edge if it has at least one adjacent pixel (up, down, left or right) which has a different color.
    - If the input pixel is part of the object, scale the coordinates by a factor of 2. Set the output grid pixels at `(2i, 2j)`, `(2i + 1, 2j)`, `(2i, 2j + 1)`, and `(2i + 1, 2j + 1)` to be object color.

4.  **Output:** The output grid now contains a 2x scaled outline of the object, with the background color elsewhere.
"""

import numpy as np

def is_edge(grid, row, col):
    """
    Checks if a pixel at (row, col) is on the edge of its object in the grid.
    """
    rows, cols = grid.shape
    color = grid[row, col]

    # Check adjacent pixels (up, down, left, right)
    if row > 0 and grid[row - 1, col] != color:
        return True
    if row < rows - 1 and grid[row + 1, col] != color:
        return True
    if col > 0 and grid[row, col - 1] != color:
        return True
    if col < cols - 1 and grid[row, col + 1] != color:
        return True

    return False

def transform(input_grid):
    # Double Dimensions: Create output grid, initialized with zeros.
    rows, cols = input_grid.shape
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Identify the Object and its color.
    object_color = 0
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                object_color = input_grid[r, c]
                break  # Optimization: Exit inner loop once object color is found
        if object_color != 0:
            break # Exit loop

    # Draw a 2x Scaled Outline
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == object_color: # if the pixel is part of the object
                if is_edge(input_grid, i, j):
                  # Scale coordinates and set output pixels.
                  output_grid[2 * i, 2 * j] = object_color
                  output_grid[2 * i + 1, 2 * j] = object_color
                  output_grid[2 * i, 2 * j + 1] = object_color
                  output_grid[2 * i + 1, 2 * j + 1] = object_color

    return output_grid