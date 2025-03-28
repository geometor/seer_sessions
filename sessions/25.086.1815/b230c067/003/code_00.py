"""
Recolor azure (8) objects based on the relationship between the parity of the total number of azure pixels and the parity of the size of each individual object.

1. Initialize the output grid as a copy of the input grid.
2. Find all distinct contiguous objects composed of azure (8) pixels in the input grid, considering pixels connected horizontally or vertically (4-way adjacency) as part of the same object.
3. Calculate the `total_azure_pixels` by summing the number of pixels in all identified azure objects.
4. Determine the `total_parity` (Even or Odd) of the `total_azure_pixels`.
5. Iterate through each identified azure object:
    a. Calculate the `object_size` (number of pixels) for the current object.
    b. Determine the `object_parity` (Even or Odd) of the `object_size`.
    c. Compare the `total_parity` and `object_parity`:
        i. If `total_parity` is the SAME as `object_parity`, set the `output_color` for this object to Red (2).
        ii. If `total_parity` is DIFFERENT from `object_parity`, set the `output_color` for this object to Blue (1).
    d. Recolor all pixels belonging to the current azure object in the output grid with the determined `output_color`.
6. Return the modified output grid.
"""

import numpy as np
from collections import deque

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If pixel is the target color and not yet visited, start a search
            if grid[r, c] == color and (r, c) not in visited:
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                # Breadth-First Search (BFS) for connected pixels
                while q:
                    row, col = q.popleft()

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is the same color and unvisited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                # Add the found object's coordinates to the list if it's not empty
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by recoloring azure objects based on parity rules.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Define the target color and output colors
    azure_color = 8
    blue_color = 1
    red_color = 2
    
    # Find all azure (8) objects using 4-way adjacency
    azure_objects = find_objects(input_grid, azure_color)
    
    # If no azure objects are found, return the original grid
    if not azure_objects:
        return output_grid
        
    # Calculate the total number of azure pixels
    total_azure_pixels = sum(len(obj) for obj in azure_objects)
    
    # Determine the parity of the total count (True for odd, False for even)
    total_parity_is_odd = (total_azure_pixels % 2 != 0)
    
    # Process each identified azure object
    for obj_coords in azure_objects:
        # Calculate the size (pixel count) of the current object
        object_pixel_count = len(obj_coords)
        # Determine the parity of the object size (True for odd, False for even)
        object_parity_is_odd = (object_pixel_count % 2 != 0)
        
        # Determine the output color based on comparing total and object parities
        # Rule: Same parity -> Red(2), Different parity -> Blue(1)
        if total_parity_is_odd == object_parity_is_odd:
            output_color = red_color 
        else: 
            output_color = blue_color
                
        # Recolor the pixels of the current object in the output grid
        for r, c in obj_coords:
            output_grid[r, c] = output_color
            
    # Return the final transformed grid
    return output_grid