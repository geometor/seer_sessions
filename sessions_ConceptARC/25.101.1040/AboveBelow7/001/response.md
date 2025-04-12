```python
import numpy as np
from collections import deque

"""
Identifies the two distinct non-background objects in the input grid.
Determines which object is vertically above the other.
Calculates the vertical gap between them.
Creates an output grid where the original lower object maintains its position,
and the original upper object is moved below the lower object, preserving the original vertical gap.
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds distinct contiguous objects of non-background colors.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, each representing an object with its 
        color, coordinates, and bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-background color and not visited yet
            if color != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'bbox': (min_r, max_r, min_c, max_c) # min_row, max_row, min_col, max_col
                })
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Swaps the vertical positions of two distinct non-background objects 
    where one is directly above the other. The lower object stays in place, 
    and the upper object moves below it, maintaining the original vertical gap.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Find the objects
    objects = find_objects(input_array)

    # Ensure exactly two objects were found
    if len(objects) != 2:
        # Handle error case or unexpected input - returning input for now
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning input.")
        return input_grid

    # Identify upper and lower objects based on min_row
    obj1 = objects[0]
    obj2 = objects[1]
    
    if obj1['bbox'][0] < obj2['bbox'][0]:
        upper_object = obj1
        lower_object = obj2
    else:
        upper_object = obj2
        lower_object = obj1

    # Extract bounding box info
    upper_min_r, upper_max_r, _, _ = upper_object['bbox']
    lower_min_r, lower_max_r, _, _ = lower_object['bbox']
    
    # Calculate the vertical gap between the objects
    # gap = bottom row of upper obj - top row of lower obj - 1
    gap = lower_min_r - upper_max_r - 1
    
    # Place the lower object in the output grid at its original position
    for r, c in lower_object['coords']:
        output_array[r, c] = lower_object['color']
        
    # Determine the new starting row for the upper object
    # It should start below the lower object, maintaining the gap
    # new_upper_top_row = bottom row of lower obj + gap + 1
    new_upper_object_start_row = lower_max_r + gap + 1
    
    # Calculate the vertical shift needed for the upper object
    shift = new_upper_object_start_row - upper_min_r
    
    # Place the upper object in the output grid at its new shifted position
    for r, c in upper_object['coords']:
        new_r = r + shift
        # Check bounds just in case, though logic should prevent out-of-bounds
        if 0 <= new_r < rows:
             output_array[new_r, c] = upper_object['color']
        else:
            print(f"Warning: Calculated new row {new_r} for upper object pixel at ({r},{c}) is out of bounds ({rows}x{cols}).")


    return output_array.tolist()
```