import numpy as np
import math
from collections import deque

"""
1.  Identify the horizontal blue line that separates the grid into an upper and lower section.
2.  Copy the input grid to create the output grid. The upper section and the blue line itself will remain unchanged.
3.  Identify all distinct, connected, non-white objects in the upper section (above the blue line). For each object, record its color, its shape (relative coordinates of its pixels from its top-left corner), its absolute pixel coordinates, and the coordinates of its top-left corner. These are the 'key' objects.
4.  Identify all distinct, connected, gray objects in the lower section (below the blue line). For each object, record its absolute pixel coordinates and the coordinates of its top-left corner. These are the 'target' objects.
5.  For each target object:
    a.  Calculate the minimum Euclidean distance from any pixel of the target object to any pixel of *every* key object identified in step 3.
    b.  Select the key object that has the overall minimum distance to the target object.
    c.  If two or more key objects are equidistant (have the same minimum distance), select the key object whose top-left corner has the smallest row index. If there is still a tie, select the one among the tied objects whose top-left corner has the smallest column index.
    d.  In the output grid, set all pixels originally belonging to the current target object to white (0).
    e.  Using the top-left corner of the *original* target object as an anchor point, draw the shape of the selected key object (from step 5c) onto the output grid using the selected key object's color. Ensure drawing stays within grid bounds.
6.  Return the modified output grid.
"""

def find_separator_row(grid):
    """Finds the row index of the first horizontal blue line."""
    rows, _ = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == 1): # Blue color is 1
            return r
    return -1 # Return -1 if no separator is found

def get_objects_bfs(grid, start_row, end_row, condition_func, get_color_shape=False):
    """
    Finds connected components within a specified row range using BFS based on a condition.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row (inclusive) for object search.
        end_row (int): The ending row (exclusive) for object search.
        condition_func (callable): A function that takes a pixel value and returns True 
                                   if the pixel should be part of an object.
        get_color_shape (bool): If True, extracts the object's color and relative shape.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'pixels' (set of (r, c) tuples),
              'bbox' (tuple: min_r, min_c, max_r, max_c),
              'top_left' (tuple: min_r, min_c),
              'color' (int, optional),
              'shape' (set of relative (dr, dc) tuples, optional).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(start_row, end_row):
        for c in range(cols):
            # Check condition, bounds, and if already visited
            if not visited[r, c] and condition_func(grid[r, c]):
                
                color = grid[r, c] # Store the color of the starting pixel
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = row + dr, col + dc

                            # Check bounds, visited status, condition, and SAME COLOR
                            if start_row <= nr < end_row and 0 <= nc < cols and \
                               not visited[nr, nc] and \
                               condition_func(grid[nr, nc]) and \
                               grid[nr, nc] == color: # Ensure connectivity is based on same color
                                
                                visited[nr, nc] = True
                                q.append((nr, nc))

                obj_info = {
                    "pixels": obj_pixels,
                    "bbox": (min_r, min_c, max_r, max_c),
                    "top_left": (min_r, min_c)
                }

                if get_color_shape:
                   obj_info["color"] = color
                   # Calculate relative shape based on the top-left of the bounding box
                   shape = set((pr - min_r, pc - min_c) for pr, pc in obj_pixels)
                   obj_info["shape"] = shape

                objects.append(obj_info)
                
    return objects

def calculate_min_distance(obj1_pixels, obj2_pixels):
    """Calculates the minimum Euclidean distance between any pair of pixels from two objects."""
    min_dist_sq = float('inf')
    # If either object is empty, return infinity
    if not obj1_pixels or not obj2_pixels:
        return float('inf')
        
    for r1, c1 in obj1_pixels:
        for r2, c2 in obj2_pixels:
            dist_sq = (r1 - r2)**2 + (c1 - c2)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                # Optimization: if distance is 0, can't get smaller
                if min_dist_sq == 0:
                    return 0.0 
                    
    return math.sqrt(min_dist_sq)

def draw_shape(grid, top_left, shape, color):
    """Draws a shape onto the grid at the specified anchor point."""
    rows, cols = grid.shape
    anchor_r, anchor_c = top_left
    for dr, dc in shape:
        r, c = anchor_r + dr, anchor_c + dc
        # Check if the pixel is within the grid boundaries
        if 0 <= r < rows and 0 <= c < cols:
            grid[r, c] = color


def transform(input_grid):
    """
    Transforms the input grid by replacing gray shapes below a blue separator 
    with the shape and color of the geometrically closest non-white object 
    from above the separator.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Find the horizontal blue separator line.
    separator_row = find_separator_row(output_grid)
    if separator_row == -1:
        # If no separator found, return the original grid (or handle as error)
        return output_grid 

    # 3. Identify 'key' objects (non-white) above the separator.
    key_objects = get_objects_bfs(
        grid=output_grid, 
        start_row=0, 
        end_row=separator_row, 
        condition_func=lambda x: x != 0, # Non-white
        get_color_shape=True
    )

    # 4. Identify 'target' objects (gray) below the separator.
    target_objects = get_objects_bfs(
        grid=output_grid, 
        start_row=separator_row + 1, 
        end_row=rows, 
        condition_func=lambda x: x == 5, # Gray color is 5
        get_color_shape=False
    )

    # If there are no key objects, no transformation can occur below the line.
    if not key_objects:
        return output_grid

    # 5. Process each target object.
    for target_obj in target_objects:
        min_distance = float('inf')
        closest_key = None

        # 5a. Calculate distances to all key objects.
        for key_obj in key_objects:
            distance = calculate_min_distance(target_obj["pixels"], key_obj["pixels"])
            
            update_closest = False
            # 5b. Select the key object with the minimum distance.
            if distance < min_distance:
                update_closest = True
            # 5c. Apply tie-breaking rules.
            elif distance == min_distance:
                 # Compare top-left row index first
                 if key_obj["top_left"][0] < closest_key["top_left"][0]:
                     update_closest = True
                 # If rows are equal, compare top-left column index
                 elif key_obj["top_left"][0] == closest_key["top_left"][0] and \
                      key_obj["top_left"][1] < closest_key["top_left"][1]:
                     update_closest = True

            if update_closest:
                min_distance = distance
                closest_key = key_obj

        # Ensure a closest key was found (should always happen if key_objects is not empty)
        if closest_key:
            # 5d. Clear the original target object pixels in the output grid.
            for r, c in target_obj["pixels"]:
                 # Boundary check (though pixels should be within bounds by definition)
                if 0 <= r < rows and 0 <= c < cols: 
                   output_grid[r, c] = 0 # Set to background color (white)

            # 5e. Draw the closest key's shape at the target's anchor point.
            draw_shape(
                grid=output_grid, 
                top_left=target_obj["top_left"], # Anchor using target's top-left
                shape=closest_key["shape"], 
                color=closest_key["color"]
            )

    # 6. Return the modified output grid.
    return output_grid