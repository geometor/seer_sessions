import numpy as np
from collections import deque

"""
Identify all distinct contiguous non-background (white, 0) objects in the input grid.
Select the object whose lowest point (maximum row index) is the greatest among all objects.
Extract the minimal bounding box around the selected object.
Return a new grid containing only the selected object's pixels within its bounding box, 
filling the rest of the bounding box with the background color.
"""

def find_objects(grid, background_color=0):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to a single object. Returns an empty list
              if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                obj_coords = set()
                obj_color = grid[r,c] # Keep track of the object's color
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    # Check if the current pixel matches the object's color
                    # This handles cases where adjacent non-background pixels are different colors
                    if grid[row, col] == obj_color:
                        obj_coords.add((row, col))
                        # Explore neighbors (4-connectivity)
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == obj_color and not visited[nr, nc]: # Check for same color neighbor
                                visited[nr, nc] = True
                                q.append((nr, nc))
                    # If the pixel is non-background but not the current object's color, mark visited but don't add to coords or queue
                    elif grid[r, c] != background_color:
                         visited[r, c] = True


                if obj_coords: # Only add if we actually found pixels of the starting color
                     # Store the object color along with coordinates
                     objects.append({'coords': obj_coords, 'color': obj_color})

    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the minimum bounding box for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    return min(rows), max(rows), min(cols), max(cols)

def get_lowest_point(obj_coords):
    """
    Finds the maximum row index for an object.

    Args:
        obj_coords (set): A set of (row, col) tuples.

    Returns:
        int: The maximum row index, or -1 if coords is empty.
    """
    if not obj_coords:
        return -1
    return max(r for r, c in obj_coords)


def transform(input_grid):
    """
    Transforms the input grid by selecting the lowest object and extracting its bounding box.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the output grid.
    """
    grid = np.array(input_grid, dtype=int)
    background_color = 0

    # 1. Identify all distinct contiguous objects
    objects = find_objects(grid, background_color)

    if not objects:
        # Handle cases with no non-background objects (return empty or 1x1 background)
        # Based on examples, it seems if only one object exists, it's selected.
        # If no object exists, maybe return 1x1 background? Let's return empty for now.
         # ARC usually expects *some* output. A 1x1 background grid is safer.
        return [[0]]


    # 2. Find the lowest point (max row index) for each object
    lowest_points = [(obj_idx, get_lowest_point(obj['coords'])) for obj_idx, obj in enumerate(objects)]

    # 3. Select the object with the highest maximum row index
    if not lowest_points: # Should not happen if objects list is not empty, but safety check
         return [[0]]
    selected_obj_idx = max(lowest_points, key=lambda item: item[1])[0]
    selected_object_data = objects[selected_obj_idx]
    selected_object_coords = selected_object_data['coords']

    # 4. Determine the minimal bounding box coordinates for the selected object
    min_row, max_row, min_col, max_col = get_bounding_box(selected_object_coords)

    # 5. Create a new output grid with dimensions equal to the bounding box
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = np.full((height, width), background_color, dtype=int)

    # 6. Copy the pixels belonging to the selected object into the output grid
    for r, c in selected_object_coords:
        # Adjust coordinates relative to the bounding box top-left corner
        output_r = r - min_row
        output_c = c - min_col
        output_grid[output_r, output_c] = grid[r, c] # Use original color from input grid

    return output_grid.tolist()