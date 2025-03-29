```python
import numpy as np
from collections import deque

"""
Identify all distinct, contiguous blocks of non-white color in the input grid.
Determine the vertical boundaries (top and bottom rows) and horizontal boundaries (leftmost and rightmost columns) for each block.
Create sorted lists of unique row and column boundaries (using min_row and max_row+1 for rows, min_col and max_col+1 for columns).
These sorted boundaries define intervals. The number of row intervals determines the output height, and column intervals determine the output width.
Construct the output grid.
For each cell (r, c) in the output grid, determine the corresponding spatial region (intersection of the r-th row interval and c-th column interval) in the input grid.
Find the input block that occupies this region and assign its color to the output cell (r, c). If a block spans multiple intervals, its color is assigned to all corresponding output cells.
"""

def _bfs(grid, start_row, start_col, visited):
    """Performs Breadth-First Search to find a connected object."""
    rows, cols = grid.shape
    q = deque([(start_row, start_col)])
    color = grid[start_row, start_col]
    pixels = set()
    min_r, max_r = start_row, start_row
    min_c, max_c = start_col, start_col
    
    while q:
        r, c = q.popleft()
        
        if not (0 <= r < rows and 0 <= c < cols) or visited[r, c] or grid[r, c] != color:
            continue
            
        visited[r, c] = True
        pixels.add((r, c))
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)
        
        # Explore neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc] and grid[nr, nc] == color:
                q.append((nr, nc))
                
    return {
        'color': color,
        'pixels': pixels,
        'min_row': min_r,
        'max_row': max_r,
        'min_col': min_c,
        'max_col': max_c
    }

def _find_objects(grid):
    """Finds all contiguous non-background objects in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-background (not 0) and not visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                obj = _bfs(grid, r, c, visited)
                objects.append(obj)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by summarizing rectangular blocks based on their
    spatial intervals.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Find all non-white objects and their properties
    objects = _find_objects(input_np)

    if not objects:
        # Handle empty input or input with only background
        # Returning an empty grid seems appropriate based on the summarization goal.
        return np.array([[]], dtype=int) 

    # Collect all unique row and column boundaries
    row_boundaries = set()
    col_boundaries = set()
    for obj in objects:
        row_boundaries.add(obj['min_row'])
        row_boundaries.add(obj['max_row'] + 1) # Use end+1 for interval definition
        col_boundaries.add(obj['min_col'])
        col_boundaries.add(obj['max_col'] + 1) # Use end+1 for interval definition

    # Sort boundaries to define intervals
    sorted_rows = sorted(list(row_boundaries))
    sorted_cols = sorted(list(col_boundaries))
    
    # Remove boundaries outside the overall min/max range if necessary
    # (though usually defined by the blocks themselves)
    min_r_overall = min(obj['min_row'] for obj in objects)
    max_r_overall = max(obj['max_row'] for obj in objects)
    min_c_overall = min(obj['min_col'] for obj in objects)
    max_c_overall = max(obj['max_col'] for obj in objects)

    # Filter boundaries to only those within the span of the objects
    # This handles cases where background padding might create unnecessary boundaries
    # But the current logic using min/max+1 naturally handles the relevant span.
    
    # Map absolute coordinates to boundary indices for easier lookup
    row_map = {val: i for i, val in enumerate(sorted_rows)}
    col_map = {val: i for i, val in enumerate(sorted_cols)}

    # Determine output grid size
    output_height = len(sorted_rows) - 1
    output_width = len(sorted_cols) - 1
    
    # Ensure non-negative dimensions
    output_height = max(0, output_height)
    output_width = max(0, output_width)

    # Initialize output grid (e.g., with background color 0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill the output grid based on object locations
    for obj in objects:
        # Find the start and end indices in the output grid for this object
        start_row_idx = row_map[obj['min_row']]
        end_row_idx = row_map[obj['max_row'] + 1] 
        start_col_idx = col_map[obj['min_col']]
        end_col_idx = col_map[obj['max_col'] + 1]

        # Assign the object's color to the corresponding cells in the output grid
        output_grid[start_row_idx:end_row_idx, start_col_idx:end_col_idx] = obj['color']

    return output_grid.tolist() # Return as list of lists per ARC standard
```