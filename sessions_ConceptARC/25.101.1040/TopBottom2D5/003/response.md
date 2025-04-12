```python
import numpy as np
from collections import deque

"""
Transformation Rule: Select the Lowest Object

1. Identify all distinct, contiguous objects of non-background color (0) in the input grid.
2. For each object, determine its topmost row (the minimum row index among its pixels).
3. Find the maximum 'topmost row' value among all objects. This identifies the lowest starting position.
4. Select the object(s) that start at this lowest position.
5. If multiple objects start at the same lowest row, select the one that was identified last during a standard top-down, left-to-right scan (this corresponds to the object with the highest assigned ID in the `_find_objects` function).
6. Create an output grid of the same dimensions as the input, filled with the background color (0).
7. Draw the selected object onto the output grid, preserving its original color and position.
8. If no objects are found in the input, return the empty grid.
"""

def _get_neighbors(r, c, height, width):
    """ Helper to get valid cardinal neighbors of a cell """
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Cardinal neighbors only
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid: np.ndarray) -> list[dict]:
    """ 
    Finds all contiguous objects of non-background color (0).
    Assigns a sequential ID based on discovery order (top-down, left-right).
    Returns a list of object dictionaries, each containing 'id', 'color', 'pixels', and 'top_row'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    obj_id_counter = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start of a new object
                obj_id = obj_id_counter
                obj_id_counter += 1
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r = r # Initialize min_r with the starting row

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row) # Update the topmost row found so far for this object

                    # Explore neighbors
                    for nr, nc in _get_neighbors(row, col, height, width):
                        if not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store object information
                objects.append({
                    'id': obj_id,
                    'color': color, 
                    'pixels': obj_pixels, 
                    'top_row': min_r,
                })
    
    return objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Selects and returns the object from the input grid that starts lowest vertically.
    If there's a tie for the lowest starting position, selects the object encountered last 
    during a top-down, left-right scan.
    """
    # Convert input to NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # Find all distinct objects in the grid
    objects = _find_objects(input_np)
    
    # If no objects found, return the empty grid
    if not objects:
        return output_grid.tolist()

    # Find the maximum top_row value (lowest starting position)
    max_top_row = -1
    for obj in objects:
        if obj['top_row'] > max_top_row:
            max_top_row = obj['top_row']

    # Filter objects to keep only those starting at the lowest position
    lowest_objects = [obj for obj in objects if obj['top_row'] == max_top_row]

    # Select the final object
    # If multiple objects are tied for the lowest position, 
    # select the one with the highest ID (discovered last)
    selected_object = None
    if lowest_objects:
        lowest_objects.sort(key=lambda x: x['id'], reverse=True) # Sort by ID descending
        selected_object = lowest_objects[0]

    # Draw the selected object onto the output grid
    if selected_object:
        color = selected_object['color']
        for r, c in selected_object['pixels']:
            # Basic bounds check (should be unnecessary if find_objects is correct)
            if 0 <= r < height and 0 <= c < width: 
                 output_grid[r, c] = color

    # Convert the NumPy output grid back to a list of lists
    return output_grid.tolist()
```