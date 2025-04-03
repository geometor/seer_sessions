```python
"""
Identifies all contiguous objects for each non-background color in the input grid. 
For each color, retains only the object(s) with the largest area (pixel count), 
changing all pixels belonging to smaller objects of that same color to the 
background color (0). Contiguity is defined by cardinal adjacency (up, down, left, right).
"""

import numpy as np
from collections import deque

def _find_objects_of_color(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid using BFS.

    Args:
        grid (np.array): The 2D input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of one object. Returns an empty
                   list if no objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects_coords = [] # Stores lists of coordinates for each found object

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell has the target color and hasn't been visited yet,
            # start a BFS to find the connected object.
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_coords.add((r, c))

                # Perform BFS
                while q:
                    row, col = q.popleft() # Current pixel being processed

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc # Neighbor coordinates

                        # Check if the neighbor is within grid boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                # Correctly add the *neighbor's* coordinates
                                current_object_coords.add((nr, nc)) 

                # Add the found object's coordinates to the list if it's not empty
                if current_object_coords:
                    objects_coords.append(current_object_coords)
                    
    return objects_coords

def transform(input_grid):
    """
    Filters the input grid to keep only the largest object for each non-background color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    # initialize output_grid with the same shape as input, filled with background color 0
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find all unique non-background colors present in the input grid
    unique_colors = np.unique(input_grid)
    non_background_colors = unique_colors[unique_colors != 0]

    # Create a set to store the coordinates of all pixels belonging to the largest objects
    pixels_to_keep = set()

    # Process each non-background color individually
    for color in non_background_colors:
        # Find all contiguous objects of the current color
        objects = _find_objects_of_color(input_grid, color)

        # If no objects of this color were found, skip to the next color
        if not objects:
            continue

        # Determine the maximum size (number of pixels) among all objects of this color
        max_size = 0
        for obj_coords in objects:
            max_size = max(max_size, len(obj_coords))

        # Identify all objects that have this maximum size and add their pixels to the keep set
        # This handles potential ties for the largest size.
        for obj_coords in objects:
            if len(obj_coords) == max_size:
                pixels_to_keep.update(obj_coords) 

    # Construct the output grid by copying pixels from the input grid
    # only if their coordinates are in the set of pixels to keep.
    for r, c in pixels_to_keep:
        # Check bounds just in case (though BFS should ensure they are valid)
        if 0 <= r < rows and 0 <= c < cols:
            # Assign the original color from the input grid to the output grid
            output_grid[r, c] = input_grid[r, c]

    return output_grid
```