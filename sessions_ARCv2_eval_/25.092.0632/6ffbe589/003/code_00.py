import numpy as np
from collections import deque

"""
Identifies all distinct contiguous groups of non-white pixels (objects) in the 
input grid using 4-way adjacency (horizontal/vertical). Selects the object 
with the largest number of pixels. Calculates the minimum bounding box 
enclosing this largest object. Returns a new grid containing the portion of the 
input grid defined by this bounding box.
"""

def _find_connected_component(grid, start_row, start_col, visited):
    """
    Finds a single connected component of non-white pixels using BFS.
    
    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row for the search.
        start_col (int): The starting column for the search.
        visited (np.array): A boolean grid tracking visited pixels.

    Returns:
        list: A list of (row, col) tuples representing the coordinates of the
              pixels in the found component, or None if the start pixel is
              invalid (white or already visited).
    """
    rows, cols = grid.shape
    # Check if the starting point is valid (bounds, visited, non-white)
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] == 0: # 0 is white/background
        return None

    component_coords = []
    q = deque([(start_row, start_col)])
    visited[start_row, start_col] = True # Mark starting pixel as visited

    while q:
        r, c = q.popleft()
        component_coords.append((r, c))

        # Check neighbors (up, down, left, right) using 4-way adjacency
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                 # Check if neighbor is non-white and hasn't been visited yet
                if not visited[nr, nc] and grid[nr, nc] != 0:
                    visited[nr, nc] = True # Mark neighbor as visited
                    q.append((nr, nc)) # Add neighbor to the queue

    return component_coords

def _find_all_objects(grid):
    """
    Finds all distinct contiguous non-white objects in the grid.
    
    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is a list of (row, col) tuples
              representing an object's pixel coordinates. Returns an empty list
              if no non-white pixels are found.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool) # Initialize visited grid
    all_objects = []

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not yet visited, it's the start of a new object
            if grid[r, c] != 0 and not visited[r, c]:
                # Find all connected pixels for this new object
                component = _find_connected_component(grid, r, c, visited)
                if component: # Should always be true if conditions met
                    all_objects.append(component)
                    
    return all_objects

def _get_bounding_box(coords):
    """
    Calculates the minimum bounding box for a set of coordinates.
    
    Args:
        coords (list): A list of (row, col) tuples for an object.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not coords:
        return None
        
    # Find the minimum and maximum row and column indices from the coordinates
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Extracts the largest contiguous non-white object (by pixel count) 
    from the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The extracted subgrid containing the largest object.
                       Returns a 1x1 white grid [[0]] if no non-white objects 
                       are found in the input.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Find all distinct contiguous non-white objects
    all_objects = _find_all_objects(grid_np)

    # Handle the edge case where the input grid has no non-white pixels
    if not all_objects:
        return [[0]] 

    # 2. & 3. Count pixels for each object and select the object with the maximum count
    # The length of the list of coordinates for an object is its pixel count.
    largest_object_coords = max(all_objects, key=len)

    # 4. Determine the minimum bounding box for the largest object
    bounding_box = _get_bounding_box(largest_object_coords)
    
    # This check should ideally not be needed if all_objects wasn't empty, 
    # but added for robustness.
    if bounding_box is None: 
        return [[0]] # Should not happen if largest_object_coords is valid
        
    min_r, max_r, min_c, max_c = bounding_box

    # 5. Create the output grid by extracting the subgrid using slicing
    # Note: NumPy slicing is exclusive of the end index, so add 1 to max values.
    output_grid_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_grid_np.tolist()

    return output_grid