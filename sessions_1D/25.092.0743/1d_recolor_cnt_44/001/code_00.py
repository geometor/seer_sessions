import numpy as np
from collections import deque

"""
Recolors contiguous red (2) objects based on their size:
- Objects of size 1 become orange (7).
- Objects of size 2 become green (3).
- Objects of size 3 become blue (1).
Other pixels, including the white (0) background, remain unchanged.
Connectivity is defined by horizontal and vertical adjacency (4-connectivity).
"""

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in a grid using BFS.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the cell is the target color and hasn't been visited yet, start a search
            if grid[r, c] == target_color and (r, c) not in visited:
                current_object = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                
                # Add the found object to the list
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by recoloring red objects based on their size.
    """
    input_grid_np = np.array(input_grid)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    input_object_color = 2 # red

    # Define the color mapping based on object size
    color_map = {
        1: 7, # orange
        2: 3, # green
        3: 1  # blue
    }

    # Find all red objects in the input grid
    red_objects = find_objects(input_grid_np, input_object_color)

    # Process each found red object
    for obj in red_objects:
        # Calculate the size of the object
        obj_size = len(obj)

        # Determine the output color based on size, default to original if size not in map
        output_color = color_map.get(obj_size, input_object_color) 

        # Recolor the pixels belonging to this object in the output grid
        for r, c in obj:
            output_grid[r, c] = output_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()