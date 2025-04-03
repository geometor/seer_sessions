```python
import numpy as np
from collections import deque

"""
Identify the background color (consistently white, 0).
Find all distinct contiguous groups (objects) formed by non-background pixels using 4-connectivity.
Calculate the size (number of pixels) for each distinct object.
Identify the object with the largest size. Assume a unique largest object based on examples.
Create a new output grid of the same dimensions as the input, filled with the background color.
Place the pixels belonging to the identified largest object onto the output grid, preserving their original color.
Return the modified output grid.
"""

def find_objects(grid, target_color, visited):
    """
    Finds all contiguous objects of a specific color using BFS.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.
        visited (np.array): A boolean grid tracking visited pixels.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If this pixel is the target color and hasn't been visited yet
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.append((curr_r, curr_c))

                    # Check 4 neighbours (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbour is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbour is the target color and not visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if current_object_coords:
                    objects.append(current_object_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous object
    of any non-background color and removing all other pixels of that same color.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    # Assume background color is 0
    background_color = 0
    
    # Find unique non-background colors
    unique_colors = np.unique(grid_np)
    foreground_colors = [color for color in unique_colors if color != background_color]
    
    # Initialize variables to track the largest object found so far
    max_size = -1
    largest_object_coords = None
    largest_object_color = -1
    
    # Keep track of visited cells across all color searches to avoid redundant BFS starts
    visited = np.zeros_like(grid_np, dtype=bool)

    # Find all objects for each foreground color and identify the largest overall
    for color in foreground_colors:
        objects = find_objects(grid_np, color, visited)
        for obj_coords in objects:
            if len(obj_coords) > max_size:
                max_size = len(obj_coords)
                largest_object_coords = obj_coords
                largest_object_color = color

    # Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # If a largest object was found, place it on the output grid
    if largest_object_coords is not None:
        for r, c in largest_object_coords:
            output_grid[r, c] = largest_object_color
            
    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
```