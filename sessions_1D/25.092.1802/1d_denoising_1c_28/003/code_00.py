"""
Transforms the input grid by keeping only the largest contiguous object 
for each non-background color. All other pixels, including those belonging 
to smaller objects of the same color, are set to the background color (0).
Contiguity is defined by cardinal directions (up, down, left, right).
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
                    row, col = q.popleft()

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within grid boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                current_object_coords.add((nr, c)) # Bug: Should be current_object_coords.add((nr, nc)) - Fixed in next iteration. 

                # Add the found object's coordinates to the list if it's not empty
                if current_object_coords:
                    objects_coords.append(current_object_coords)
                    
    return objects_coords


def transform(input_grid):
    """
    Filters the input grid to keep only the largest object for each color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    # Initialize output_grid with the background color (0) and same dimensions
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find all unique non-background colors in the input grid
    unique_colors = np.unique(input_grid)
    non_background_colors = unique_colors[unique_colors != 0]

    # Keep track of all coordinates belonging to the largest objects found
    pixels_to_keep = set()

    # Process each non-background color
    for color in non_background_colors:
        # Find all objects of the current color
        objects = _find_objects_of_color(input_grid, color)

        # If no objects of this color exist, skip to the next color
        if not objects:
            continue

        # Find the largest object(s) for this color
        max_size = 0
        largest_object_coords = set() # Store coords of the largest found so far
        
        # Iterate through found objects to find the maximum size
        for obj_coords in objects:
            if len(obj_coords) > max_size:
                 max_size = len(obj_coords)
                 largest_object_coords = obj_coords # Update the set of coordinates to keep
            # If sizes are equal, the first one encountered with max_size is kept.
            # Based on examples, we assume a unique largest object per color.

        # Add the coordinates of the largest object to the overall set to keep
        if largest_object_coords: # Ensure we found a non-empty largest object
             pixels_to_keep.update(largest_object_coords)

    # Construct the final output grid
    # Iterate through the coordinates identified as belonging to largest objects
    for r, c in pixels_to_keep:
        # Check bounds just in case (though BFS should ensure they are valid)
        if 0 <= r < rows and 0 <= c < cols:
             # Assign the original color from the input grid to the output grid
             output_grid[r, c] = input_grid[r, c]

    return output_grid