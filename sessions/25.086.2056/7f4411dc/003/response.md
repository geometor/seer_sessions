```python
import numpy as np
from collections import deque

"""
Identifies all separate, connected groups (objects) of the single non-white color 
in the input grid using orthogonal adjacency (up, down, left, right). 
Filters these objects, keeping only those with a size (pixel count) greater than 1. 
For each remaining object, further removes any pixel that has exactly one neighbor 
belonging to the same object, unless the object consists of only two pixels 
(in which case both pixels are kept). 
Creates an output grid containing only the filtered and pruned pixels, 
preserving their original color and position against a white background.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    height, width = grid.shape
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and (r, c) not in visited:
                current_object_coords = []
                queue = deque([(r, c)])
                visited.add((r, c))

                # Start BFS from this pixel
                while queue:
                    curr_r, curr_c = queue.popleft()
                    current_object_coords.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                
                # Add the found object (list of coordinates) to our list of objects
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    return objects

def count_internal_neighbors(coord, object_coords_set):
    """
    Counts how many orthogonal neighbors of a coordinate belong to the same object set.

    Args:
        coord (tuple): The (row, col) of the pixel to check.
        object_coords_set (set): A set of (row, col) tuples representing the object.

    Returns:
        int: The number of neighbors within the object.
    """
    r, c = coord
    count = 0
    # Check neighbors (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        # Check if neighbor is part of the same object set
        if (nr, nc) in object_coords_set:
            count += 1
    return count

def transform(input_grid):
    """
    Filters and prunes objects in the input grid based on size and connectivity.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    height, width = input_grid.shape
    # Initialize output_grid with background color (white=0)
    output_grid = np.zeros_like(input_grid)

    # Find the non-background color used for objects
    object_color = None
    unique_colors = np.unique(input_grid)
    for color in unique_colors:
        if color != 0: # Assuming 0 is always the background
            object_color = color
            break
            
    # If no object color found (grid is all white), return the empty grid
    if object_color is None:
        return output_grid

    # Find all connected objects of that color
    all_objects = find_objects(input_grid, object_color)

    # If no objects are found, return the empty grid
    if not all_objects:
        return output_grid
        
    # --- Step 1: Filter objects by size > 1 ---
    large_objects = [obj for obj in all_objects if len(obj) > 1]

    # --- Step 2: Prune pixels with only one internal neighbor ---
    final_pixels_to_draw = set()
    for obj_coords in large_objects:
        obj_coords_set = set(obj_coords) # Use set for efficient lookups
        obj_size = len(obj_coords_set)
        
        # Handle the special case for 2-pixel objects directly
        if obj_size == 2:
            final_pixels_to_draw.update(obj_coords_set)
            continue # Move to the next object

        # For objects larger than 2 pixels, check each pixel's neighbors
        current_object_pixels_to_keep = set()
        for r, c in obj_coords:
            # Count neighbors that are also part of the current object
            internal_neighbors = count_internal_neighbors((r, c), obj_coords_set)
            
            # Keep the pixel if it has more than one neighbor within the object
            if internal_neighbors > 1:
                 current_object_pixels_to_keep.add((r, c))

        # Add the processed pixels for this object to the final set
        final_pixels_to_draw.update(current_object_pixels_to_keep)

    # --- Step 3: Draw the final pixels onto the output grid ---
    for r, c in final_pixels_to_draw:
        # Ensure coordinates are within bounds (should be, but good practice)
        if 0 <= r < height and 0 <= c < width:
            output_grid[r, c] = object_color
                
    return output_grid
```