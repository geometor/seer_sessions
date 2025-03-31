"""
Transforms the input grid by finding the largest contiguous non-white object,
identifying all cells enclosed by it (cells not part of the object that cannot
reach the grid boundary without crossing the object), and filling those enclosed
cells with the color of the largest object. Other cells remain unchanged.
"""

import numpy as np
from collections import deque

# Helper function to find contiguous objects
def find_contiguous_objects(grid, ignore_color=0):
    """
    Finds all contiguous objects of the same color in a grid, ignoring a specified color.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color value to ignore (usually background).

    Returns:
        list: A list of tuples, where each tuple represents an object and contains
              (color, set_of_coordinates). Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is not the ignored color and hasn't been visited
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                # BFS to find all connected cells of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, visited status, and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found object to the list
                if obj_coords:
                    objects.append((int(color), obj_coords)) # Store color as int
                    
    return objects

# Helper function to find the largest object by pixel count
def find_largest_object(objects):
    """
    Finds the object with the most pixels from a list of objects.

    Args:
        objects (list): A list of objects, where each object is (color, set_of_coordinates).

    Returns:
        tuple: The largest object (color, set_of_coordinates), or None if the list is empty.
              Returns the first object encountered in case of a size tie.
    """
    if not objects:
        return None
    
    # Find the object with the maximum number of coordinates in its set
    # Note: max() is stable, so if sizes are equal, the first one encountered wins.
    largest_obj = max(objects, key=lambda obj: len(obj[1]))
    return largest_obj

# Helper function to find cells reachable from the boundary without crossing a barrier
def find_externally_reachable(grid_shape, barrier_coords):
    """
    Finds all cells not part of the barrier that can be reached from the grid edges
    using Breadth-First Search (BFS).

    Args:
        grid_shape (tuple): The (rows, cols) dimensions of the grid.
        barrier_coords (set): A set of (row, col) coordinates representing the barrier object.

    Returns:
        set: A set of (row, col) coordinates representing cells reachable from the outside.
    """
    rows, cols = grid_shape
    reachable = set()
    q = deque()
    
    # Initialize queue with all non-barrier cells on the grid edges
    for r in range(rows):
        # Left edge
        if (r, 0) not in barrier_coords and (r, 0) not in reachable:
            q.append((r, 0))
            reachable.add((r, 0))
        # Right edge
        if (r, cols - 1) not in barrier_coords and (r, cols - 1) not in reachable:
            q.append((r, cols - 1))
            reachable.add((r, cols - 1))
                
    for c in range(cols):
        # Top edge
        if (0, c) not in barrier_coords and (0, c) not in reachable:
            q.append((0, c))
            reachable.add((0, c))
        # Bottom edge
        if (rows - 1, c) not in barrier_coords and (rows - 1, c) not in reachable:
            q.append((rows - 1, c))
            reachable.add((rows - 1, c))

    # Perform BFS to find all reachable non-barrier cells
    while q:
        r, c = q.popleft()
        
        # Explore neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds, if it's not a barrier, and if not already found reachable
            if 0 <= nr < rows and 0 <= nc < cols and \
               (nr, nc) not in barrier_coords and (nr, nc) not in reachable:
                reachable.add((nr, nc))
                q.append((nr, nc))
                
    return reachable


def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    # Convert input to numpy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # 1. Find all contiguous non-white objects
    objects = find_contiguous_objects(input_grid_np, ignore_color=0)
    
    # If no non-white objects exist, return the original grid
    if not objects:
        return input_grid_np.tolist()
        
    # 2. Find the largest object (barrier)
    largest_object = find_largest_object(objects)
    # This check should ideally not be needed if objects is not empty, but it's safe.
    if largest_object is None: 
         return input_grid_np.tolist()

    largest_object_color, largest_object_coords = largest_object
    
    # 3. Identify all externally reachable cells (not part of the largest object)
    externally_reachable_coords = find_externally_reachable(input_grid_np.shape, largest_object_coords)

    # 4. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    # 5. Iterate through all cells and fill the enclosed ones
    for r in range(rows):
        for c in range(cols):
            coord = (r, c)
            # A cell is enclosed if it's NOT part of the largest object
            # AND it's NOT externally reachable.
            if coord not in largest_object_coords and coord not in externally_reachable_coords:
                output_grid[r, c] = largest_object_color
                
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()