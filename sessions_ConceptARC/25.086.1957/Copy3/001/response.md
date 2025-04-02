```python
import numpy as np
from collections import deque

"""
This program transforms an input grid based on the presence or absence of magenta (6) pixels.

1.  **Check for Magenta:** Determine if any magenta pixels exist in the input grid.

2.  **If Magenta is Absent:**
    a.  Calculate a horizontal shift: `shift_col = width // 2 - 1`. Vertical shift is 0.
    b.  Identify all non-white objects fully contained within the left half of the grid (columns 0 to `width // 2 - 1`).
    c.  Copy each of these objects, applying the calculated shift `(0, shift_col)` to each pixel's coordinates.
    d.  Draw the copied objects onto the output grid (initialized as a copy of the input).

3.  **If Magenta is Present:**
    a.  Identify all non-white objects and find the one with the largest area (most pixels).
    b.  Identify all distinct magenta objects.
    c.  Determine the top-left coordinate for each magenta object.
    d.  Sort these top-left coordinates first by row, then by column.
    e.  Select the coordinates of the *second* magenta object in the sorted list. These coordinates `(shift_row, shift_col)` define the shift vector.
    f.  Copy the largest non-white object, applying the shift vector `(shift_row, shift_col)` to each of its pixels.
    g.  Draw the copied largest object onto the output grid.

The output grid starts as a copy of the input grid, and the copied objects overwrite existing pixels at their new locations.
"""

def find_objects(grid, target_color=None):
    """
    Finds all contiguous objects of non-background pixels (or a specific color).
    Includes diagonal connectivity.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int, optional): If specified, only find objects of this color.
                                      Otherwise, find all non-zero colored objects.

    Returns:
        list: A list of objects. Each object is a dictionary:
              {'coords': set((r, c), ...), 'color': int, 'size': int}
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue

            color = grid[r, c]

            # Skip background or non-target colors
            if color == background_color:
                visited.add((r,c)) # Mark background as visited too
                continue
            if target_color is not None and color != target_color:
                continue # Skip if looking for specific color and this isn't it

            # Start BFS for a new object
            q = deque([(r, c)])
            current_object_coords = set()
            visited.add((r, c))
            obj_color = color # All pixels in an object have the same color

            while q:
                row, col = q.popleft()
                current_object_coords.add((row, col))

                # Check 8 neighbors (including diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc

                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor_color = grid[nr, nc]
                            # Check if neighbor is part of the same object and not visited
                            if (nr, nc) not in visited and neighbor_color == obj_color:
                                visited.add((nr, nc))
                                q.append((nr, nc))

            if current_object_coords:
                objects.append({
                    'coords': current_object_coords,
                    'color': obj_color,
                    'size': len(current_object_coords)
                })

    return objects

def get_top_left(obj_coords):
    """Calculates the top-left coordinate of an object."""
    if not obj_coords:
        return None
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords if r == min_r) # Find min col among min rows
    # Refined: find global min_r and global min_c independently
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    return (min_r, min_c)


def transform(input_grid):
    """
    Transforms the input grid based on the presence/absence of magenta pixels.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Check for magenta pixels (color 6)
    magenta_present = np.any(input_np == 6)

    if not magenta_present:
        # --- Case 1: No Magenta ---
        shift_row = 0
        shift_col = cols // 2 - 1 # As derived from example 1

        # Check if shift is valid (e.g., for very narrow grids)
        if shift_col < 0:
             shift_col = 0 # Avoid negative shift, perhaps just copy in place or no copy? Adjust as needed.

        all_objects = find_objects(input_np)
        left_half_boundary = cols // 2

        for obj in all_objects:
            # Check if the entire object is within the left half
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
                    # Draw pixel if within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        output_grid[nr, nc] = obj_color

    else:
        # --- Case 2: Magenta Present ---
        # Find all non-white objects
        all_objects = find_objects(input_np)

        if not all_objects:
             return output_grid.tolist() # No objects to move

        # Find the largest object
        largest_object = max(all_objects, key=lambda obj: obj['size'])

        # Find all magenta objects
        magenta_objects = find_objects(input_np, target_color=6)

        if len(magenta_objects) < 2:
             # Handle cases with 0 or 1 magenta object - behavior undefined by examples.
             # Let's assume no copy happens in this edge case.
             return output_grid.tolist()

        # Get top-left coordinates of magenta objects
        magenta_top_lefts = []
        for m_obj in magenta_objects:
            tl = get_top_left(m_obj['coords'])
            if tl:
                magenta_top_lefts.append(tl)

        # Sort coordinates (row first, then column)
        magenta_top_lefts.sort()

        # Get the shift vector from the second magenta object's top-left coordinate
        shift_row, shift_col = magenta_top_lefts[1] # Index 1 for the second item

        # Copy the largest object using the shift vector
        largest_obj_color = largest_object['color']
        for r, c in largest_object['coords']:
            nr, nc = r + shift_row, c + shift_col
            # Draw pixel if within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = largest_obj_color

    return output_grid.tolist()
```