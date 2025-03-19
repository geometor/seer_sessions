# e76a88a6 • 008 • refine_coder

---
```python
"""
1. Identify Gray Rectangles: The input grid is scanned to identify contiguous regions of gray (5) pixels. These regions are treated as rectangular objects.
2. Determine Dimensions: For each gray rectangle, the width and height are calculated.
3. Replace with Red and Yellow: The gray rectangle is replaced with a rectangle of the same dimensions, composed of red (2) and yellow (4) pixels.
4. L-Shape creation. The top row and leftmost column are colored red. The bottom row and rightmost column are colored yellow. If the object is only one pixel wide or tall, then the color will be red.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        """Depth-first search to find contiguous pixels of the same color."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def create_l_shape_replacement(width, height):
    """Creates a rectangular replacement pattern with L-shapes of red and yellow."""
    replacement = np.zeros((height, width), dtype=int)
    for r in range(height):
        for c in range(width):
            if r == 0:  # Top row - red
                replacement[r, c] = 2
            elif c == 0: # Leftmost col, red
                replacement[r,c] = 2
            elif r == height -1: # Bottom Row - Yellow
                replacement[r,c] = 4
            elif c == width -1: #rightmost col - Yellow
                replacement[r,c] = 4
    return replacement


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Find gray objects
    gray_objects = [obj for obj in objects if obj['color'] == 5]

    for gray_object in gray_objects:
        # Find the bounding box
        min_row = min(pixel[0] for pixel in gray_object['pixels'])
        max_row = max(pixel[0] for pixel in gray_object['pixels'])
        min_col = min(pixel[1] for pixel in gray_object['pixels'])
        max_col = max(pixel[1] for pixel in gray_object['pixels'])

        width = max_col - min_col + 1
        height = max_row - min_row + 1

        # Create the replacement rectangle
        replacement_rectangle = create_l_shape_replacement(width, height)

        # Replace the grey object's pixels
        for r in range(height):
            for c in range(width):
                # Map the replacement rectangle to output coordinates.
                output_row = min_row + r
                output_col = min_col + c

                if 0 <= output_row < output_grid.shape[0] and 0 <= output_col < output_grid.shape[1]:
                    output_grid[output_row, output_col] = replacement_rectangle[r, c]

    return output_grid
```

