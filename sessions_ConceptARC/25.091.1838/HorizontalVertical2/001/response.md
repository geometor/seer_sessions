```python
import numpy as np
from collections import deque

"""
Identify two distinct, separated non-white patterns in the input grid. 
One pattern will exhibit horizontal stripes (colors change primarily vertically), 
and the other will exhibit vertical stripes (colors change primarily horizontally).
The transformation rule is to isolate and keep only the pattern with horizontal stripes, 
placing it in its original position on an otherwise white background grid of the same dimensions.
The pattern with vertical stripes and any separating white pixels are discarded.
"""

def _get_neighbors(coord, max_rows, max_cols):
    """Gets valid neighbor coordinates (up, down, left, right)."""
    r, c = coord
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < max_rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < max_cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def _find_objects(grid):
    """Finds connected components of non-white pixels."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not yet visited
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    
                    # Explore neighbors
                    for nr, nc in _get_neighbors((row, col), rows, cols):
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    # Simple filter: Assume the two largest objects are the patterns
    # This helps ignore small noise pixels if any exist.
    if len(objects) > 2:
        objects.sort(key=len, reverse=True)
        return objects[:2]
        
    return objects

def _get_stripe_orientation(grid, object_coords):
    """Determines if an object has horizontal or vertical stripes."""
    if not object_coords:
        return 'unknown'

    horizontal_changes = 0
    vertical_changes = 0

    for r, c in object_coords:
        # Check right neighbor
        right_neighbor = (r, c + 1)
        if right_neighbor in object_coords and grid[r, c] != grid[right_neighbor]:
            horizontal_changes += 1
            
        # Check bottom neighbor
        bottom_neighbor = (r + 1, c)
        if bottom_neighbor in object_coords and grid[r, c] != grid[bottom_neighbor]:
            vertical_changes += 1

    # If colors change more often vertically, the stripes are horizontal.
    if vertical_changes > horizontal_changes:
        return 'horizontal'
    # If colors change more often horizontally, the stripes are vertical.
    elif horizontal_changes > vertical_changes:
        return 'vertical'
    # Handle cases with no changes or equal changes (e.g., solid color blocks)
    # Based on the task examples, we expect clear differentiation.
    # If an object is a single row/column of alternating colors, this logic holds.
    # If it's ambiguous, classify as 'unknown'.
    else: 
         # If it's a single line/solid block, default check.
         # A single row object -> vertical stripes (changes are horizontal)
         # A single col object -> horizontal stripes (changes are vertical)
         rows = {r for r, c in object_coords}
         cols = {c for r, c in object_coords}
         if len(rows) == 1 and len(cols) > 1 and horizontal_changes > 0:
             return 'vertical'
         if len(cols) == 1 and len(rows) > 1 and vertical_changes > 0:
             return 'horizontal'
         # Otherwise, truly ambiguous or uniform color
         return 'unknown' 


def transform(input_grid):
    """
    Transforms the input grid by isolating the pattern with horizontal stripes.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color (white, 0)
    output_grid = np.zeros_like(input_array, dtype=int)

    # Find all non-white connected objects
    objects = _find_objects(input_array)

    # Expecting exactly two main objects based on examples
    if len(objects) != 2:
        # If not exactly two objects found, return empty grid or handle error
        # For this task, the structure seems consistent. Let's find the horizontal one if possible.
        # pass # Re-evaluate if this happens in tests
        pass # Continue to see if one has horizontal stripes
        
    horizontal_stripe_object_coords = None

    # Identify the object with horizontal stripes
    for obj_coords in objects:
        orientation = _get_stripe_orientation(input_array, obj_coords)
        if orientation == 'horizontal':
            # Ensure only one horizontal object is found, otherwise ambiguous
            if horizontal_stripe_object_coords is not None:
                 # Ambiguous case: found more than one horizontal pattern
                 return output_grid.tolist() # Return empty grid
            horizontal_stripe_object_coords = obj_coords

    # If a horizontal stripe object was successfully identified
    if horizontal_stripe_object_coords:
        # Copy the pixels of the selected object to the output grid
        for r, c in horizontal_stripe_object_coords:
            # Check bounds just in case, though coordinates should be valid
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = input_array[r, c]

    # Return the result as a list of lists
    return output_grid.tolist()
```