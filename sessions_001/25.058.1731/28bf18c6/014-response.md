# 28bf18c6 • 014 • refine_coder

---
```python
"""
Transforms an input grid based on the objects it contains. The transformation rules include:

1. Single pixels are copied and stacked vertically.
2. Rectangular objects are copied to the top-left or transformed based on color and size.
3. Red (color 2) objects are transformed into an alternating pattern.
4. Other colored rectangular objects have their width adjusted and filled with an alternating pattern.
"""

import numpy as np

def find_objects(grid):
    """Identifies distinct objects (contiguous regions of same color) in a grid."""
    grid = np.array(grid)
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color):
        """Depth-first search to find all pixels of a contiguous object."""
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return []
        visited[row, col] = True
        object_pixels = [(row, col)]
        object_pixels.extend(dfs(row + 1, col, color))
        object_pixels.extend(dfs(row - 1, col, color))
        object_pixels.extend(dfs(row, col + 1, color))
        object_pixels.extend(dfs(row, col - 1, color))
        return object_pixels

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = dfs(row, col, color)
                if object_pixels:
                    objects.append((color, object_pixels))
    return objects

def get_object_shape(pixels):
    """Calculates the bounding box dimensions (height, width) of an object."""
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return height, width

def transform(input_grid):
    """Transforms the input grid according to the identified rules."""
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)

    if not objects:  # If no objects, return input
        return input_grid.tolist()

    single_pixel_objects = []
    other_objects = []

    for color, pixels in objects:
        height, width = get_object_shape(pixels)
        if height == 1 and width == 1:
            single_pixel_objects.append((color, pixels))
        else:
            other_objects.append((color, pixels))

    # Handle single pixel objects: stack vertically
    if single_pixel_objects:
        output_grid = np.zeros((len(single_pixel_objects), 1), dtype=int)
        for i, (color, _) in enumerate(single_pixel_objects):
            output_grid[i, 0] = color
        if not other_objects: # if there are *only* single pixel objects
            return output_grid.tolist()

    # Handle other objects (rectangles)
    output_grid = None
    for color, pixels in other_objects:
        height, width = get_object_shape(pixels)
        min_row = min(p[0] for p in pixels)
        min_col = min(p[1] for p in pixels)

        if color == 2:  # Red object: alternating pattern
            output_grid = np.zeros((3, width * 2), dtype=int)
            for i in range(width):
                output_grid[0, 2 * i + 1] = 2
            output_grid[1, :] = 2
            for i in range(width):
                output_grid[2, 2 * i + 1] = 2

        elif height == 3 and width == 5:  # 3x5 object, copy
            output_grid = np.zeros((height, width), dtype=int)
            for r in range(height):
                for c in range(width):
                    if (min_row + r, min_col + c) in pixels:
                        output_grid[r, c] = color

        else:  # Other colored objects
            output_width = 2 * width - 1
            output_grid = np.zeros((1, output_width), dtype=int)
            for i in range(output_width):
                output_grid[0, i] = color if i % 2 == 0 else 0
    
    if len(other_objects) == 0: # single pixel case
        return output_grid.tolist()

    if other_objects and single_pixel_objects: # if we have already created stacked objects
        # Find dimensions
        num_rows = len(single_pixel_objects)
        _, num_cols = output_grid.shape
        stacked_grid = np.zeros((num_rows,1),dtype=int)
        for i, (color,_) in enumerate(single_pixel_objects):
            stacked_grid[i,0] = color

        #Combine with other objects output
        combined_height = max(num_rows, output_grid.shape[0])
        combined_width = max(1, output_grid.shape[1])
        combined_grid = np.zeros((combined_height, combined_width), dtype=int)
        combined_grid[:num_rows, :1] = stacked_grid
        combined_grid[:output_grid.shape[0], :output_grid.shape[1]] = output_grid

        return combined_grid.tolist()
    
    return output_grid.tolist()
```
