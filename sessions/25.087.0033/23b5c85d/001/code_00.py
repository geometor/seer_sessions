import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects composed of non-white (non-0) pixels in the input grid.
For each object, determine its color and bounding box dimensions (height and width).
Calculate the area (height * width) for each object's bounding box.
Find the object that has the minimum calculated bounding box area.
Create a new grid whose height and width match the height and width of the bounding box of the minimum-area object.
Fill the entire new grid with the color of the minimum-area object.
Return the newly created and filled grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels', and 'bbox'. Returns empty list if no objects found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If the cell is not background and hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                bbox = (min_r, min_c, max_r, max_c)
                objects.append({'color': color, 'pixels': obj_pixels, 'bbox': bbox})
                
    return objects

def get_bbox_dims(bbox):
    """Calculates height and width from a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def get_area(bbox):
    """Calculates the area of a bounding box."""
    height, width = get_bbox_dims(bbox)
    return height * width

def transform(input_grid):
    """
    Transforms the input grid by finding the smallest rectangular object (by bounding box area)
    and creating an output grid of its dimensions filled with its color.
    """
    # Find all non-background objects in the input grid
    objects = find_objects(np.array(input_grid))

    # Handle cases with no objects found
    if not objects:
        # Returning a 1x1 white grid as a default, though examples suggest objects always exist.
        return np.array([[0]], dtype=int) 

    # Find the object with the minimum bounding box area
    min_area = float('inf')
    smallest_object = None
    for obj in objects:
        area = get_area(obj['bbox'])
        if area < min_area:
            min_area = area
            smallest_object = obj
        # If areas are equal, the first one encountered is kept (no specific tie-breaking needed based on examples)

    # If somehow smallest_object is still None (shouldn't happen if objects list is not empty)
    if smallest_object is None:
         return np.array([[0]], dtype=int) 

    # Get the dimensions and color of the smallest object
    smallest_bbox = smallest_object['bbox']
    output_color = smallest_object['color']
    output_height, output_width = get_bbox_dims(smallest_bbox)

    # Create the output grid filled with the determined color
    output_grid = np.full((output_height, output_width), output_color, dtype=int)

    return output_grid.tolist() # Return as list of lists per ARC format