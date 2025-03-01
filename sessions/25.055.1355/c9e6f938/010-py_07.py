"""
Identifies all contiguous blocks of orange (7) pixels in the input grid and expands them horizontally, doubling their width. Other color pixels remain in their original positions within the expanded grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous objects (blocks of same color) in a grid.
    Returns a list of objects, where each object is a dictionary containing:
    - color: The color of the object.
    - pixels: A list of (row, col) tuples representing the object's pixels.
    - top_left: top-left corner
    - bottom_right: bottom-right corner
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, pixels):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        pixels.append((row, col))
        dfs(row + 1, col, color, pixels)
        dfs(row - 1, col, color, pixels)
        dfs(row, col + 1, color, pixels)
        dfs(row, col - 1, color, pixels)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                pixels = []
                dfs(row, col, color, pixels)
                if pixels:
                    # find top_left, bottom_right
                    pixels_array = np.array(pixels)
                    min_row, min_col = np.min(pixels_array, axis=0)
                    max_row, max_col = np.max(pixels_array, axis=0)
                    objects.append({
                        "color": color,
                        "pixels": pixels,
                        "top_left": (min_row, min_col),
                        "bottom_right": (max_row, max_col)
                    })
    return objects

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    # Calculate maximum expansion needed
    max_expansion = 0
    for obj in objects:
        if obj["color"] == 7:
            width = obj["bottom_right"][1] - obj["top_left"][1] + 1
            max_expansion = max(max_expansion, width)

    # Initialize output grid with white pixels, and sufficient width expansion
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] + max_expansion), dtype=int)

    # Copy and expand orange objects, copy other color objects
    for obj in objects:
        if obj["color"] == 7:
            # Calculate original width
            original_width = obj["bottom_right"][1] - obj["top_left"][1] + 1
            expansion_amount = original_width

            # copy and expand
            for row, col in obj["pixels"]:
                output_grid[row, col] = 7  # Original position
                output_grid[row, col + expansion_amount] = 7  # Expanded position

        else:
            # copy all other color pixels
            for row, col in obj["pixels"]:
                output_grid[row, col] = obj["color"]

    return output_grid