"""
1. **Identify Potential Target Objects:** Examine the input grid and identify all distinct contiguous objects (blocks of connected pixels of the same non-zero color).
2. **Select Target:** For each example, find a 3x3 object that is the focus of the transformation.
3. **Determine Bounding Box:** Find the smallest rectangle (bounding box) that completely encloses the target object.
4. **Create Output Grid:** Create a new, empty grid with the dimensions of the bounding box (always 3x3 in these examples).
5. **Copy and Extract:** Copy the target object from the input grid to the output grid, preserving its shape and color.  The position of the object within the bounding box in the input grid is preserved in the output grid.
"""

import numpy as np

def find_all_objects(grid):
    # Find all distinct contiguous objects in the grid
    rows, cols = grid.shape
    visited = set()
    objects = []

    def flood_fill(row, col, color):
        pixels = []
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
                pixels.append((r, c))
                stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
        return pixels

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                object_pixels = flood_fill(r, c, color)
                if object_pixels:
                    objects.append((object_pixels, color))
    return objects

def get_bounding_box(pixels):
    # Find min and max row/col to define bounding box
    if not pixels:
        return 0, 0, 0, 0
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return min_row, max_row, min_col, max_col

def check_3x3_object(pixels, color, grid):
    # Checks if an object is a 3x3 block
    min_row, max_row, min_col, max_col = get_bounding_box(pixels)
    if (max_row - min_row + 1) == 3 and (max_col - min_col + 1) == 3:
        return True

    return False

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find all distinct objects
    all_objects = find_all_objects(grid)

    # Select 3x3 Target
    target_object = None
    target_color = 0
    for obj_pixels, color in all_objects:
        if check_3x3_object(obj_pixels, color, grid):
          target_object = obj_pixels
          target_color = color
          break # added this to test target object selection
    
    #If not found exit
    if target_object is None:
        return grid.tolist()

    # Get the bounding box of the target object (should already be 3x3)
    min_row, max_row, min_col, max_col = get_bounding_box(target_object)


    # Create the output grid (3x3)
    output_grid = np.zeros((3, 3), dtype=int)

    # Copy the object to the output grid
    for r, c in target_object:
        output_grid[r - min_row, c - min_col] = target_color

    return output_grid.tolist()