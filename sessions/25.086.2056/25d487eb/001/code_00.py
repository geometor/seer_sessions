import numpy as np
from collections import deque

"""
Identifies the largest contiguous non-background object (container) and a single pixel of a different color (source) within it.
Calculates the shortest distance from the source pixel to the boundary of the container object in the four cardinal directions (up, down, left, right).
Determines the direction opposite to this shortest distance (projection direction).
Extends the source pixel's color along the projection direction, starting from the pixel adjacent to the source, until the boundary of the container object is reached.
The output grid reflects this color projection within the container, leaving everything else unchanged.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents an object and contains
              (color, set_of_coordinates). Excludes background (color 0).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                if color == 0: # Skip background
                    visited[r,c] = True
                    continue
                
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append((color, obj_coords))
                    
    return objects

def get_largest_object(objects):
    """
    Finds the largest object (most pixels) from a list of objects.

    Args:
        objects (list): A list of (color, set_of_coordinates) tuples.

    Returns:
        tuple or None: The (color, set_of_coordinates) of the largest object, 
                       or None if the list is empty.
    """
    if not objects:
        return None
    
    largest_obj = max(objects, key=lambda item: len(item[1]))
    return largest_obj


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # 1. Find all non-background objects
    objects = find_objects(grid)
    if not objects:
        return output_grid.tolist() # Return copy if no objects found

    # 2. Identify the largest object (container)
    container = get_largest_object(objects)
    if not container:
         return output_grid.tolist() # Should not happen if objects is not empty, but good practice
        
    container_color, container_coords = container

    # 3. Find the source pixel within the container
    source_pixel = None
    source_count = 0
    for r, c in container_coords:
        pixel_color = grid[r, c]
        if pixel_color != container_color:
            # Check if it's already identified as part of another smaller object within the container
            is_part_of_other_obj = False
            for obj_color, obj_coords in objects:
                 if (r,c) in obj_coords and obj_color != container_color:
                      is_part_of_other_obj = True
                      break
            # If it's not part of another *found* object, it could be the source.
            # This handles cases where the source pixel itself is a 1-pixel object.
            # It also handles cases where the source pixel is just different but not forming a separate object found by find_objects (if connectivity changes).
            # Let's simplify: Assume the source is just any pixel within the container coords that isn't the container color.
            if grid[r,c] != container_color:
                 source_pixel = ((r, c), grid[r,c])
                 source_count += 1


    # 4. Check if exactly one source pixel was found
    if source_count != 1 or source_pixel is None:
        return output_grid.tolist() # Return copy if 0 or >1 source pixels

    source_pos, source_color = source_pixel
    source_r, source_c = source_pos

    # 5. Calculate distances to the boundary within the container
    distances = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

    # Calculate UP distance
    for r in range(source_r - 1, -2, -1):
        if r < 0 or (r, source_c) not in container_coords:
            break
        distances['up'] += 1
        
    # Calculate DOWN distance
    for r in range(source_r + 1, height + 1):
         if r >= height or (r, source_c) not in container_coords:
            break
         distances['down'] += 1

    # Calculate LEFT distance
    for c in range(source_c - 1, -2, -1):
        if c < 0 or (source_r, c) not in container_coords:
            break
        distances['left'] += 1
        
    # Calculate RIGHT distance
    for c in range(source_c + 1, width + 1):
         if c >= width or (source_r, c) not in container_coords:
            break
         distances['right'] += 1

    # 6. Find the minimum distance direction
    # Handle potential ties - arbitrarily pick the first one encountered (e.g., up, down, left, right order)
    min_dist = float('inf')
    min_dir = None
    for direction in ['up', 'down', 'left', 'right']:
        if distances[direction] < min_dist:
            min_dist = distances[direction]
            min_dir = direction

    if min_dir is None:
         return output_grid.tolist() # Should not happen if source is inside container

    # 7. Determine the projection direction (opposite to min_dir)
    opposite_dirs = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    projection_dir = opposite_dirs[min_dir]

    # 8. Project the color along the projection direction
    dr, dc = 0, 0
    if projection_dir == 'up': dr = -1
    elif projection_dir == 'down': dr = 1
    elif projection_dir == 'left': dc = -1
    elif projection_dir == 'right': dc = 1

    curr_r, curr_c = source_r + dr, source_c + dc # Start from the neighbor
    while 0 <= curr_r < height and 0 <= curr_c < width:
        # Check if the current pixel is *part of the container*
        if (curr_r, curr_c) in container_coords:
            output_grid[curr_r, curr_c] = source_color
            curr_r += dr
            curr_c += dc
        else:
            # Stop if we hit the boundary (a non-container pixel) or go out of bounds
            break

    # Convert the result back to a list of lists
    return output_grid.tolist()