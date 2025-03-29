import numpy as np
from collections import deque

"""
Identify unique red (2) and green (3) objects on a white (0) background.
If there is exactly one 2x2 green object and exactly one red object, replicate the red object by reflecting it across the horizontal, vertical, and center axes defined by the center of the 2x2 green square.
The three reflected copies are added to the original grid.
If the conditions (one 2x2 green object, one red object) are not met, return the input grid unchanged.
"""

def find_objects(grid, color):
    """Finds all contiguous objects of a specified color in the grid."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def is_2x2(obj_coords):
    """Checks if a set of coordinates forms a 2x2 square."""
    if len(obj_coords) != 4:
        return False
    rows = sorted([r for r, c in obj_coords])
    cols = sorted([c for r, c in obj_coords])
    return rows[0] == rows[1] and rows[2] == rows[3] and rows[0] + 1 == rows[2] and \
           cols[0] == cols[2] and cols[1] == cols[3] and cols[0] + 1 == cols[1]


def transform(input_grid):
    """
    Applies the reflection transformation based on the presence of a single 2x2
    green square and a single red object.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find green objects (color 3)
    green_objects = find_objects(input_grid, 3)

    # Find red objects (color 2)
    red_objects = find_objects(input_grid, 2)

    # Check conditions: exactly one green object, exactly one red object, and green is 2x2
    if len(green_objects) != 1 or len(red_objects) != 1:
        return output_grid # Return original if counts are wrong

    green_coords = green_objects[0]
    if not is_2x2(green_coords):
        return output_grid # Return original if green object is not 2x2

    red_coords = red_objects[0]

    # Calculate the center of the green 2x2 square
    min_r = min(r for r, c in green_coords)
    min_c = min(c for r, c in green_coords)
    center_r = min_r + 0.5
    center_c = min_c + 0.5

    # Iterate through each pixel of the red object and calculate reflections
    for r, c in red_coords:
        # Horizontal reflection (across horizontal line through center)
        ref_r_h = int(round(2 * center_r - (r + 1))) # Using pixel center (r+0.5) -> 2*center_r - (r+0.5) - 0.5 = 2*center_r - r - 1
        ref_c_h = c

        # Vertical reflection (across vertical line through center)
        ref_r_v = r
        ref_c_v = int(round(2 * center_c - (c + 1))) # Using pixel center (c+0.5) -> 2*center_c - (c+0.5) - 0.5 = 2*center_c - c - 1

        # Center reflection (180-degree rotation)
        ref_r_c = ref_r_h # Same row calculation as horizontal
        ref_c_c = ref_c_v # Same col calculation as vertical

        # Apply reflections to the output grid if within bounds
        # Note: The original red object is already in output_grid
        
        # Horizontal Reflection
        if 0 <= ref_r_h < rows and 0 <= ref_c_h < cols:
            output_grid[ref_r_h, ref_c_h] = 2

        # Vertical Reflection
        if 0 <= ref_r_v < rows and 0 <= ref_c_v < cols:
            output_grid[ref_r_v, ref_c_v] = 2

        # Center Reflection
        if 0 <= ref_r_c < rows and 0 <= ref_c_c < cols:
            output_grid[ref_r_c, ref_c_c] = 2

    return output_grid