import numpy as np
from collections import deque

"""
For each connected yellow (4) object in the input grid:
1. Find its bounding box.
2. Identify the unique non-white (0), non-yellow (4) 'internal color' pixel(s) contained strictly within that bounding box in the input grid.
3. Count the number of pixels having this 'internal color' within the bounding box. This count determines the 'frame thickness'.
4. Calculate an expanded bounding box by extending the original bounding box outwards by 'frame thickness' pixels in all directions (up, down, left, right), clamped to the grid boundaries.
5. Initialize the output grid as a copy of the input grid.
6. Fill the area *between* the original bounding box and the expanded bounding box in the output grid with the 'internal color'. Specifically, any pixel within the expanded bounding box that is *outside* the original bounding box is colored with the 'internal color', overwriting the existing pixel value. The content inside the original bounding box remains unchanged from the input unless overwritten by the frame.
"""

def find_objects(grid, color):
    """Finds all connected objects of a given color in the grid using 8-way connectivity."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) for a new object
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
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

def find_internal_color_and_count(grid, bounding_box):
    """
    Finds the non-background (0), non-yellow (4) color and counts its occurrences 
    within a bounding box in the input grid. Assumes only one such color type per box.
    """
    min_r, min_c, max_r, max_c = bounding_box
    internal_color = None
    count = 0
    
    # First pass: find the color type
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            color = grid[r, c]
            if color != 0 and color != 4:
                internal_color = color
                break # Found the color type
        if internal_color is not None:
            break

    if internal_color is None:
        return None, 0 # No internal color found

    # Second pass: count occurrences of that specific color
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] == internal_color:
                count += 1
                
    return internal_color, count

def transform(input_grid):
    # 1. Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Find all distinct Yellow Objects in input_grid.
    yellow_objects = find_objects(input_grid, 4)

    # 3. Process each Yellow Object found
    for obj_coords in yellow_objects:
        if not obj_coords:
            continue

        # 3a. Get its bounding_box.
        bbox = get_bounding_box(obj_coords)
        if bbox is None:
            continue
        min_r, min_c, max_r, max_c = bbox

        # 3b. Find its internal_color and internal_count (thickness).
        frame_color, thickness = find_internal_color_and_count(input_grid, bbox)

        # 3c. If internal_color exists and thickness is positive:
        if frame_color is not None and thickness > 0:
            # i. Calculate the expanded_bounding_box.
            exp_min_r = max(0, min_r - thickness)
            exp_min_c = max(0, min_c - thickness)
            exp_max_r = min(rows - 1, max_r + thickness)
            exp_max_c = min(cols - 1, max_c + thickness)

            # ii. Draw the frame: Color pixels in the expanded box BUT outside the original box.
            for r in range(exp_min_r, exp_max_r + 1):
                for c in range(exp_min_c, exp_max_c + 1):
                    # Check if the current pixel (r, c) is outside the original bounding box
                    is_outside_original_box = not (min_r <= r <= max_r and min_c <= c <= max_c)
                    
                    if is_outside_original_box:
                        output_grid[r, c] = frame_color

    # 4. Return the final modified grid.
    return output_grid