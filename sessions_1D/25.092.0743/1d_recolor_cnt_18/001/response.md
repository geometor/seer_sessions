```python
import numpy as np
from collections import deque

"""
Recolors contiguous objects composed of azure (8) pixels based on their size.
- Objects of size 1 become orange (7).
- Objects of size 2 become green (3).
- Objects of size 3 become blue (1).
All other pixels, including the white (0) background, remain unchanged.
Contiguity is defined by horizontal and vertical adjacency.
"""

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of
              pixel coordinates [(r1, c1), (r2, c2), ...].
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited yet,
            # start a search (BFS) to find the entire object it belongs to.
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, target color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Add the found object (list of coordinates) to our list of objects
                if current_object_coords:
                    objects.append(current_object_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by recoloring azure (8) objects based on size.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = input_np.copy()

    # Define the target color (azure)
    target_color = 8

    # Find all azure objects in the input grid
    azure_objects = find_objects(input_np, target_color)

    # Define the size-to-color mapping
    size_to_color_map = {
        1: 7,  # orange
        2: 3,  # green
        3: 1   # blue
    }

    # Process each found object
    for obj_coords in azure_objects:
        # Calculate the size of the object
        obj_size = len(obj_coords)

        # Determine the new color based on size, default to original if size not in map
        new_color = size_to_color_map.get(obj_size, target_color) # Defaults to 8 if size unknown

        # Recolor the pixels belonging to this object in the output grid
        for r, c in obj_coords:
            output_grid[r, c] = new_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
```