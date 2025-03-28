```python
import numpy as np
from collections import deque

"""
This program transforms an input grid based on the presence or absence of magenta (6) pixels. The output grid starts as a copy of the input.

1.  **Check for Magenta:** Determine if any magenta pixels exist in the input grid.

2.  **If Magenta is Absent:**
    a.  Calculate a horizontal shift: `shift_col = floor(width / 2) - 1`. Vertical shift `shift_row` is 0.
    b.  Identify all distinct, single-color, non-white objects fully contained within the left half of the grid (columns 0 to `floor(width / 2) - 1`), using 8-way connectivity.
    c.  Copy each of these objects, applying the calculated shift `(shift_row, shift_col)` to each pixel's coordinates. Draw the copied objects onto the output grid, overwriting existing pixels.

3.  **If Magenta is Present:**
    a.  Find the coordinate `(start_r, start_c)` of the first pixel (scanning top-to-bottom, left-to-right) that is neither white (0) nor magenta (6). If none exists, return the initial copy.
    b.  Perform a search (BFS) starting from `(start_r, start_c)` to find all reachable non-white pixels using 8-way connectivity.
    c.  Define the "Source Object" as the set of all pixels found in step 3b that are *not* magenta. Store their original coordinates and colors.
    d.  Identify all distinct magenta objects (contiguous blocks of color 6) using 8-way connectivity.
    e.  For each distinct magenta object, find its top-left coordinate (minimum row, then minimum column).
    f.  Collect all unique top-left coordinates of the magenta objects.
    g.  Sort these coordinates first by row index, then by column index.
    h.  If there are fewer than two sorted coordinates, return the initial copy. Otherwise, select the *second* coordinate pair in the sorted list as the shift vector `(shift_row, shift_col)`.
    i.  Copy the "Source Object". For each pixel `(r, c)` with color `clr` in the Source Object, draw the color `clr` at the new coordinate `(r + shift_row, c + shift_col)` on the output grid, overwriting any existing pixel.

The output grid starts as a copy of the input grid, and the copied objects overwrite existing pixels at their new locations.
"""

def find_single_color_objects(grid, target_color=None, connectivity=8):
    """
    Finds all contiguous objects of a specific color or any non-background color.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int, optional): If specified, only find objects of this color.
                                      Otherwise, find all non-zero colored objects.
        connectivity (int): 4 or 8 for neighbor checking. Default is 8.

    Returns:
        list: A list of objects. Each object is a dictionary:
              {'coords': set((r, c), ...), 'color': int, 'size': int}
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    background_color = 0

    if connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else: # connectivity 4
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue

            color = grid[r, c]

            # Skip background
            if color == background_color:
                visited.add((r, c))
                continue
            # Skip if looking for a specific color and this isn't it
            if target_color is not None and color != target_color:
                continue

            # Start BFS for a new object of the current color
            q = deque([(r, c)])
            current_object_coords = set()
            visited.add((r, c))
            obj_color = color # All pixels in this object must have this color

            while q:
                row, col = q.popleft()
                current_object_coords.add((row, col))

                # Check neighbors
                for dr, dc in deltas:
                    nr, nc = row + dr, col + dc

                    # Check bounds and if neighbor is part of the same object (same color) and not visited
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       (nr, nc) not in visited and grid[nr, nc] == obj_color:
                        visited.add((nr, nc))
                        q.append((nr, nc))

            if current_object_coords:
                objects.append({
                    'coords': current_object_coords,
                    'color': obj_color,
                    'size': len(current_object_coords)
                })

    return objects


def get_top_left(coords):
    """Calculates the top-left coordinate (min row, then min col) of a set of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords if r == min_r) # Min col among those with min row
    # Correction: Find global min_r and global min_c independently is simpler/often intended.
    # Let's stick to the strict definition: min row, then min col *among min rows*
    # Re-correction: Based on many ARC tasks, global min_r and global min_c is usually expected. Let's use that.
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return (min_r, min_c)


def find_connected_component(grid, start_node, connectivity=8):
    """
    Finds all non-background pixels connected to start_node using BFS.

    Args:
        grid (np.ndarray): The input grid.
        start_node (tuple): The (row, col) to start the search from.
        connectivity (int): 4 or 8 for neighbor checking. Default is 8.

    Returns:
        set: A set of tuples (r, c, color) for all pixels in the connected component.
             Returns an empty set if start_node is background or out of bounds.
    """
    rows, cols = grid.shape
    r_start, c_start = start_node

    if not (0 <= r_start < rows and 0 <= c_start < cols) or grid[r_start, c_start] == 0:
        return set()

    if connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else: # connectivity 4
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    q = deque([start_node])
    visited = {start_node}
    component_pixels = set()
    component_pixels.add((r_start, c_start, grid[r_start, c_start]))

    while q:
        r, c = q.popleft()

        for dr, dc in deltas:
            nr, nc = r + dr, c + dc

            # Check bounds, if non-background, and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] != 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                component_pixels.add((nr, nc, grid[nr, nc]))
                q.append((nr, nc))

    return component_pixels


def transform(input_grid):
    """
    Transforms the input grid based on the presence/absence of magenta pixels.
    Copies objects either from the left half (no magenta) or a specific
    composite object determined by magenta marker positions.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape
    magenta_color = 6
    background_color = 0
    connectivity = 8 # Use 8-way connectivity as specified

    # Check for magenta pixels
    magenta_present = np.any(input_np == magenta_color)

    if not magenta_present:
        # --- Case 1: No Magenta ---
        shift_row = 0
        # Calculate horizontal shift based on grid width
        shift_col = cols // 2 - 1
        # Ensure shift is not negative for very narrow grids
        if shift_col < 0:
             shift_col = 0

        # Find all single-color non-white objects
        all_objects = find_single_color_objects(input_np, connectivity=connectivity)

        # Define the boundary for the left half
        left_half_boundary = cols // 2

        # Iterate through objects and copy those entirely in the left half
        for obj in all_objects:
            is_in_left_half = True
            for r, c in obj['coords']:
                if c >= left_half_boundary:
                    is_in_left_half = False
                    break

            if is_in_left_half:
                # Copy the object with the calculated shift
                obj_color = obj['color']
                for r, c in obj['coords']:
                    nr, nc = r + shift_row, c + shift_col
                    # Draw pixel if within output grid bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        output_grid[nr, nc] = obj_color

    else:
        # --- Case 2: Magenta Present ---
        # Find the first non-background, non-magenta pixel
        start_node = None
        for r in range(rows):
            for c in range(cols):
                if input_np[r, c] != background_color and input_np[r, c] != magenta_color:
                    start_node = (r, c)
                    break
            if start_node:
                break

        # If no such starting pixel, return the initial copy
        if start_node is None:
             return output_grid.tolist()

        # Find the connected component starting from this node
        connected_component = find_connected_component(input_np, start_node, connectivity=connectivity)

        # Define the Source Object (non-magenta pixels from the component)
        source_object_pixels = {(r, c, color) for r, c, color in connected_component if color != magenta_color}

        if not source_object_pixels:
             # If the component was only magenta or empty, nothing to copy
             return output_grid.tolist()

        # Find all distinct magenta objects
        magenta_objects = find_single_color_objects(input_np, target_color=magenta_color, connectivity=connectivity)

        # If fewer than 2 magenta objects, cannot determine shift, return initial copy
        if len(magenta_objects) < 2:
             return output_grid.tolist()

        # Get top-left coordinates of magenta objects
        magenta_top_lefts = []
        for m_obj in magenta_objects:
            tl = get_top_left(m_obj['coords'])
            if tl:
                magenta_top_lefts.append(tl)

        # Ensure we have unique top-lefts in case objects overlap in top-left calc?
        # The spec says "distinct magenta objects", so their coordinates should be distinct.
        # If multiple objects share the same min_r, min_c, get_top_left will return the same point.
        # Let's assume the examples imply distinct locations matter. Using unique set of TLs.
        unique_magenta_top_lefts = sorted(list(set(magenta_top_lefts)))

        # Check again if we have at least two unique positions
        if len(unique_magenta_top_lefts) < 2:
             return output_grid.tolist()

        # Sort coordinates (row first, then column) - sorting the unique set handles this
        # Get the shift vector from the *second* unique magenta object's top-left coordinate
        shift_row, shift_col = unique_magenta_top_lefts[1] # Index 1 for the second item

        # Copy the Source Object using the shift vector
        for r, c, color in source_object_pixels:
            nr, nc = r + shift_row, c + shift_col
            # Draw pixel if within output grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = color

    # Return the transformed grid as a list of lists
    return output_grid.tolist()
```