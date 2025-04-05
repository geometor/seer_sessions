import numpy as np
from collections import deque

"""
Identify all distinct connected objects of non-zero digits in the input grid. 
For each object, determine its lowest point (maximum row index). 
Select the object(s) whose lowest point is maximal among all objects. 
Create an output grid filled with zeros and copy the pixels of the selected lowest object(s) onto it.
"""

def _find_objects(grid):
    """
    Finds all connected components (objects) of non-zero cells in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'pixels' (list of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not visited yet, start a search (BFS)
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if neighbor has the same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({'color': color, 'pixels': current_object_pixels})
    return objects

def transform(input_grid):
    """
    Identifies the lowest object(s) in the input grid and returns a new grid
    containing only those object(s).

    Args:
        input_grid (list of lists or np.array): The input 10x10 grid.

    Returns:
        np.array: The output 10x10 grid with only the lowest object(s).
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    
    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_grid_np)

    # Find all distinct objects in the input grid
    objects = _find_objects(input_grid_np)

    # If no objects are found, return the empty grid
    if not objects:
        return output_grid.tolist() # Return as list of lists if needed, sticking to np array for now

    # Determine the lowest point for each object
    max_lowest_row = -1
    lowest_objects = []

    for obj in objects:
        current_max_row = -1
        for r, c in obj['pixels']:
            if r > current_max_row:
                current_max_row = r
        
        # Update the overall maximum lowest row and the list of lowest objects
        if current_max_row > max_lowest_row:
            max_lowest_row = current_max_row
            lowest_objects = [obj] # Start a new list with this object
        elif current_max_row == max_lowest_row:
            lowest_objects.append(obj) # Add this object to the list of tied objects

    # Draw the selected lowest object(s) onto the output grid
    for obj in lowest_objects:
        color = obj['color']
        for r, c in obj['pixels']:
            output_grid[r, c] = color
            
    # Return the output grid (convert back to list of lists if required by ARC standard)
    return output_grid.tolist() 