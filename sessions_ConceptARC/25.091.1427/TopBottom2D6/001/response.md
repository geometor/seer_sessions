```python
import numpy as np
from collections import deque

"""
1. Identify all distinct objects in the input grid, where an object is a connected 
   group of pixels of the same non-white color (using 4-way adjacency).
2. For each object, find the row index of its topmost pixel(s) (the minimum row index).
3. Select the object whose topmost pixel has the largest row index (i.e., the object 
   positioned lowest in the grid). If there's a tie, select the first one identified 
   during the grid scan (top-to-bottom, left-to-right).
4. Determine the minimal bounding box (top-left and bottom-right coordinates) 
   that perfectly encloses the selected object.
5. Create a new output grid with dimensions equal to the height and width of the 
   bounding box.
6. Copy the pixels from the input grid within the calculated bounding box to the 
   output grid, preserving their relative positions.
"""

def find_objects(grid):
    """
    Finds all distinct connected objects of non-background (0) pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents an object
              and contains (color, set_of_coordinates).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col)
    """
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Selects the object starting lowest in the grid and extracts its bounding box.
    """
    
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all distinct objects
    objects = find_objects(input_np)

    if not objects:
        # Handle case with no objects if necessary, maybe return empty grid or original?
        # Based on examples, there's always at least one object to select.
        # Return an empty grid for now if no object found.
         return np.array([[]], dtype=int).tolist()


    # 2. Find the topmost row for each object
    object_data = []
    for color, coords in objects:
        min_row = min(r for r, c in coords)
        object_data.append({'color': color, 'coords': coords, 'top_row': min_row})

    # 3. Select the object with the maximum 'top_row' (lowest starting object)
    # If there's a tie, the first one encountered in find_objects (top-left scan) wins.
    lowest_object = max(object_data, key=lambda obj: obj['top_row'])

    # 4. Determine the bounding box of the selected object
    selected_coords = lowest_object['coords']
    min_row, min_col, max_row, max_col = get_bounding_box(selected_coords)

    # 5. & 6. Extract the subgrid corresponding to the bounding box
    output_grid_np = input_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```