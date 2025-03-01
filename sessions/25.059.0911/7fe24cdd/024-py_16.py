"""
1.  **Identify Objects:** Examine the input grid and identify all non-zero pixels. Each of these is an object. Note their color and (row, column) position.
2.  **Horizontal Mirroring:** For each object, calculate its mirrored position along the horizontal axis. The perceived center of the input grid is `(width - 1) / 2`.  The mirrored column is calculated as `2 * center - original_column`.
3. **Determine Output Width**: The output width is twice the input width if the input width is even, or  `input_width + (input_width - 1)` if input width is odd.
4. **Output Grid Creation:** Create a new grid filled with zeros, with dimensions determined in the previous step.
5. **Place Original and Mirrored Objects:** Place each original object in the new grid at its original row and column. Place the mirrored object at the same row and the mirrored column calculated in step 2. If there are multiple colors, mirror each object of each color using the same logic. The order the objects are processed in should not change the outcome.
"""

import numpy as np

def get_object_coordinates(grid, color=None):
    coords = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0 and (color is None or grid[r][c] == color):
                coords.append((r, c))
    return coords

def calculate_mirrored_col(col, width):
    center = (width - 1) / 2
    return int(2 * center - col)

def transform(input_grid):
    # Determine output width
    input_width = len(input_grid[0])
    output_width = input_width * 2 if input_width % 2 == 0 else input_width + (input_width - 1)

    # Initialize output grid with zeros
    output_grid = [[0] * output_width for _ in range(len(input_grid))]

    # Iterate through all colors and their coordinates in the input grid
    for color in range(1, 10):  # Check colors 1-9
        objects = get_object_coordinates(input_grid, color)
        for row, col in objects:
            # Place original object
            output_grid[row][col] = color
            
            # Calculate and place mirrored object
            mirrored_col = calculate_mirrored_col(col, input_width)
            output_grid[row][mirrored_col] = color

    return output_grid