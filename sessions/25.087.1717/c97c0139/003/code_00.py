import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all contiguous objects composed of 'red' pixels (color 2) in the input grid.
2. For each red object found:
    a. Calculate its size 'L' (number of pixels).
    b. Determine its distance threshold 'D' = (L - 1) // 2.
    c. Store the object's coordinates and its threshold D.
3. Perform a multi-source Breadth-First Search (BFS) starting from all red pixels simultaneously.
4. The BFS calculates the Manhattan distance ('dist') from each grid cell to the *nearest* red pixel and identifies which red object ('obj_id') that nearest red pixel belongs to.
5. Create an output grid initialized as a copy of the input grid.
6. Iterate through each pixel (r, c) in the grid.
7. If the pixel at (r, c) is not red (i.e., color is not 2) and it was reached by the BFS (meaning it has an associated minimum distance 'dist' and a corresponding 'obj_id' from the nearest red object):
    a. Retrieve the distance threshold 'D' associated with the 'obj_id' of the object that is closest to this pixel (r, c).
    b. If the calculated minimum distance 'dist' is greater than 0 and less than or equal to the threshold 'D', change the color of the pixel at (r, c) in the output grid to 'azure' (color 8).
8. Return the modified output grid.
"""

# === Helper Functions ===

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color using Breadth-First Search (BFS).
    Calculates size and distance threshold for each object.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        tuple: A tuple containing:
            - dict: Maps object_id to {'coords': set(), 'length': int, 'threshold': int}.
            - dict: Maps each pixel (row, col) of the specified color to its object ID.
            - list: A list of all pixel coordinates (r, c) of the specified color.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    object_details = {}
    pixel_to_object_map = {}
    all_color_pixels = []
    object_id_counter = 0

    for r in range(height):
        for c in range(width):
            # Add pixel to list if it's the target color
            if grid[r, c] == color:
                all_color_pixels.append((r, c))
                # Start BFS if we find an unvisited pixel of the target color
                if not visited[r, c]:
                    current_object_coords = set()
                    q = deque([(r, c)])
                    visited[r, c] = True
                    obj_id = object_id_counter

                    while q:
                        row, col = q.popleft()
                        current_object_coords.add((row, col))
                        pixel_to_object_map[(row, col)] = obj_id # Map pixel to this object ID

                        # Check 4 cardinal neighbors
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            # Check bounds and if the neighbor is the correct color and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                    # Store details if object is valid
                    if current_object_coords:
                        length = len(current_object_coords)
                        threshold_D = (length - 1) // 2
                        object_details[obj_id] = {
                            'coords': current_object_coords,
                            'length': length,
                            'threshold': threshold_D
                        }
                        object_id_counter += 1

    return object_details, pixel_to_object_map, all_color_pixels

# === Main Transformation Function ===

def transform(input_grid):
    """
    Applies the transformation rule to the input grid. Fills areas around red
    objects with azure based on Manhattan distance, constrained by a threshold
    derived from the size of the nearest red object.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    red_color = 2
    azure_color = 8

    # 1. Find red objects, their properties, and pixel-to-object mapping
    object_details, pixel_to_object_map, red_pixels = find_objects(input_np, red_color)

    # If there are no red pixels, return the original grid
    if not red_pixels:
        return input_grid

    # 3. Initialize BFS structures: distance grid and object ID grid
    # distance grid stores min distance to any red pixel
    dist_grid = np.full_like(input_np, fill_value=float('inf'), dtype=float)
    # object ID grid stores the ID of the object that is closest
    obj_id_grid = np.full_like(input_np, fill_value=-1, dtype=int)
    queue = deque()

    # 4. Initialize BFS queue and grids using all red pixels as starting points
    for r_red, c_red in red_pixels:
        obj_id = pixel_to_object_map[(r_red, c_red)]
        dist_grid[r_red, c_red] = 0
        obj_id_grid[r_red, c_red] = obj_id
        # Add the pixel coordinate and its corresponding object ID to the queue
        queue.append(((r_red, c_red), obj_id))

    # 5. Perform multi-source BFS to calculate minimum distances and closest object IDs
    while queue:
        (r, c), current_obj_id = queue.popleft() # Get pixel and the ID of the object it belongs to (or was reached from)
        current_dist = dist_grid[r, c]

        # Explore neighbors (4-connectivity for Manhattan distance)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                new_dist = current_dist + 1
                # If this path offers a shorter distance to the neighbor than previously found
                if new_dist < dist_grid[nr, nc]:
                    dist_grid[nr, nc] = new_dist
                    # Record the object ID associated with this shortest path
                    obj_id_grid[nr, nc] = current_obj_id
                    # Add the neighbor to the queue for further exploration
                    queue.append(((nr, nc), current_obj_id))
                # Note: No complex tie-breaking needed based on examples. First path found with min distance determines the object ID.

    # 6. Iterate through the grid to color pixels based on BFS results
    for r in range(height):
        for c in range(width):
            # Consider only non-red pixels that were reached by the BFS
            if input_np[r, c] != red_color and obj_id_grid[r, c] != -1:
                # Get the minimum distance and the ID of the closest object
                dist = dist_grid[r, c]
                obj_id = obj_id_grid[r, c]
                # Retrieve the distance threshold D for that specific object
                threshold_D = object_details[obj_id]['threshold']

                # 7. Apply the coloring rule: color azure if distance is within threshold
                # dist > 0 condition prevents coloring the original red pixels
                if 0 < dist <= threshold_D:
                    output_np[r, c] = azure_color

    # 8. Return the modified grid as a list of lists
    return output_np.tolist()