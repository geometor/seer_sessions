import numpy as np
from collections import deque

"""
Identifies all distinct solid yellow (4) rectangles in the input grid.
For each rectangle, determines its interior pixels (yellow pixels surrounded cardinally by other yellow pixels).
Calculates the area of the interior for each rectangle.
Compares the interior areas: the rectangle with the largest interior area has its interior colored red (2),
and the rectangle with the smallest interior area has its interior colored blue (1).
The yellow borders of the rectangles and the background remain unchanged.
Assumes exactly two yellow rectangles with distinct interior areas, based on the examples.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the coordinates (row, col)
              of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_pixels.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def find_interior_pixels(grid, obj_pixels):
    """
    Finds the interior pixels of a given object within the grid.
    An interior pixel is one belonging to the object whose four cardinal neighbors
    also belong to the object (or are the same color).

    Args:
        grid (np.array): The input grid (used for boundary checks and color).
        obj_pixels (set): A set of (row, col) coordinates for the object.

    Returns:
        set: A set of (row, col) coordinates for the interior pixels.
              Returns an empty set if the object has no interior.
    """
    interior_pixels = set()
    rows, cols = grid.shape
    object_color = grid[next(iter(obj_pixels))] # Get the color of the object

    for r, c in obj_pixels:
        is_interior = True
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds AND has the same color
            if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == object_color):
                is_interior = False
                break
        if is_interior:
            interior_pixels.add((r, c))
            
    # Alternative simpler check (given solid rectangles): Check if all neighbors are part of the object pixel set.
    # interior_pixels = set()
    # for r, c in obj_pixels:
    #     is_interior = True
    #     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    #         nr, nc = r + dr, c + dc
    #         if (nr, nc) not in obj_pixels:
    #             is_interior = False
    #             break
    #     if is_interior:
    #         interior_pixels.add((r,c))

    return interior_pixels


def transform(input_grid):
    """
    Transforms the input grid by coloring the interiors of yellow rectangles.

    Args:
        input_grid (np.array): The input 2D array representing the grid.

    Returns:
        np.array: The transformed 2D array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    yellow_color = 4
    red_color = 2
    blue_color = 1

    # Find all yellow objects (rectangles in this case)
    yellow_objects = find_objects(output_grid, yellow_color)

    object_data = []
    # Calculate interior area for each yellow object
    for obj_pixels in yellow_objects:
        interior = find_interior_pixels(output_grid, obj_pixels)
        interior_area = len(interior)
        object_data.append({
            'pixels': obj_pixels,
            'interior_pixels': interior,
            'interior_area': interior_area
        })

    # Check if we found exactly two objects (as per examples)
    if len(object_data) == 2:
        # Sort objects by interior area (ascending)
        object_data.sort(key=lambda x: x['interior_area'])

        smaller_obj = object_data[0]
        larger_obj = object_data[1]

        # Color the interior of the smaller object blue
        for r, c in smaller_obj['interior_pixels']:
            output_grid[r, c] = blue_color

        # Color the interior of the larger object red
        for r, c in larger_obj['interior_pixels']:
            output_grid[r, c] = red_color
            
    # If not exactly two objects, or if areas are equal, the current logic
    # based on examples won't apply perfectly. For now, it will either do nothing
    # (if 0 or 1 object) or potentially miscolor if areas are equal or more than 2 objects exist.
    # The problem description implies exactly two objects with distinct areas.

    return output_grid