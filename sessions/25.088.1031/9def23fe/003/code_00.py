import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1. Identify the largest contiguous object of a single non-white color in the input grid. This is the "pattern object". Note its color (C) and determine its bounding box (min_row, max_row, min_col, max_col).
2. Identify all other non-white pixels in the input grid. These are the "marker pixels". Note their color(s) (M) and their locations (row and column indices).
3. Create a set `R_marker` containing the row indices of all marker pixels.
4. Create a set `C_marker` containing the column indices of all marker pixels.
5. Initialize a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
6. Iterate through all cells `(r, c)` within the bounding box of the pattern object (from `min_row` to `max_row` and `min_col` to `max_col`).
7. If row index `r` is *not* present in the set `R_marker` AND column index `c` is *not* present in the set `C_marker`, set the output grid cell `(r, c)` to the pattern object's color (C). This fills the grid where neither the row nor the column is blocked by a marker.
8. Iterate through all cells `(r, c)` of the input grid. If the input cell `(r, c)` was part of the original pattern object (i.e., had color C), set the corresponding output cell `(r, c)` to color C. This overlays the original pattern shape onto the filled area.
9. Iterate through all cells `(r, c)` of the input grid. If the input cell `(r, c)` was a marker pixel (i.e., had color M), set the corresponding output cell `(r, c)` to color M. This overlays the marker pixels.
"""

def _find_all_objects(grid):
    """
    Finds all contiguous objects (connected components) of the same non-background color.
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of (row, col) tuples).
              Returns an empty list if no non-background objects are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If the cell is non-background and not visited yet, start a search
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Breadth-First Search (BFS) for connected component
                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    
                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, color match, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found object
                if coords:
                    objects.append({'color': color, 'coords': coords})
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the identified pattern and marker objects.
    Fills cells within the pattern object's bounding box with the pattern color,
    if the cell's row AND column are not inhibited by marker pixels.
    Then overlays the original pattern and markers.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # 1 & 2. Identify pattern object and marker pixels/objects
    all_objects = _find_all_objects(grid)
    
    if not all_objects:
        return input_grid # Return original grid if no objects found
        
    # Find the largest object (pattern object)
    pattern_object = max(all_objects, key=lambda obj: len(obj['coords']), default=None)
    
    if pattern_object is None:
         return input_grid # Should not happen if all_objects is not empty, but safety check

    pattern_color = pattern_object['color']
    pattern_coords = pattern_object['coords']
    
    # Identify marker pixels (all non-background pixels not in the pattern object)
    marker_pixels = []
    for r in range(height):
        for c in range(width):
            if grid[r,c] != 0 and (r,c) not in pattern_coords:
                 marker_pixels.append({'r': r, 'c': c, 'color': grid[r,c]})

    # 3 & 4. Determine inhibited rows and columns
    inhibited_rows = set(p['r'] for p in marker_pixels)
    inhibited_cols = set(p['c'] for p in marker_pixels)

    # Determine pattern object bounding box
    if not pattern_coords:
         return input_grid # No pattern object pixels found

    rows, cols = zip(*pattern_coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # 5. Initialize output grid with background color
    output_grid = np.zeros_like(grid, dtype=int)

    # 6 & 7. Fill non-inhibited cells within the bounding box
    # Iterate through each cell within the bounding box
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            # If the row is NOT inhibited AND the column is NOT inhibited
            if r not in inhibited_rows and c not in inhibited_cols:
                # Fill the cell with the pattern color
                output_grid[r, c] = pattern_color

    # 8. Overlay the original pattern object
    # This ensures the original shape is preserved on top of the filled area
    for r, c in pattern_coords:
        output_grid[r, c] = pattern_color

    # 9. Overlay the marker pixels
    # This places the markers back on top of everything else
    for p in marker_pixels:
        output_grid[p['r'], p['c']] = p['color']

    return output_grid.tolist()