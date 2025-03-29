import numpy as np
from collections import deque, namedtuple

BoundingBox = namedtuple("BoundingBox", ["min_row", "max_row", "min_col", "max_col"])

def find_connected_components(grid, ignore_color=0):
    """
    Finds all connected components (objects) in the grid, ignoring a specific color.
    Uses BFS.
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
    both inside and outside the given bounding box.
    """
    rows, cols = grid.shape
    candidate_colors = set(np.unique(grid)) - {ignore_color, main_shape_color}

    for color in candidate_colors:
        found_inside = False
        found_outside = False
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color:
                    is_inside = (bbox.min_row <= r <= bbox.max_row and 
                                 bbox.min_col <= c <= bbox.max_col)
                    if is_inside:
                        found_inside = True
                    else:
                        found_outside = True
                if found_inside and found_outside:
                    return color # Found the active color
    return None # No active color found


def transform(input_grid):
    """
    Transforms the input grid based on the observed pattern:
    1. Identifies the main solid shape (largest non-background object) and its bounding box.
    2. Identifies the 'active color' present both inside and outside the main shape's bounding box.
    3. Removes active color pixels from inside the main shape's bounding box.
    4. Moves active color pixels from outside the bounding box:
        - If vertically aligned with the box, move 3 columns right.
        - If horizontally aligned with the box, move to the top edge (min_row) of the box.
    """
    
    # Find the main shape (largest non-background object)
    main_shape_color, main_shape_pixels = find_largest_object(input_grid, ignore_color=0)
    
    if main_shape_color is None or main_shape_pixels is None:
        # Cannot identify main shape, return input unchanged
        return input_grid.copy()
        
    # Determine the bounding box of the main shape
    bbox = get_bounding_box(main_shape_pixels)
    if bbox is None:
         # Should not happen if main_shape_pixels is not None, but safety check
        return input_grid.copy()

    # Identify the active color
    active_color = find_active_color(input_grid, main_shape_color, bbox, ignore_color=0)
    
    if active_color is None:
        # Cannot identify active color, return input unchanged
        return input_grid.copy()
        
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    
    # Store movements to apply later to avoid conflicts during iteration
    movements = [] # List of tuples: (target_r, target_c, color)

    # Iterate through the input grid to process active color pixels
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
                    # Remove active color pixel from its original outside position
                    output_grid[r, c] = 0 
                    
                    # Determine target position for movement
                    target_r, target_c = -1, -1 # Initialize invalid target

                    # Check if pixel is vertically aligned (within column span of bbox)
                    if bbox.min_col <= c <= bbox.max_col:
                        target_r, target_c = r, c + 3
                    # Check if pixel is horizontally aligned (within row span of bbox)
                    elif bbox.min_row <= r <= bbox.max_row:
                         target_r, target_c = bbox.min_row, c
                         
                    # Check if target is valid and within grid bounds before adding movement
                    if 0 <= target_r < rows and 0 <= target_c < cols:
                         movements.append((target_r, target_c, active_color))

    # Apply the stored movements to the output grid
    for r, c, color in movements:
        # Check bounds again just in case (e.g., if multiple pixels move to same spot, last one wins)
         if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = color

    return output_grid