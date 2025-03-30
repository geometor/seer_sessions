import numpy as np

"""
Identifies connected components of yellow (4) pixels in the input grid. 
For each yellow component:
1. Determines its bounding box.
2. Finds the unique non-yellow, non-white color pixel located within that bounding box in the input grid. This is the 'fill_color'.
3. Calculates an expanded bounding box by extending the original one pixel outwards in all directions (including diagonals).
4. Colors all pixels within this expanded bounding box that were originally white (0) in the input grid with the 'fill_color'. The original yellow shape and its internal colored pixels remain unchanged.
"""

def find_objects(grid, color):
    """Finds all connected objects of a given color in the grid."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) for a new object
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check boundaries and if neighbor has the target color and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if obj_coords:
                    objects.append(list(obj_coords)) # Store as list of tuples
    return objects

def get_bounding_box(object_coords):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of coordinates."""
    if not object_coords:
        return None
    rows = [r for r, c in object_coords]
    cols = [c for r, c in object_coords]
    return min(rows), min(cols), max(rows), max(cols)

def find_internal_color(grid, bounding_box):
    """Finds the first non-background (0), non-yellow (4) color within a bounding box."""
    min_r, min_c, max_r, max_c = bounding_box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            color = grid[r, c]
            if color != 0 and color != 4:
                return color
    return None # Should not happen based on examples

def transform(input_grid):
    """
    Applies the transformation rule: finds yellow objects, determines their internal 
    color, and draws a frame of that color around each object.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all yellow objects
    yellow_objects = find_objects(input_grid, 4)

    # 2. Process each yellow object
    for obj_coords in yellow_objects:
        if not obj_coords:
            continue
            
        # 2a. Get bounding box
        bbox = get_bounding_box(obj_coords)
        if bbox is None:
            continue
        min_r, min_c, max_r, max_c = bbox

        # 2b. Find the internal fill color within the bounding box
        fill_color = find_internal_color(input_grid, bbox)
        if fill_color is None:
            # If no internal color found (unexpected), skip this object
            continue

        # 2c. Calculate expanded bounding box coordinates, clamped to grid boundaries
        exp_min_r = max(0, min_r - 1)
        exp_min_c = max(0, min_c - 1)
        exp_max_r = min(rows - 1, max_r + 1)
        exp_max_c = min(cols - 1, max_c + 1)

        # 2d. Iterate through the expanded bounding box
        for r in range(exp_min_r, exp_max_r + 1):
            for c in range(exp_min_c, exp_max_c + 1):
                # 2e. If the cell in the *input* grid is white (0), color it in the *output* grid
                if input_grid[r, c] == 0:
                    output_grid[r, c] = fill_color

    return output_grid