import numpy as np
from collections import deque
from typing import Set, Tuple

"""
Recolor distinct red(2) objects based on scanning order.
The object containing the first red pixel encountered during a top-to-bottom, 
left-to-right scan is recolored to maroon(9). All other distinct red objects 
are recolored to orange(7). White(0) pixels remain unchanged. 
Contiguity for objects is defined by 8-way adjacency (including diagonals).
"""

def _find_object_bfs(grid: np.ndarray, start_r: int, start_c: int, visited: np.ndarray) -> Set[Tuple[int, int]]:
    """
    Finds all connected pixels of the same color as the starting pixel
    using Breadth-First Search (BFS) with 8-way adjacency. Marks visited
    pixels in the `visited` array.

    Args:
        grid (np.ndarray): The input grid.
        start_r (int): The starting row index.
        start_c (int): The starting column index.
        visited (np.ndarray): A boolean grid of the same shape as grid,
                              marking visited pixels. Modified in place.

    Returns:
        set: A set of tuples (row, col) representing the coordinates of
             all pixels belonging to the connected object. Returns an empty
             set if the starting pixel is invalid or already visited.
    """
    height, width = grid.shape
    
    # Basic validation and check if already visited
    if not (0 <= start_r < height and 0 <= start_c < width) or visited[start_r, start_c]:
       return set() 

    target_color = grid[start_r, start_c]
    object_coords = set()
    
    # Define 8 directions for adjacency (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Use a deque for BFS queue
    queue = deque([(start_r, start_c)])

    # Mark the starting pixel as visited and add to the object
    visited[start_r, start_c] = True
    object_coords.add((start_r, start_c))

    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is the target color and not visited
                if grid[nr, nc] == target_color and not visited[nr, nc]:
                    visited[nr, nc] = True # Mark as visited
                    object_coords.add((nr, nc)) # Add to current object
                    queue.append((nr, nc)) # Add to queue for exploration

    return object_coords


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by recoloring red(2) objects based on scan order.
    The first encountered red object (top-to-bottom, left-to-right) is colored 
    maroon(9), others are colored orange(7). White(0) pixels are unchanged.

    Args:
        input_grid (np.ndarray): The 2D input grid containing integers 0-9.

    Returns:
        np.ndarray: The transformed 2D output grid.
    """
    # Initialize output grid as a copy of the input to preserve non-red pixels
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Keep track of visited pixels to avoid processing parts of the same object multiple times
    visited = np.zeros((height, width), dtype=bool)

    # Store coordinates of the first object and others separately
    first_object_coords = set()
    other_objects_coords = set()
    first_object_found = False

    # Iterate through the grid, top-to-bottom, left-to-right
    for r in range(height):
        for c in range(width):
            # If we find a red pixel (color 2) that hasn't been visited yet
            if input_grid[r, c] == 2 and not visited[r, c]:
                
                # Find all connected red pixels belonging to this object using BFS
                # The BFS also marks the found pixels as visited.
                current_object_coords = _find_object_bfs(input_grid, r, c, visited)

                # If this is the very first red object we've identified in the scan
                if not first_object_found:
                    # Store its coordinates and set the flag
                    first_object_coords = current_object_coords
                    first_object_found = True
                # Otherwise, this is a subsequent red object
                else:
                    # Add its coordinates to the set of 'other' objects
                    other_objects_coords.update(current_object_coords)
                
                # Note: _find_object_bfs modifies 'visited' in place.

    # After scanning the entire grid and identifying all objects:
    # Recolor the pixels based on which object set they belong to.
    
    # Color the first object maroon (9)
    for r_obj, c_obj in first_object_coords:
        if 0 <= r_obj < height and 0 <= c_obj < width: # Bounds check for safety
            output_grid[r_obj, c_obj] = 9

    # Color all other objects orange (7)
    for r_obj, c_obj in other_objects_coords:
         if 0 <= r_obj < height and 0 <= c_obj < width: # Bounds check for safety
            output_grid[r_obj, c_obj] = 7

    # White (0) pixels (and any other colors) were preserved by the initial copy
    return output_grid