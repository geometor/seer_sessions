```python
import numpy as np
from collections import deque

"""
Identifies all distinct contiguous groups of non-white pixels (objects) in the 
input grid using 4-way adjacency (horizontal/vertical neighbors only). 
Selects the object containing the largest number of pixels. Calculates the 
minimum bounding box that encloses this largest object. Returns a new grid 
corresponding to the portion of the input grid defined by this bounding box. 
If multiple objects share the largest size, the behavior is implicitly defined 
by the first one encountered during the scan, though the examples suggest a 
unique largest object. If no non-white pixels exist, returns a 1x1 white grid.
"""

def _find_connected_component(grid, start_row, start_col, visited):
    """
    Helper function: Finds a single connected component of non-white pixels 
    starting from a given point using Breadth-First Search (BFS).

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
    # Check if the starting point is valid (within bounds, not visited, not background)
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] == 0: # 0 represents the background color (white)
        return None

    component_coords = []
    q = deque([(start_row, start_col)])
    visited[start_row, start_col] = True # Mark starting pixel as visited

    while q:
        r, c = q.popleft()
        component_coords.append((r, c))

        # Check neighbors (up, down, left, right) for 4-way adjacency
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                 # Check if neighbor is non-white and hasn't been visited yet
                if not visited[nr, nc] and grid[nr, nc] != 0:
                    visited[nr, nc] = True # Mark neighbor as visited
                    q.append((nr, nc)) # Add neighbor to the queue for exploration

    return component_coords

def _find_all_objects(grid):
    """
    Helper function: Finds all distinct contiguous non-white objects in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is itself a list of (row, col) tuples
              representing the coordinates of pixels belonging to an object. 
              Returns an empty list if no non-white pixels are found.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool) # Keep track of visited pixels
    all_objects = []

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is non-white and hasn't been visited, start a search
            # for the connected component (object) it belongs to.
            if grid[r, c] != 0 and not visited[r, c]:
                component = _find_connected_component(grid, r, c, visited)
                # If a valid component is found, add its coordinates to the list
                if component: 
                    all_objects.append(component)
                    
    return all_objects

def _get_bounding_box(coords):
    """
    Helper function: Calculates the minimum bounding box coordinates for a set 
    of pixel coordinates.

    Args:
        coords (list): A list of (row, col) tuples representing an object's pixels.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) defining the bounding box.
               Returns None if the input list is empty.
    """
    if not coords:
        return None
        
    # Determine the minimum and maximum row and column indices from the coordinates
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Extracts the largest contiguous non-white object (by pixel count) 
    from the input grid and returns it within its minimal bounding box.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The extracted subgrid containing the largest object.
                       Returns a 1x1 white grid [[0]] if no non-white objects 
                       are found in the input.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Step 1: Find all distinct contiguous non-white objects in the grid.
    all_objects = _find_all_objects(grid_np)

    # Handle the edge case where the input grid contains no non-white pixels.
    if not all_objects:
        return [[0]] # Return a 1x1 grid containing only the background color.

    # Step 2 & 3: Identify the object with the largest number of pixels.
    # The size of an object is the number of coordinates in its list.
    largest_object_coords = max(all_objects, key=len)

    # Step 4: Determine the minimum bounding box for this largest object.
    bounding_box = _get_bounding_box(largest_object_coords)
    
    # Added robustness check, though should not be triggered if all_objects is not empty.
    if bounding_box is None: 
        return [[0]] 
        
    min_r, max_r, min_c, max_c = bounding_box

    # Step 5 & 6: Extract the subgrid defined by the bounding box using NumPy slicing.
    # Note: NumPy slice upper bounds are exclusive, so add 1 to max indices.
    output_grid_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert the resulting NumPy array back to the required list of lists format.
    output_grid = output_grid_np.tolist()

    return output_grid
```