```python
"""
Identifies a single gray pixel (color 5) as a target location.
Identifies a contiguous shape composed of colors other than white (0) and gray (5).
Calculates the center of the bounding box of this source shape.
Copies the source shape to the target location, aligning the shape's calculated center with the gray pixel's coordinates.
The copied shape overwrites existing pixels at the target location. The original shape remains in place.
"""

import numpy as np
from collections import deque

def find_pixels(grid, color_value):
    """Finds all coordinates of pixels with a specific color value."""
    coords = np.argwhere(grid == color_value)
    return [(int(r), int(c)) for r, c in coords] # Ensure integer indices

def get_connected_component(grid, start_r, start_c):
    """
    Finds all connected pixels belonging to the same object, starting from (start_r, start_c).
    Connectivity is 8-way (including diagonals).
    The object is defined as contiguous pixels that are not background (0) and not the marker color (5).
    """
    height, width = grid.shape
    q = deque([(start_r, start_c)])
    component = set()
    visited = set()

    # Check if starting point itself is valid
    start_color = grid[start_r, start_c]
    if start_color == 0 or start_color == 5:
        return component # Start point is not part of a valid shape

    while q:
        r, c = q.popleft()

        # Check bounds
        if not (0 <= r < height and 0 <= c < width):
            continue

        # Check if already visited
        if (r, c) in visited:
            continue

        # Check if pixel is part of the shape (not background or marker)
        color = grid[r, c]
        if color == 0 or color == 5:
            continue

        # Add to component and mark visited
        visited.add((r, c))
        component.add((r, c))

        # Explore neighbors (8-way connectivity)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                # Add neighbor to queue only if within bounds (further checks happen when popped)
                if 0 <= nr < height and 0 <= nc < width:
                     if (nr, nc) not in visited:
                        q.append((nr, nc))

    return component

def transform(input_grid):
    """
    Copies a shape identified by non-background, non-marker colors to a location
    specified by a gray marker pixel. The shape is centered on the marker.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # 1. Locate the coordinates (Gy, Gx) of the single gray pixel (color 5)
    gray_coords = find_pixels(input_grid_np, 5)
    if not gray_coords:
        # Task guarantees one gray pixel, but handle defensively
        print("Warning: No gray marker (color 5) found.")
        return output_grid.tolist() # Return original if no marker
    Gy, Gx = gray_coords[0] # Assuming exactly one gray pixel

    # 2. Identify the "source shape"
    source_pixels = set()
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            # Check if it's a potential start of the shape and not already found
            if color != 0 and color != 5:
                 # Check if this pixel is already part of the found shape to avoid re-running BFS
                 is_part_of_found_shape = False
                 for pr, pc in source_pixels:
                     if r == pr and c == pc:
                         is_part_of_found_shape = True
                         break
                 if not is_part_of_found_shape:
                    component = get_connected_component(input_grid_np, r, c)
                    if component: # Found the shape
                        source_pixels = component
                        break # Stop searching once the shape is found
        if source_pixels:
            break # Stop outer loop as well

    if not source_pixels:
        # Handle case where no source shape is found
        print("Warning: No source shape (non-0, non-5 pixels) found.")
        return output_grid.tolist()

    # 3. Determine the bounding box and calculate the reference center
    rows = [p[0] for p in source_pixels]
    cols = [p[1] for p in source_pixels]
    min_y, max_y = min(rows), max(rows)
    min_x, max_x = min(cols), max(cols)

    # Calculate center reference point (integer division for center)
    Ref_y = min_y + (max_y - min_y) // 2
    Ref_x = min_x + (max_x - min_x) // 2

    # 4. Iterate through source shape pixels and copy them to the target location
    for Sy, Sx in source_pixels:
        color = input_grid_np[Sy, Sx] # Get the color of the source pixel

        # Calculate the corresponding target coordinates (Ty, Tx)
        # Offset from shape center = (Sy - Ref_y, Sx - Ref_x)
        # Target coord = Marker coord + Offset
        Ty = Gy + (Sy - Ref_y)
        Tx = Gx + (Sx - Ref_x)

        # Check if the target coordinates are within the grid bounds
        if 0 <= Ty < height and 0 <= Tx < width:
            # Update the output grid at the target coordinates
            output_grid[Ty, Tx] = color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```