import numpy as np
from collections import deque

"""
Identify all distinct contiguous areas (objects) formed by connected non-white pixels (values 1-9), 
considering horizontal and vertical adjacency. Calculate the size (pixel count) of each object. 
Select the object with the largest size. Determine the bounding box (min/max row and column indices) 
of this largest object. Extract the subgrid from the input corresponding to this bounding box and 
return it as the output.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not visited yet, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if the neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_pixels:
                    objects.append(current_object_pixels)
    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a list of pixel coordinates.

    Args:
        pixels (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col)
    """
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Transforms the input grid by extracting the largest contiguous non-white object.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the cropped output grid containing the largest object.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Find all non-white objects
    objects = find_objects(input_np)

    # Handle case where there are no non-white objects
    if not objects:
        # Return an empty grid or the original grid based on interpretation?
        # The examples suggest there's always an object to find.
        # Returning an empty grid might be safer if this case is possible.
         return [[]] # Or potentially return input_grid? Let's assume extraction is always possible based on examples.

    # Find the largest object based on pixel count
    largest_object = max(objects, key=len)

    # Determine the bounding box of the largest object
    min_r, max_r, min_c, max_c = get_bounding_box(largest_object)

    # Crop the input grid using the bounding box coordinates
    # Slicing is [start_row:end_row+1, start_col:end_col+1]
    output_np = input_np[min_r:max_r+1, min_c:max_c+1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid