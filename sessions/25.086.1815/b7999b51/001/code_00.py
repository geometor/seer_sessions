"""
Identifies all distinct contiguous non-white objects in the input grid (using 8-way connectivity).
For each object, calculates its color and height (span of rows).
Sorts the objects based on their height in descending order.
Creates an output grid where:
  - The height is the maximum height found among all objects.
  - The width is the total number of objects found.
  - Each column corresponds to a sorted object.
  - The j-th column is filled from the top with the j-th object's color for a number of rows equal to its height.
  - The remaining cells in the column are filled with the background color (white, 0).
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color' (int): The color of the object.
              'min_row' (int): The minimum row index occupied by the object.
              'max_row' (int): The maximum row index occupied by the object.
              'height' (int): The calculated height of the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8-way connectivity neighbors (row_offset, col_offset)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1),          ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not yet visited, start BFS for a new object
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                min_r, max_r = r, r
                
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_pixels = set([(r, c)])

                while q:
                    curr_r, curr_c = q.popleft()
                    
                    # Update min/max row for the object
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)

                    # Check neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            current_object_pixels.add((nr, nc))
                
                # Calculate height and store object info
                height = max_r - min_r + 1
                objects.append({
                    'color': color,
                    'min_row': min_r,
                    'max_row': max_r,
                    'height': height
                })
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on identified object properties.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1. Find all non-white objects and their properties
    objects = find_objects(np.array(input_grid))

    # Handle edge case: no objects found
    if not objects:
        # Return a 1x1 white grid or based on specific requirements if any
        return np.zeros((1, 1), dtype=int) 

    # 2. Sort objects by height in descending order
    # Using a stable sort, relative order of equal height objects is maintained
    sorted_objects = sorted(objects, key=lambda obj: obj['height'], reverse=True)

    # 3. Determine output grid dimensions
    max_height = 0
    if sorted_objects: # Ensure there is at least one object before accessing
        max_height = sorted_objects[0]['height'] 
    num_objects = len(sorted_objects)

    # 4. Initialize output grid with background color (0)
    output_grid = np.zeros((max_height, num_objects), dtype=int)

    # 5. Populate output grid column by column based on sorted objects
    for j, obj in enumerate(sorted_objects):
        color = obj['color']
        height = obj['height']
        # Fill the top 'height' cells of column 'j' with the object's color
        output_grid[:height, j] = color
        # The rest of the column remains 0 (background) due to initialization

    return output_grid.tolist() # Return as list of lists per requirement
