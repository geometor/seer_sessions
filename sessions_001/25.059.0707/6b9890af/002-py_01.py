"""
1.  **Identify Objects:** Scan the input grid and identify all distinct, contiguous colored regions (objects) that are not white (0). The input contains two distinct colored regions.
2.  **Define a Bounding Box**. Identify the smallest rectangular region that fully encloses any two objects.
3. **Create Output Border:** Construct a rectangular output grid, equal to the dimensions of the bounding box. Fill this rectangle with red color (2).
4.  **Transfer Inner Objects:** For the detected objects inside the bounding box in the input, copy their pixels to the corresponding positions within the output grid, inside the bounding box. The empty areas inside the bounding box are all white color (0).
5.  **Output:** The final output is the new, smaller rectangular grid.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct colored objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find contiguous pixels of the same color."""
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
            if not visited[row, col] and grid[row, col] != 0:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": object_pixels}
                )
    return objects

def create_bounding_box(objects):
    """Creates a bounding box around the two objects."""
    if len(objects) < 2:
      return None, None, None, None    
    
    all_pixels = []

    for i in range(len(objects)):
            all_pixels.extend(objects[i]["pixels"])


    min_row = min(pixel[0] for pixel in all_pixels)
    max_row = max(pixel[0] for pixel in all_pixels)
    min_col = min(pixel[1] for pixel in all_pixels)
    max_col = max(pixel[1] for pixel in all_pixels)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find distinct objects
    objects = find_objects(input_grid)
    
    # Define bounding box
    min_row, max_row, min_col, max_col = create_bounding_box(objects)

    if min_row is None:
        return np.array([[0]]) # Return a default 1x1 grid if no objects are found

    # Create output grid
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = np.zeros((height, width), dtype=int)

    #draw red border around output
    for row in range(height):
      for col in range(width):
        if row == 0 or row == height -1 or col == 0 or col == width-1:
          output_grid[row,col] = 2


    # Transfer object pixels, offsetting by min_row and min_col
    for obj in objects:
      if obj['color'] != 2: #make sure not to overwrite border
        for row, col in obj["pixels"]:
            new_row = row - min_row
            new_col = col - min_col
            if 0 < new_row < height -1 and 0 < new_col < width - 1: #make sure object is fully within red border
              output_grid[new_row, new_col] = obj["color"]

    return output_grid