import numpy as np
from collections import deque

"""
Recolor blue (1) objects based on the shape of the spatially closest orange (7) object, then remove the orange objects.

The transformation rule involves the following steps:
1. Identify all distinct contiguous objects composed of blue (1) pixels and orange (7) pixels in the input grid.
2. For each orange object, determine its unique shape. The shape is defined as the pattern of orange pixels within the object's minimal bounding box, represented as a tuple of tuples.
3. Establish a mapping between these specific orange object shapes and target output colors:
    - Shape ((0, 7), (7, 7)) maps to Green (3).
    - Shape ((7, 7), (7, 0)) maps to Magenta (6).
    - Shape ((7, 7), (0, 7)) maps to Yellow (4).
    - Shape ((7, 0), (7, 7)) maps to Azure (8).
4. For each blue object:
    a. Calculate the minimum Manhattan distance to every orange object. The distance is measured between any pixel of the blue object and any pixel of the orange object.
    b. Identify the orange object that is closest to the blue object.
    c. Retrieve the shape of this closest orange object.
    d. Use the shape-to-color mapping to determine the target output color for the blue object.
5. Create an output grid initialized with the background color (white, 0).
6. For each blue object, color its corresponding pixels in the output grid with its determined target output color. Orange objects are not drawn in the output grid.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is represented as a set of
              (row, col) coordinate tuples.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4-directional neighbors (ARC standard for contiguity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                objects.append(obj_coords)
    return objects

def get_object_shape(grid, obj_coords):
    """
    Calculates the shape of an object based on its pixels within its minimal bounding box.

    Args:
        grid (np.array): The input grid (needed for color values).
        obj_coords (set): A set of (row, col) coordinates for the object.

    Returns:
        tuple: A tuple of tuples representing the object's shape within its
               bounding box, including background pixels within the box.
               Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None

    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Use object's color, not just 7, in case this is reused
    obj_color = grid[min_r, min_c] if (min_r, min_c) in obj_coords else grid[list(obj_coords)[0]]


    shape_grid = np.zeros((height, width), dtype=int)

    for r, c in obj_coords:
        shape_grid[r - min_r, c - min_c] = grid[r,c] # Use actual color

    # Convert to tuple of tuples for hashing
    return tuple(map(tuple, shape_grid))

def min_manhattan_distance(obj1_coords, obj2_coords):
    """
    Calculates the minimum Manhattan distance between two objects.

    Args:
        obj1_coords (set): Set of (row, col) coordinates for object 1.
        obj2_coords (set): Set of (row, col) coordinates for object 2.

    Returns:
        int: The minimum Manhattan distance between any pixel in obj1 and
             any pixel in obj2. Returns infinity if either object is empty.
    """
    if not obj1_coords or not obj2_coords:
        return float('inf')

    min_dist = float('inf')
    for r1, c1 in obj1_coords:
        for r2, c2 in obj2_coords:
            dist = abs(r1 - r2) + abs(c1 - c2)
            min_dist = min(min_dist, dist)
    return min_dist

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros_like(input_grid_np) # Initialize with background color 0

    # 1. Find blue and orange objects
    blue_objects = find_objects(input_grid_np, 1)
    orange_objects = find_objects(input_grid_np, 7)

    if not blue_objects or not orange_objects:
        return output_grid.tolist() # Return background if no blue or no orange objects

    # 2. Precompute shapes for orange objects
    orange_shapes = [get_object_shape(input_grid_np, obj_coords) for obj_coords in orange_objects]

    # 3. Define the shape-to-color mapping
    SHAPE_COLOR_MAP = {
        ((0, 7), (7, 7)): 3,  # Green
        ((7, 7), (7, 0)): 6,  # Magenta
        ((7, 7), (0, 7)): 4,  # Yellow
        ((7, 0), (7, 7)): 8,  # Azure
    }

    # 4. Process each blue object
    for blue_coords in blue_objects:
        min_dist = float('inf')
        closest_orange_idx = -1

        # 4a. Calculate minimum distances to all orange objects
        for idx, orange_coords in enumerate(orange_objects):
            dist = min_manhattan_distance(blue_coords, orange_coords)
            if dist < min_dist:
                min_dist = dist
                closest_orange_idx = idx
            # Tie-breaking: Implicitly picks the first one found in the list
            # (consistent iteration order should handle this deterministically)

        if closest_orange_idx != -1:
            # 4c. Get the shape of the closest orange object
            closest_orange_shape = orange_shapes[closest_orange_idx]

            # 4d. Determine output color from shape
            output_color = SHAPE_COLOR_MAP.get(closest_orange_shape)

            # 6. Color the blue object's pixels in the output grid
            if output_color is not None:
                for r, c in blue_coords:
                    output_grid[r, c] = output_color
            # else: handle case where shape is not in map (optional: error or default color)
            # Based on training examples, all shapes should be in the map.

    return output_grid.tolist()