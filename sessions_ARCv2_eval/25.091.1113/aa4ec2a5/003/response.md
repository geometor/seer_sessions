```python
import numpy as np
from collections import deque

"""
This transformation rule processes a grid containing a background color (yellow, 4) and one or more shapes made of blue pixels (1).

The rule performs the following steps:
1. Identify all separate, contiguous regions (shapes) of blue (1) pixels using 4-connectivity.
2. Identify all yellow (4) background pixels reachable from the grid's outer border using a 4-connectivity flood fill ('exterior_yellow').
3. Identify all yellow (4) pixels not reachable from the border ('hole_pixels').
4. For each blue shape, determine if it encloses any holes by checking if any of its adjacent pixels (8-connectivity) is a 'hole_pixel'.
5. For each blue shape, identify the 'exterior_yellow' pixels adjacent (8-connectivity) to it; these form the potential border.
6. Create the output grid:
    a. Initialize with the background color (yellow, 4).
    b. Fill all 'hole_pixels' with magenta (6).
    c. Fill the pixels corresponding to blue shapes: use azure (8) if the shape encloses holes, otherwise use blue (1).
    d. Fill the identified border pixels with red (2).
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """Gets valid neighbor coordinates based on specified connectivity (4 or 8)."""
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals for 4-connectivity
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid, target_color, connectivity=4):
    """Finds all connected components of a specific color using specified connectivity."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))

                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=connectivity):
                        if grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_coords:
                    components.append(component_coords)

    return components

def find_exterior_pixels(grid, background_color, connectivity=4):
    """Finds all background pixels reachable from the border using specified connectivity."""
    height, width = grid.shape
    exterior_pixels = set()
    q = deque()
    visited_flood = np.zeros_like(grid, dtype=bool)

    # Add border background pixels to the queue if they match the background color
    for r in range(height):
        for c in [0, width - 1]:
            if grid[r, c] == background_color and not visited_flood[r,c]:
                q.append((r, c))
                visited_flood[r,c] = True
                exterior_pixels.add((r, c))
    for c in range(width): # Use range(width) instead of range(1, width - 1) to include corners
        for r in [0, height - 1]:
             if grid[r, c] == background_color and not visited_flood[r,c]:
                q.append((r, c))
                visited_flood[r,c] = True
                exterior_pixels.add((r, c))

    # Flood fill from the border using specified connectivity
    while q:
        curr_r, curr_c = q.popleft()
        for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=connectivity):
            if grid[nr, nc] == background_color and not visited_flood[nr, nc]:
                visited_flood[nr, nc] = True
                exterior_pixels.add((nr, nc))
                q.append((nr, nc))

    return exterior_pixels


def transform(input_grid):
    """
    Transforms the input grid by bordering blue shapes and filling based on holes.
    - Shapes enclosing holes become azure (8), holes become magenta (6).
    - Shapes without holes remain blue (1).
    - Borders on the exterior side become red (2).
    - Background remains yellow (4).
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Define colors
    background_color = 4
    shape_color = 1
    border_color = 2
    hole_fill_color = 6
    shape_with_hole_color = 8

    # 1. Find all blue shapes (using 4-connectivity for shape definition)
    blue_shapes = find_connected_components(input_np, shape_color, connectivity=4)

    if not blue_shapes: # No blue shapes, return original grid
        return input_np.tolist()

    # 2. Find all exterior yellow pixels (using 4-connectivity for background reachability)
    exterior_yellow = find_exterior_pixels(input_np, background_color, connectivity=4)

    # 3. Identify all hole pixels (yellow pixels not reachable from outside)
    all_hole_pixels = set()
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == background_color and (r, c) not in exterior_yellow:
                all_hole_pixels.add((r, c))

    # 4. Determine which shapes have holes and identify border pixels
    shape_has_holes = [False] * len(blue_shapes)
    all_border_pixels = set() # Pixels that are exterior_yellow and adjacent to a shape

    for shape_id, shape_coords in enumerate(blue_shapes):
        current_shape_borders = set()
        shape_touches_hole = False
        for r, c in shape_coords:
            # Check 8 neighbors for holes and potential borders
            for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                neighbor_coord = (nr, nc)
                if input_np[nr, nc] == background_color:
                    if neighbor_coord in exterior_yellow:
                        current_shape_borders.add(neighbor_coord)
                    elif neighbor_coord in all_hole_pixels:
                        # If any part of the shape touches a hole pixel, mark the shape
                        shape_touches_hole = True
        
        shape_has_holes[shape_id] = shape_touches_hole
        all_border_pixels.update(current_shape_borders)

    # 5. Create the output grid, applying colors in order of precedence
    # Initialize with background color
    output_grid = np.full_like(input_np, background_color)

    # Fill holes first
    for hr, hc in all_hole_pixels:
        output_grid[hr, hc] = hole_fill_color

    # Fill shapes based on whether they have holes
    for shape_id, shape_coords in enumerate(blue_shapes):
        fill_color = shape_with_hole_color if shape_has_holes[shape_id] else shape_color
        for r, c in shape_coords:
            output_grid[r, c] = fill_color

    # Fill borders last (only affects original exterior yellow locations)
    for br, bc in all_border_pixels:
         # Check if the target pixel wasn't already filled by a shape or hole.
         # This check might be redundant if logic is correct, but adds safety.
         # The border should only occupy space that was originally exterior yellow.
        if (br, bc) in exterior_yellow:
             output_grid[br, bc] = border_color


    return output_grid.tolist()
```