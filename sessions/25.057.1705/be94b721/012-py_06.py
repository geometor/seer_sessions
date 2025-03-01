"""
1.  **Identify Objects:** Find all contiguous regions of the same color (objects) in the input grid, ignoring the background color (0).
2.  **Find the Largest Object:** Determine the object with the largest number of pixels.
3.   **Create the output.** Create a rectangular output grid that is filled with pixels of the same color of the largest object. The total number of pixels in the output grid must equal the number of pixels in the largest object.
     * If the height of the largest object is greater or equal to the width, the output grid should have the same height as the largest object, and the width must be the number of pixels divided by the height.
     * If the width of the largest object is greater than the height, the output grid should have the same width as the largest object, and the height is the number of pixels divided by the width.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color (objects) in the grid.
    Ignores the background color (0).
    Returns a list of objects, where each object is a dictionary containing
    the color and a list of pixel coordinates.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels and color != 0:  # Ignore background
                    objects.append({"color": color, "pixels": object_pixels})
    return objects

def get_largest_object(objects):
    """
    Finds the object with the most pixels.
    """
    largest_object = None
    max_pixels = 0
    for obj in objects:
        if len(obj["pixels"]) > max_pixels:
            max_pixels = len(obj["pixels"])
            largest_object = obj
    return largest_object

def get_object_dimensions(object_pixels):
    """
    Calculates the bounding box dimensions (height, width) of an object.
    """
    if not object_pixels:
        return 0, 0

    min_row = min(pixel[0] for pixel in object_pixels)
    max_row = max(pixel[0] for pixel in object_pixels)
    min_col = min(pixel[1] for pixel in object_pixels)
    max_col = max(pixel[1] for pixel in object_pixels)

    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width

def transform(input_grid):
    """
    Transforms the input grid according to the defined rule.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    # Find the largest object
    largest_object = get_largest_object(objects)

    if largest_object is None:
        return []

    # Count pixels of the largest object
    pixel_count = len(largest_object["pixels"])
    object_color = largest_object["color"]

    # get dimensions of largest object
    height, width = get_object_dimensions(largest_object["pixels"])

    # Determine output dimensions
    if height >= width:
      output_height = height
      output_width = pixel_count // output_height
    else:
      output_width = width
      output_height = pixel_count // output_width

    # Create output grid
    output_grid = np.full((output_height, output_width), object_color, dtype=int)

    return output_grid.tolist()