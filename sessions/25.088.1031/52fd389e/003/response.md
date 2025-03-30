```python
import numpy as np

"""
Identifies connected components of yellow (4) pixels in the input grid. 
For each yellow component:
1. Determines its bounding box.
2. Finds the unique non-yellow, non-white color pixel located within that bounding box in the input grid. This is the 'frame_color'.
3. Calculates an expanded bounding box by extending the original one pixel outwards in all directions (including diagonals).
4. Colors the pixels lying on the *perimeter* of this expanded bounding box with the 'frame_color', overwriting any existing color in the output grid. The interior of the frame (including the original yellow shape and its internal colored pixels) remains unchanged from the input, unless overwritten by a frame pixel.
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
            # Check if the color is neither white (0) nor yellow (4)
            if color != 0 and color != 4:
                return color
    # Fallback if no such color is found (should not happen based on examples)
    return None 

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all distinct yellow objects (connected components)
    yellow_objects = find_objects(input_grid, 4)

    # 2. Process each yellow object found
    for obj_coords in yellow_objects:
        if not obj_coords:
            continue
            
        # 2a. Determine the bounding box of the current yellow object
        bbox = get_bounding_box(obj_coords)
        if bbox is None:
            continue
        min_r, min_c, max_r, max_c = bbox

        # 2b. Find the 'frame color' associated with this object
        # Search within the bounding box in the input grid for a non-white, non-yellow pixel
        frame_color = find_internal_color(input_grid, bbox)
        if frame_color is None:
            # If no internal color found (unexpected based on examples), skip this object
            continue

        # 2c. Calculate the coordinates of the expanded bounding box (frame boundaries)
        # Extend by one pixel outwards, clamping to grid boundaries
        exp_min_r = max(0, min_r - 1)
        exp_min_c = max(0, min_c - 1)
        exp_max_r = min(rows - 1, max_r + 1)
        exp_max_c = min(cols - 1, max_c + 1)

        # 2d. Iterate through all cells within the expanded bounding box
        for r in range(exp_min_r, exp_max_r + 1):
            for c in range(exp_min_c, exp_max_c + 1):
                # 2e. Check if the current cell (r, c) lies on the perimeter of the expanded box
                is_perimeter = (r == exp_min_r or r == exp_max_r or
                                c == exp_min_c or c == exp_max_c)

                # 2f. If it's on the perimeter, update the output grid pixel with the frame color
                if is_perimeter:
                    output_grid[r, c] = frame_color

    # 3. Return the final modified grid
    return output_grid
```