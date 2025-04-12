```python
"""
Transforms the input grid by applying symmetry operations to specific objects.

The core transformation identifies objects composed of exactly two colors: red (2)
and one other color (C). It then determines the geometric shape formed by the
red pixels within that object.

1.  If the red pixels form a single point (P), the C-colored pixels of that
    object are reflected through point symmetry around P.
2.  If the red pixels form a continuous straight horizontal line (L), the
    C-colored pixels are reflected across line L.
3.  If the red pixels form a continuous straight vertical line (L), the
    C-colored pixels are reflected across line L.

Reflected pixels are added to the output grid only if their target location
contains the background color. Objects that do not contain red, contain only
red, or contain red and more than one other color are left unchanged. The
background color also remains unchanged. Cases where red pixels form a more
complex shape or where C pixels are already symmetric relative to the red line
might not be fully handled by this initial implementation based on observed
dominant patterns.
"""

import numpy as np
from collections import Counter

def get_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assumed to be the background."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def find_objects(grid: np.ndarray, background_color: int) -> list[dict]:
    """
    Finds connected components (objects) of non-background colors using BFS.
    Uses 8-way connectivity (includes diagonals).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start BFS for a new object
                q = [(r, c)]
                visited[r, c] = True
                current_object_coords = set()
                current_object_colors = set()
                
                while q:
                    row, col = q.pop(0)
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])
                    
                    # Explore 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds and if valid pixel for object
                            if 0 <= nr < height and 0 <= nc < width and \
                               not visited[nr, nc] and grid[nr, nc] != background_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                objects.append({
                    'coords': current_object_coords,
                    'colors': current_object_colors
                })
    return objects

def is_straight_line(coords: set[tuple[int, int]]) -> tuple[str, int] | tuple[None, None]:
    """Checks if coords form a straight horizontal or vertical line of length >= 1."""
    if not coords:
        return None, None
        
    rows = {r for r, c in coords}
    cols = {c for r, c in coords}

    if len(rows) == 1:
        # Potentially horizontal
        min_c, max_c = min(cols), max(cols)
        # Check continuity
        if len(cols) == max_c - min_c + 1 and len(coords) == len(cols):
             # Check all points are on the line
             line_row = list(rows)[0]
             expected_coords = {(line_row, c) for c in range(min_c, max_c + 1)}
             if coords == expected_coords:
                 return "horizontal", line_row
                 
    if len(cols) == 1:
        # Potentially vertical
        min_r, max_r = min(rows), max(rows)
        # Check continuity
        if len(rows) == max_r - min_r + 1 and len(coords) == len(rows):
            # Check all points are on the line
            line_col = list(cols)[0]
            expected_coords = {(r, line_col) for r in range(min_r, max_r + 1)}
            if coords == expected_coords:
                return "vertical", line_col

    return None, None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the symmetry transformation."""
    
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Determine background color
    background_color = get_background_color(input_np)

    # Find all distinct objects
    objects = find_objects(input_np, background_color)

    # Process objects that contain red (2) and exactly one other color
    for obj in objects:
        colors = obj['colors']
        coords = obj['coords']

        if len(colors) == 2 and 2 in colors:
            other_color = list(colors - {2})[0]
            
            # Separate coordinates by color
            red_coords = {coord for coord in coords if input_np[coord] == 2}
            c_coords = {coord for coord in coords if input_np[coord] == other_color}

            # Case 1: Single red pixel - Point Symmetry
            if len(red_coords) == 1:
                center_r, center_c = list(red_coords)[0]
                for r, c in c_coords:
                    reflected_r = 2 * center_r - r
                    reflected_c = 2 * center_c - c
                    
                    # Add reflected pixel if within bounds and on background
                    if 0 <= reflected_r < height and 0 <= reflected_c < width and \
                       output_np[reflected_r, reflected_c] == background_color:
                        output_np[reflected_r, reflected_c] = other_color

            # Case 2 & 3: Red pixels form a straight line - Line Symmetry
            else:
                line_type, line_coord = is_straight_line(red_coords)
                
                if line_type == "horizontal":
                    line_row = line_coord
                    for r, c in c_coords:
                        reflected_r = 2 * line_row - r
                        reflected_c = c
                        # Add reflected pixel if within bounds and on background
                        if 0 <= reflected_r < height and 0 <= reflected_c < width and \
                           output_np[reflected_r, reflected_c] == background_color:
                            output_np[reflected_r, reflected_c] = other_color
                            
                elif line_type == "vertical":
                    line_col = line_coord
                    for r, c in c_coords:
                        reflected_r = r
                        reflected_c = 2 * line_col - c
                        # Add reflected pixel if within bounds and on background
                        if 0 <= reflected_r < height and 0 <= reflected_c < width and \
                           output_np[reflected_r, reflected_c] == background_color:
                            output_np[reflected_r, reflected_c] = other_color
                
                # Else: Red pixels form a complex shape or other configuration.
                # Based on the analysis, the simple rules cover most cases.
                # The more complex cases (like T1 Yellow/Red, T1 Azure/Red)
                # are not explicitly handled by this core logic yet.
                # If needed, additional rules could be added here.
                # For now, we do nothing for these complex/unhandled cases.


    return output_np.tolist()
```