```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify all contiguous objects composed of 'red' pixels (color 2) in the input grid.
2. For each red object found, calculate its size (number of pixels it contains).
3. Determine a maximum Manhattan distance threshold 'D' for each object based on its size 'L': D = (L - 1) // 2.
4. Create an output grid initialized as a copy of the input grid.
5. Iterate through each pixel (r, c) in the input grid.
6. If the pixel at (r, c) is not red (i.e., color is not 2):
    a. Find the minimum Manhattan distance ('min_dist') from this pixel (r, c) to *any* red pixel in the grid.
    b. Identify the specific red pixel ('closest_red_pixel') that yields this minimum distance.
    c. Determine which red object the 'closest_red_pixel' belongs to.
    d. Retrieve the pre-calculated distance threshold 'D' associated with that specific red object.
    e. If 'min_dist' is greater than 0 and less than or equal to 'D', change the color of the pixel at (r, c) in the output grid to 'azure' (color 8).
7. Return the modified output grid.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color using Breadth-First Search (BFS).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        tuple: A tuple containing:
            - list: A list where each element is a set of (row, col) tuples representing an object.
            - dict: A dictionary mapping each pixel (row, col) of the specified color to its object ID (index in the list).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    pixel_to_object_map = {}
    object_id_counter = 0

    for r in range(height):
        for c in range(width):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_id = object_id_counter

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    pixel_to_object_map[(row, col)] = obj_id

                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the correct color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Add the found object to the list if it's not empty
                if current_object_coords:
                    objects.append(current_object_coords)
                    object_id_counter += 1

    return objects, pixel_to_object_map

def calculate_manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Fills areas around red objects with azure based on Manhattan distance
    relative to the size of the nearest object.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    red_color = 2
    azure_color = 8

    # 1. Find all red pixels
    red_pixels = list(zip(*np.where(input_np == red_color)))
    if not red_pixels:
        # If there are no red pixels, return the original grid
        return input_grid

    # 2. Find red objects and map pixels to objects
    objects, pixel_to_object_map = find_objects(input_np, red_color)

    # 3. Calculate size and distance threshold D for each object
    object_details = {}
    for obj_id, obj_coords in enumerate(objects):
        length = len(obj_coords)
        threshold_D = (length - 1) // 2
        object_details[obj_id] = {'coords': obj_coords, 'length': length, 'threshold': threshold_D}

    # 4. Iterate through all pixels in the grid
    for r in range(height):
        for c in range(width):
            # 5. Only consider changing non-red pixels
            if input_np[r, c] != red_color:
                min_dist = float('inf')
                closest_red_pixel = None

                # 6a. Find the minimum Manhattan distance to any red pixel
                for r_red, c_red in red_pixels:
                    dist = calculate_manhattan_distance((r, c), (r_red, c_red))
                    if dist < min_dist:
                        min_dist = dist
                        closest_red_pixel = (r_red, c_red)

                # Proceed only if a closest red pixel was found and the distance is > 0
                if closest_red_pixel is not None and min_dist > 0:
                    # 6b & 6c. Find the object this closest pixel belongs to
                    obj_id = pixel_to_object_map.get(closest_red_pixel)

                    if obj_id is not None:
                       # 6d. Get the threshold distance D for that object
                       threshold_D = object_details[obj_id]['threshold']

                       # 6e. If the min distance is within the threshold, color azure
                       if min_dist <= threshold_D:
                           output_np[r, c] = azure_color

    # 7. Return the modified grid as a list of lists
    return output_np.tolist()

```