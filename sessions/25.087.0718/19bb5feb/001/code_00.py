import numpy as np
from collections import deque

"""
Identifies the largest contiguous azure (8) object (container) in the input grid.
Determines the bounding box and center of this container.
Finds all distinct contiguous objects (content) within the input grid composed of colors other than white (0) and azure (8).
For each content object, determines which quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) it primarily occupies relative to the container's center.
Creates a 2x2 output grid, placing the color of each content object into the cell corresponding to its quadrant. Quadrants without a content object remain white (0).
"""

def find_contiguous_objects(grid, target_colors=None, ignore_colors=None):
    """
    Finds all contiguous objects of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        target_colors (set, optional): Set of colors to find objects for. 
                                      If None, finds objects of any color not in ignore_colors.
        ignore_colors (set, optional): Set of colors to ignore. Defaults to {0}.

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, list_of_coordinates).
              Returns an empty list if no objects are found.
    """
    if ignore_colors is None:
        ignore_colors = {0} # Default ignore white background

    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip if visited, ignored color, or not a target color (if specified)
            if visited[r, c] or color in ignore_colors or \
               (target_colors is not None and color not in target_colors):
                continue

            # Start BFS for a new object
            obj_coords = []
            q = deque([(r, c)])
            visited[r, c] = True
            
            while q:
                row, col = q.popleft()
                obj_coords.append((row, col))

                # Check neighbors (4-connectivity: up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    
                    # Check bounds and if neighbor is same color and not visited
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       not visited[nr, nc] and grid[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))
            
            if obj_coords: # Should always be true if we start BFS
                 objects.append((color, obj_coords))

    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a list of coordinates.

    Args:
        coords (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not coords:
        return None
    
    min_row = min(r for r, c in coords)
    max_row = max(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_col = max(c for r, c in coords)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid based on the quadrant location of colored objects
    within the main azure container object.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Find the container object (azure = 8)
    azure_objects = find_contiguous_objects(grid, target_colors={8}, ignore_colors={0})
    
    if not azure_objects:
        # Handle case where no azure container is found (return empty or default grid?)
        # Based on examples, expecting a 2x2 white grid if process fails early.
        return [[0, 0], [0, 0]] 
        
    # Assume the largest azure object is the container
    container_color, container_coords = max(azure_objects, key=lambda obj: len(obj[1]))

    # 2. Determine the bounding box of the container
    bbox = get_bounding_box(container_coords)
    if bbox is None:
        return [[0, 0], [0, 0]] # Should not happen if container found
    min_r, max_r, min_c, max_c = bbox

    # 3. Calculate the center of the container's bounding box
    # Using floating point for center to handle even/odd dimensions
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0

    # 4. Initialize a 2x2 output grid with white (0)
    output_grid = np.zeros((2, 2), dtype=int)

    # 5. Find all content objects (not white 0, not azure 8)
    content_objects = find_contiguous_objects(grid, ignore_colors={0, 8})

    # 6. Process each content object
    for content_color, content_coords in content_objects:
        # a. Determine representative location (use top-left corner of its own bbox)
        content_bbox = get_bounding_box(content_coords)
        if content_bbox is None:
            continue # Skip if object has no coords (shouldn't happen)
        
        obj_r, _, obj_c, _ = content_bbox # Using top-left coord (min_r, min_c)
        
        # b. Determine the quadrant relative to container center
        output_row = 0 if obj_r < center_r else 1
        output_col = 0 if obj_c < center_c else 1
            
        # c. Update the output grid cell
        # Check if the object is actually *inside* the container coords might be useful,
        # but examples imply they always are. Sticking to quadrant logic.
        output_grid[output_row, output_col] = content_color
        
    # 7. Return the final 2x2 output grid as list of lists
    return output_grid.tolist()