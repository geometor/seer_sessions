import numpy as np
from collections import deque

"""
Identify all distinct connected objects of non-background (non-0) pixels in the input grid, using 8-way connectivity (including diagonals).
Determine the size (pixel count) of each object.
Select the object with the largest size.
Determine the bounding box (minimum and maximum row and column indices) of the largest object.
Create a new output grid whose dimensions match the height and width of the bounding box.
Initialize the output grid with the background color (0).
Copy the pixels of the largest object from the input grid into the output grid, adjusting their positions relative to the top-left corner of the bounding box.
"""

def find_objects(grid):
    """
    Finds all connected objects of non-background pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'size', and 'bbox' (min_r, max_r, min_c, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8-way connectivity neighbors (relative coordinates)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find an unvisited non-background pixel
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.append((curr_r, curr_c))

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'size': len(obj_pixels),
                    'bbox': (min_r, max_r, min_c, max_c)
                })

    return objects

def transform(input_grid_list):
    """
    Extracts the largest object from the input grid into a new grid 
    corresponding to its bounding box.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the output grid. Returns an empty
              list or a default grid if no objects are found.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    
    # 1. Identify Objects
    objects = find_objects(input_grid)

    # Handle case with no objects found
    if not objects:
        # Returning a 1x1 white grid as a default, adjust if needed
        return [[0]] 

    # 2. Select Largest Object
    largest_object = max(objects, key=lambda obj: obj['size'])

    # 3. Determine Bounding Box
    min_r, max_r, min_c, max_c = largest_object['bbox']

    # 4. Calculate Output Dimensions
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1

    # 5. Create Output Grid (initialized to background color 0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 6. Copy Object pixels to the output grid
    object_color = largest_object['color']
    for r, c in largest_object['pixels']:
        # Calculate position relative to the top-left of the bounding box
        output_r = r - min_r
        output_c = c - min_c
        output_grid[output_r, output_c] = object_color # Use stored color for safety

    # 7. Final Output - convert back to list of lists
    return output_grid.tolist()