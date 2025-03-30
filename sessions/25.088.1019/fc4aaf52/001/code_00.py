import numpy as np
from collections import Counter

"""
Identifies a single non-background object in the input grid, determines its properties (bounding box, colors, max color). 
Calculates a horizontal shift based on the object's rightmost column and the parity of its maximum color value. 
Creates a copy of the object, changes all its pixels to the maximum color value, and places this monochrome copy 
in the calculated shifted position on the output grid, while preserving the original object in its place.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    # Assuming background is the most frequent color
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_connected_object(grid, start_r, start_c, background_color, visited):
    """Finds all connected non-background pixels starting from (start_r, start_c) using BFS."""
    rows, cols = grid.shape
    q = [(start_r, start_c)]
    object_coords = set()
    object_colors = set()

    while q:
        r, c = q.pop(0)

        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in visited or grid[r, c] == background_color:
            continue

        visited.add((r, c))
        object_coords.add((r, c))
        object_colors.add(grid[r, c])

        # Check neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr, nc] != background_color:
                 q.append((nr, nc))

    return object_coords, object_colors


def find_the_object(grid, background_color):
    """Finds the single non-background object in the grid."""
    rows, cols = grid.shape
    visited = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                # Found the start of the object, find all connected parts
                object_coords, object_colors = find_connected_object(grid, r, c, background_color, visited)
                if object_coords: # Ensure an object was actually found
                    return object_coords, object_colors
    return None, None # Should not happen based on task description


def get_object_properties(object_coords, object_colors):
    """Calculates bounding box and finds the maximum color value."""
    if not object_coords:
        return None, None, None, None, None

    rows = [r for r, c in object_coords]
    cols = [c for r, c in object_coords]

    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    target_color = max(object_colors)

    return min_row, max_row, min_col, max_col, target_color


def transform(input_grid):
    """
    Applies the transformation rule: duplicate object, change color to max, shift right.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify the background color
    background_color = find_background_color(grid)

    # 2. Find the single connected non-background object
    object_coords, object_colors = find_the_object(grid, background_color)

    if not object_coords:
        # If no object found (e.g., empty grid or all background), return original
        return input_grid

    # 3. Determine object properties
    min_row, max_row, min_col, max_col, target_color = get_object_properties(object_coords, object_colors)

    # 4. Calculate the translation offset and shift
    # offset = -1 if target_color is odd else 1
    offset = -1 if target_color % 2 != 0 else 1
    # new_min_col = max_col + 1 + offset
    # Note: The shift calculation places the *start* of the copy relative to the *end* of the original.
    # The actual distance to shift each pixel is the difference between the new start and the old start.
    new_copy_min_col = max_col + 1 + offset
    shift = new_copy_min_col - min_col

    # 5. Initialize the output grid as a copy of the input grid
    output_grid = np.copy(grid)

    # 6. Iterate through original object pixels and place the colored, shifted copy
    for r, c in object_coords:
        # Calculate destination coordinates for the copy
        r_dest, c_dest = r, c + shift

        # Check if the destination is within grid bounds
        if 0 <= r_dest < rows and 0 <= c_dest < cols:
            # Set the pixel in the output grid to the target color
            output_grid[r_dest, c_dest] = target_color
        # else: the copied pixel falls off the grid, do nothing

    # Convert output numpy array back to list of lists
    return output_grid.tolist()