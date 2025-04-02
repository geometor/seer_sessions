import numpy as np
import math

"""
Transforms the input grid based on the following steps:
1. Identifies all distinct groups of contiguous, non-white pixels in the input grid using 8-directional connectivity (horizontal, vertical, and diagonal).
2. Determines which object is the "container" (the one with the largest number of pixels) and which is the "content" (the other non-white object). Stores the color and original coordinate(s) of the content object.
3. Calculates the bounding box of the container object (minimum row, maximum row, minimum column, maximum column).
4. Calculates the coordinates (row, column) of the geometric center of the container's bounding box using integer floor division: center_row = (min_row + max_row) // 2, center_col = (min_col + max_col) // 2.
5. Creates a copy of the input grid.
6. Modifies the copied grid:
    a. Changes the pixel(s) at the original location(s) of the content object to the background color (white/0).
    b. Changes the pixel at the calculated center coordinates (center_row, center_col) to the stored color of the content object.
7. Returns the modified grid.
"""

def find_objects_8_connectivity(grid, background_color=0):
    """
    Finds all contiguous objects of the same color in the grid, excluding the 
    background color, using 8-directional connectivity.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color designated as the background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'coords' (list of tuples (row, col)).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Start search if pixel is not background and not visited
            if color != background_color and not visited[r, c]:
                current_object_coords = []
                q = [(r, c)]  # Queue for BFS
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    current_object_coords.append((row, col))
                    
                    # Check 8-directional neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: # Skip self
                                continue
                                
                            nr, nc = row + dr, col + dc
                            # Check bounds, if neighbor has same color, and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                objects.append({'color': color, 'coords': current_object_coords})
    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box (min/max row/col) for a set of coordinates.

    Args:
        coords (list): A list of tuples (row, col).

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid):
    """
    Transforms the input grid by moving a 'content' object to the center 
    of a 'container' object based on 8-connectivity and bounding box center.

    Args:
        input_grid (list of lists): The input grid representation.

    Returns:
        list of lists: The transformed grid representation.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    background_color = 0

    # 1. Identify all distinct non-white objects using 8-connectivity
    objects = find_objects_8_connectivity(input_np, background_color)

    # Ensure exactly two non-background objects are found, as per problem constraints
    if len(objects) != 2:
        # If assumption of 2 objects fails, return the original grid unchanged
        # (this matches behavior if identification fails)
        return input_grid 

    # 2. Determine container and content objects (container is larger by pixel count)
    obj1_size = len(objects[0]['coords'])
    obj2_size = len(objects[1]['coords'])

    if obj1_size > obj2_size:
        container_object = objects[0]
        content_object = objects[1]
    # Handle tie-breaking or equal size if necessary, assume obj1 > obj2 or obj2 > obj1
    elif obj2_size > obj1_size: 
        container_object = objects[1]
        content_object = objects[0]
    else:
         # Undefined behavior if sizes are equal, return original grid as a safe default
         return input_grid

    content_color = content_object['color']
    content_coords = content_object['coords']
    container_coords = container_object['coords']

    # 3. Calculate the bounding box of the container object
    bbox = get_bounding_box(container_coords)
    if bbox is None:
         # Should not happen if container_object is correctly identified
         return input_grid
    min_row, max_row, min_col, max_col = bbox

    # 4. Calculate the geometric center of the container's bounding box using floor division
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    # 5. Modify the output grid (already initialized)
    # 6a. Erase the original content object by setting its pixels to background color
    for r, c in content_coords:
        # Check bounds just in case
         if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = background_color

    # 6b. Place the content object's color at the calculated center
    # Check if center coordinates are within grid bounds
    if 0 <= center_row < output_grid.shape[0] and 0 <= center_col < output_grid.shape[1]:
        output_grid[center_row, center_col] = content_color
    # else: Handle error case? For this task, assume center is always valid.

    # 7. Return the modified grid, converted back to list of lists
    return output_grid.tolist()