```python
import numpy as np
from collections import deque

"""
Identifies shapes and colors of objects enclosed within gray (5) frames ("template objects").
Finds all blue (1) objects located entirely outside any gray frames.
If an outside blue object's shape exactly matches the shape of a template object, 
the blue object's color is changed to the color of the matching template object in the output grid.
Other objects, gray frames, and the background remain unchanged.
"""

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def _find_connected_components(grid, target_colors, mask=None):
    """
    Finds all connected components (objects) of specified colors.
    Uses BFS. Optionally respects a mask (only considers True cells in the mask).
    Returns a list of objects, where each object is a tuple: 
    (color, set_of_coordinates).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel has the target color, hasn't been visited,
            # and is allowed by the mask (if mask exists)
            if (grid[r, c] in target_colors and 
                    not visited[r, c] and 
                    (mask is None or mask[r, c])):
                
                obj_color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (8-directional, assuming objects connect diagonally)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            if (_is_valid(nr, nc, rows, cols) and
                                    not visited[nr, nc] and
                                    grid[nr, nc] == obj_color and
                                    (mask is None or mask[nr, nc])):
                                
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                if obj_coords:
                    objects.append((obj_color, obj_coords))
                    
    return objects

def _get_normalized_shape(coords):
    """
    Normalizes the coordinates of an object relative to its top-left corner.
    Returns a frozenset of relative coordinates for hashability.
    """
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)

def _find_outside_pixels(grid):
    """
    Uses BFS starting from the border to find all pixels reachable 
    without crossing a gray (5) pixel. These are considered "outside".
    Returns a boolean mask where True means the pixel is outside.
    """
    rows, cols = grid.shape
    is_outside = np.zeros((rows, cols), dtype=bool)
    q = deque()
    
    # Add border cells to queue if they are not gray
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] != 5 and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))
    # Avoid double-adding corners
    for c in range(1, cols - 1):
        for r in [0, rows - 1]:
             if grid[r, c] != 5 and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))

    # BFS
    while q:
        r, c = q.popleft()
        
        # Check neighbors (4-directional is sufficient for flood fill)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if _is_valid(nr, nc, rows, cols) and \
               grid[nr, nc] != 5 and \
               not is_outside[nr, nc]:
                is_outside[nr, nc] = True
                q.append((nr, nc))
                
    return is_outside

def transform(input_grid):
    """
    Transforms the input grid by finding template objects inside gray frames,
    finding blue objects outside the frames, and changing the color of outside
    blue objects that match the shape of a template object to that template's color.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Determine which pixels are "outside" the gray frames
    is_outside_mask = _find_outside_pixels(input_grid)
    
    # 2. Determine which pixels are "inside" (not outside and not gray)
    # We are interested in non-white pixels inside.
    is_inside_mask = ~is_outside_mask & (input_grid != 5) & (input_grid != 0)
    
    # 3. Find all template objects (connected components inside frames)
    # Colors can be anything except white(0) and gray(5)
    template_colors = set(range(1, 10)) - {5} 
    template_objects = _find_connected_components(input_grid, template_colors, mask=is_inside_mask)

    # Store template shapes and their corresponding colors
    template_shapes = {} # {normalized_shape: color}
    for color, coords in template_objects:
        shape = _get_normalized_shape(coords)
        if shape: # Avoid empty shapes
             # If multiple templates have the same shape but different colors,
             # the last one encountered will be used. This seems consistent
             # with examples where only one color dictates the change.
             # If a specific rule is needed (e.g., most frequent), adjust here.
            template_shapes[shape] = color

    # If no templates found, no changes needed
    if not template_shapes:
        return output_grid

    # 4. Find all blue objects
    blue_objects = _find_connected_components(input_grid, {1}) # Find only blue objects

    # 5. Iterate through blue objects, check if outside, compare shape, and transform
    for _, blue_coords in blue_objects:
        # Check if the entire object is outside
        is_entirely_outside = all(is_outside_mask[r, c] for r, c in blue_coords)
        
        if is_entirely_outside:
            # Get the normalized shape of the blue object
            blue_shape = _get_normalized_shape(blue_coords)
            
            # Check if this shape matches any template shape
            if blue_shape in template_shapes:
                target_color = template_shapes[blue_shape]
                # Change the color of this blue object in the output grid
                for r, c in blue_coords:
                    output_grid[r, c] = target_color

    return output_grid
```