"""
1. **Identify the Target Object:** In each input grid, identify the largest contiguous block (object) of a specific non-zero color. The target color changes in each example, and seems to be the uppermost and leftmost.
2. **Determine Bounding Box:** Find the smallest rectangle (bounding box) that completely encloses the target object. This defines the dimensions of the output.
3. **Create Output Grid:**  Create a new, empty grid with the dimensions of the bounding box determined in step 2.
4. **Copy and Extract:** Copy the target object from the input grid to the output grid, preserving its shape and color.  The position of the object within the bounding box in the input grid is preserved in the output grid.
"""

import numpy as np

def find_target_object(grid):
    # Find the uppermost, leftmost non-zero color
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                target_color = grid[r, c]
                # Use a flood fill algorithm to find connected component
                object_pixels = flood_fill(grid, r, c, target_color)
                return object_pixels, target_color
    return [], 0

def flood_fill(grid, row, col, target_color):
     # Standard flood fill to get contiguous object
    rows, cols = grid.shape
    pixels = []
    stack = [(row, col)]
    visited = set()

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == target_color:
            pixels.append((r, c))
            # Add adjacent cells to the stack
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
    return pixels

def get_bounding_box(pixels):
    # Find min and max row/col to define the bounding box
    if not pixels:
        return 0, 0, 0, 0
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find the target object (connected component)
    object_pixels, target_color = find_target_object(grid)

    # Get the bounding box of the target object
    min_row, max_row, min_col, max_col = get_bounding_box(object_pixels)

    # Create the output grid based on the bounding box
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the object to the output grid
    for r, c in object_pixels:
        output_grid[r - min_row, c - min_col] = target_color

    return output_grid.tolist()