import numpy as np
from collections import deque

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return set(zip(rows, cols))

def find_contiguous_objects(grid, color):
    """
    Finds all contiguous objects of a given color in the grid.
    Uses Breadth-First Search (BFS) for 4-connectivity.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If the pixel is the target color and not yet visited
            if grid[r, c] == color and not visited[r, c]:
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # If neighbor is same color and not visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                current_object.add((nr, nc))
                
                if current_object:
                    objects.append(current_object)
                    
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the locations of blue pixels (1) and red pixels (2).
    
    1. Identifies rows (R) and columns (C) containing at least one blue pixel (1).
    2. Finds all contiguous objects of red pixels (2).
    3. Initializes the output grid as a copy of the input.
    4. For each red object: if any of its pixels fall into an affected row (R) or column (C),
       the entire red object is changed to blue (1) in the output.
    5. For each pixel location (r, c): if its column (c) is an affected column (C) and
       the input pixel was white (0), the output pixel is changed to blue (1).
    """
    # Convert input to numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # 1. Find affected rows (R) and columns (C) from blue pixels (1)
    blue_pixels_coords = find_pixels_by_color(input_array, 1)
    affected_rows = set(r for r, c in blue_pixels_coords)
    affected_cols = set(c for r, c in blue_pixels_coords)

    # 2. Find all contiguous red (2) objects
    red_objects = find_contiguous_objects(input_array, 2)

    # 4. Process red objects
    for red_object in red_objects:
        intersects_affected_zone = False
        for r_obj, c_obj in red_object:
            if r_obj in affected_rows or c_obj in affected_cols:
                intersects_affected_zone = True
                break # No need to check further pixels in this object
        
        # If the object intersects the affected zone, change all its pixels to blue (1)
        if intersects_affected_zone:
            for r_obj, c_obj in red_object:
                output_array[r_obj, c_obj] = 1

    # 5. Process white (0) pixels in affected columns
    for r in range(height):
        for c in range(width):
            # Check if the column is affected AND the original pixel was white (0)
            if c in affected_cols and input_array[r, c] == 0:
                # Note: We only modify output_array here. If a red object was turned 
                # blue in step 4, this step won't overwrite it back to 0. If the
                # pixel was originally blue (1) or red (2) that wasn't changed in step 4,
                # this condition (input_array[r,c] == 0) prevents changing it.
                output_array[r, c] = 1
                
    # Convert the result back to a list of lists
    return output_array.tolist()