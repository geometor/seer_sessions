```python
import numpy as np
from collections import deque, namedtuple
import math

"""
Transforms the input grid based on the following rules:
1. Identifies the main solid shape (largest non-background connected component) and its bounding box.
2. Calculates the width of the bounding box.
3. Identifies the 'active color' - a color (not background or main shape color) present both inside and outside the main shape's bounding box.
4. Creates an output grid initially identical to the input.
5. Removes active color pixels from inside the main shape's bounding box in the output grid (sets them to background color 0).
6. Moves active color pixels from outside the bounding box in the output grid:
    a. Erases the pixel from its original position (sets to background color 0).
    b. If the pixel was vertically aligned with the box (within its column range), its new position is in the same row, but shifted right by floor(bounding_box_width / 2) columns.
    c. If the pixel was horizontally aligned with the box (within its row range), its new position is in the same column, but moved to the top row of the bounding box (bbox.min_row).
7. The moved pixels are painted onto the output grid in their new locations. If multiple pixels move to the same location, the last one processed determines the final color.
"""

BoundingBox = namedtuple("BoundingBox", ["min_row", "max_row", "min_col", "max_col"])

def find_connected_components(grid, ignore_color=0):
    """
    Finds all connected components (objects) in the grid, ignoring a specific color.
    Uses BFS with 8-way connectivity (including diagonals).
    Returns a list of tuples: (color, set_of_coordinates).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                component_pixels.add((nr, nc))
                                q.append((nr, nc))

                if component_pixels:
                     components.append((color, component_pixels))

    return components

def find_largest_object(grid, ignore_color=0):
    """
    Finds the largest connected component (object) in the grid, ignoring the background color.
    Returns the color and pixels of the largest object, or (None, None) if no object found.
    """
    components = find_connected_components(grid, ignore_color)
    if not components:
        return None, None

    largest_component = max(components, key=lambda item: len(item[1]))
    return largest_component[0], largest_component[1]


def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixel coordinates.
    Returns a BoundingBox named tuple, or None if pixels set is empty.
    """
    if not pixels:
        return None

    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]

    return BoundingBox(min(rows), max(rows), min(cols), max(cols))

def find_active_color(grid, main_shape_color, bbox, ignore_color=0):
    """
    Finds the color (other than background and main shape color) that exists
    both inside and outside the given bounding box. Returns the color or None.
    """
    rows, cols = grid.shape
    # Find all unique colors present in the grid
    unique_colors = set(np.unique(grid))
    # Define candidate colors: exclude background and main shape color
    candidate_colors = unique_colors - {ignore_color, main_shape_color}

    for color in candidate_colors:
        found_inside = False
        found_outside = False
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color:
                    # Check if the pixel is inside the bounding box
                    is_inside = (bbox.min_row <= r <= bbox.max_row and
                                 bbox.min_col <= c <= bbox.max_col)
                    if is_inside:
                        found_inside = True
                    else:
                        found_outside = True
                # If we found the color both inside and outside, no need to check further for this color
                if found_inside and found_outside:
                    return color # Found the active color

    return None # No active color found


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    rows, cols = input_grid.shape

    # 1. Identify the main shape (largest non-background object)
    main_shape_color, main_shape_pixels = find_largest_object(input_grid, ignore_color=0)

    if main_shape_color is None or main_shape_pixels is None:
        # Cannot identify main shape, return input unchanged
        return input_grid.copy()

    # 2. Determine the bounding box of the main shape
    bbox = get_bounding_box(main_shape_pixels)
    if bbox is None:
         # Should not happen if main_shape_pixels is not None, but safety check
        return input_grid.copy()

    # Calculate bounding box width
    bbox_width = bbox.max_col - bbox.min_col + 1
    # Calculate the vertical shift distance
    vertical_shift = math.floor(bbox_width / 2)


    # 3. Identify the active color
    active_color = find_active_color(input_grid, main_shape_color, bbox, ignore_color=0)

    if active_color is None:
        # Cannot identify active color, return input unchanged
        return input_grid.copy()

    # 4. Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()

    # 5 & 6. Process active color pixels: remove inside, determine moves for outside
    movements = [] # Store target locations for moved pixels: (target_r, target_c, color)

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == active_color:
                # Check if the pixel is inside the bounding box
                is_inside = (bbox.min_row <= r <= bbox.max_row and
                             bbox.min_col <= c <= bbox.max_col)

                if is_inside:
                    # Remove active color pixels from inside the bbox
                    output_grid[r, c] = 0
                else:
                    # Pixel is outside the bbox. Erase from original position.
                    output_grid[r, c] = 0

                    # Determine target position based on alignment
                    target_r, target_c = -1, -1 # Initialize invalid target

                    # Check if pixel is vertically aligned (within column span of bbox)
                    if bbox.min_col <= c <= bbox.max_col:
                        target_r, target_c = r, c + vertical_shift # Apply calculated shift
                    # Check if pixel is horizontally aligned (within row span of bbox)
                    elif bbox.min_row <= r <= bbox.max_row:
                         target_r, target_c = bbox.min_row, c # Move to top edge of bbox

                    # If a valid target was determined, store the movement
                    if target_r != -1 or target_c != -1: # Check if either target was set
                         movements.append((target_r, target_c, active_color))


    # 7. Apply the stored movements to the output grid
    for r, c, color in movements:
        # Apply movement only if target is within grid bounds
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = color

    return output_grid
```