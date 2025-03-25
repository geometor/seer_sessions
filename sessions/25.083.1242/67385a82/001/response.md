```python
"""
Iterate through each pixel of the input grid. Identify green (3) pixels. For each green pixel, check for adjacent white (0) pixels. Count the number of adjacent white pixels. If a green pixel has two or more adjacent white neighbors (up, down, left, or right), replace it with an azure (8) pixel in the output grid. If a green pixel has fewer than two adjacent white pixels, or if it is any other color, copy the original pixel value to the output grid. Return the modified output grid.
"""

import numpy as np

def count_adjacent_white_pixels(grid, row, col):
    """Counts the number of white (0) pixels adjacent to a given cell."""
    count = 0
    rows, cols = grid.shape
    # Check up
    if row > 0 and grid[row - 1, col] == 0:
        count += 1
    # Check down
    if row < rows - 1 and grid[row + 1, col] == 0:
        count += 1
    # Check left
    if col > 0 and grid[row, col - 1] == 0:
        count += 1
    # Check right
    if col < cols - 1 and grid[row, col + 1] == 0:
        count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is green (3)
            if input_grid[row, col] == 3:
                # Count adjacent white pixels
                adjacent_whites = count_adjacent_white_pixels(input_grid, row, col)
                # Replace with azure (8) if at least two adjacent whites
                if adjacent_whites >= 2:
                    output_grid[row, col] = 8

    return output_grid
```