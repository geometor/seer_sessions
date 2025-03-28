import numpy as np
from collections import deque

"""
Recolor azure (8) objects based on the parity of their size (pixel count).

1. Create a copy of the input grid to serve as the output grid.
2. Identify all distinct contiguous objects composed solely of azure (8) pixels 
   within the input grid using 4-way adjacency (horizontal/vertical).
3. For each identified azure object:
    a. Calculate its size (number of pixels).
    b. Determine the parity of the size (Even or Odd).
    c. If the size is Even, recolor all pixels of the object to Red (2) in the 
       output grid.
    d. If the size is Odd, recolor all pixels of the object to Blue (1) in the 
       output grid.
4. Pixels not part of any azure object remain unchanged.
5. Return the modified output grid.
"""

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
    Transforms the input grid by recoloring azure objects based on the parity of their size.

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
        
    # Process each identified azure object
    for obj_coords in azure_objects:
        # Calculate the size (pixel count) of the current object
        object_size = len(obj_coords)
        
        # Determine the output color based on the parity of the object size
        # Rule: Even size -> Red(2), Odd size -> Blue(1)
        if object_size % 2 == 0: # Even parity
            output_color = red_color 
        else: # Odd parity
            output_color = blue_color
                
        # Recolor the pixels of the current object in the output grid
        for r, c in obj_coords:
            output_grid[r, c] = output_color
            
    # Return the final transformed grid
    return output_grid