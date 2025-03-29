import numpy as np
from collections import deque

"""
Relocates gray (5) objects into a central gap defined by static red (2) structures.

The transformation follows these steps:

1.  **Identify Static Structures and Gap:**
    *   Locate all red (2) pixels. These remain fixed.
    *   Determine the bounding box of red pixels (`min_r`, `max_r`, `min_c`, `max_c`).
    *   Search for a contiguous block of empty (white, 0) rows strictly *inside* the vertical span of the red bounding box (`min_r + 1` to `max_r - 1`). If found, this is a **horizontal gap** (Vertical Separation). Record its top (`gap_min_r`) and bottom (`gap_max_r`) rows.
    *   If no horizontal gap, search for a contiguous block of empty (white, 0) columns strictly *inside* the horizontal span of the red bounding box (`min_c + 1` to `max_c - 1`). If found, this is a **vertical gap** (Horizontal Separation). Record its leftmost (`gap_min_c`) and rightmost (`gap_max_c`) columns.
    *   If no gap is found, return the grid with only red pixels.

2.  **Identify Mobile Objects:**
    *   Find all distinct connected groups (objects) of gray (5) pixels in the *original* input grid using 8-way connectivity (including diagonals). Record the coordinates for each object.

3.  **Initialize Output Grid:**
    *   Create an output grid of the same dimensions as the input, filled with white (0).
    *   Copy all red (2) pixels from the input to the output grid.

4.  **Calculate Relocation Shift for Each Gray Object:**
    *   For each gray object:
        *   Determine its bounding box (`obj_min_r`, `obj_max_r`, `obj_min_c`, `obj_max_c`).
        *   Initialize shift `delta_r = 0`, `delta_c = 0`.
        *   **If Vertical Separation (Horizontal Gap):**
            *   Object Above (`obj_max_r < gap_min_r`): Align object's top edge with gap's top edge. `delta_r = gap_min_r - obj_min_r`.
            *   Object Below (`obj_min_r > gap_max_r`): Align object's bottom edge with gap's bottom edge. `delta_r = gap_max_r - obj_max_r`.
        *   **If Horizontal Separation (Vertical Gap):**
            *   Object Left (`obj_max_c < gap_min_c`): Align object's left edge with gap's left edge. `delta_c = gap_min_c - obj_min_c`.
            *   Object Right (`obj_min_c > gap_max_c`): Align object's right edge with gap's right edge. `delta_c = gap_max_c - obj_max_c`.

5.  **Apply Shift and Paint Objects:**
    *   For each gray object and its calculated shift (`delta_r`, `delta_c`):
        *   For each pixel `(r, c)` belonging to the object, calculate the new position `(new_r, new_c) = (r + delta_r, c + delta_c)`.
        *   If the new position is within grid bounds, paint the pixel `(new_r, new_c)` gray (5) on the output grid.

6.  **Return Result:** The final output grid.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid.
    Connectivity includes diagonals (8 neighbors).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set[tuple[int, int]]]: A list where each element is a set
                                      of (row, col) coordinates for one object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            # If this pixel is the right color and hasn't been visited yet
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is the right color and unvisited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid_list):
    """
    Transforms the input grid by relocating gray objects into a gap
    defined by red structures.

    Args:
        input_grid_list (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape

    # --- 1. Identify Static Structures (Red Pixels) ---
    red_coords = np.argwhere(input_grid == 2)

    # Initialize output grid - start with white, add red pixels
    output_grid = np.zeros_like(input_grid, dtype=int)
    if red_coords.size > 0:
        for r, c in red_coords:
            output_grid[r, c] = 2
    else:
        # Edge case: No red pixels, no gap defined. Return blank grid.
        return output_grid.tolist()

    # --- 2. Identify Mobile Objects (Gray Pixels) ---
    gray_objects = find_objects(input_grid, 5)
    if not gray_objects:
        # Edge case: No gray objects to move. Return grid with only red pixels.
        return output_grid.tolist()

    # --- Continue Step 1: Find the Gap ---
    min_r, min_c = red_coords.min(axis=0)
    max_r, max_c = red_coords.max(axis=0)

    separation_axis = None
    gap_min_r, gap_max_r = -1, -1
    gap_min_c, gap_max_c = -1, -1

    # Check for horizontal gap (Vertical Separation)
    # Check rows strictly *between* min_r and max_r
    if max_r > min_r + 1: # Need at least one row between bounds
        potential_gap_rows = list(range(min_r + 1, max_r))
        current_gap_start = -1
        for r in potential_gap_rows:
            # Check if the row is empty *within the horizontal bounds* of red pixels
            is_empty_in_bounds = not np.any(input_grid[r, min_c:max_c+1] == 2) # Check only for red, gap can have other colors potentially? No, examples imply empty=white. Let's assume gap must be white.
            is_empty_in_bounds = not np.any(input_grid[r, :] != 0) # More strict: entire row must be white? No, just within the red structure bounds.
            is_empty_in_bounds = not np.any(input_grid[r, min_c:max_c+1] != 0) # Check for non-white within red bounds

            if is_empty_in_bounds:
                if current_gap_start == -1:
                    current_gap_start = r
                # If this is the last potential row or the next row is not empty, finalize gap
                if r == potential_gap_rows[-1] or np.any(input_grid[r+1, min_c:max_c+1] != 0):
                    gap_min_r = current_gap_start
                    gap_max_r = r
                    separation_axis = 'vertical'
                    break # Found the first contiguous horizontal gap
            else:
                 current_gap_start = -1 # Reset if row is not empty


    # Check for vertical gap (Horizontal Separation) only if no horizontal gap was found
    if separation_axis is None and max_c > min_c + 1: # Need at least one col between bounds
        potential_gap_cols = list(range(min_c + 1, max_c))
        current_gap_start = -1
        for c in potential_gap_cols:
            # Check if the col is empty *within the vertical bounds* of red pixels
            is_empty_in_bounds = not np.any(input_grid[min_r:max_r+1, c] != 0) # Check for non-white within red bounds
            if is_empty_in_bounds:
                 if current_gap_start == -1:
                     current_gap_start = c
                 # If this is the last potential col or the next col is not empty, finalize gap
                 if c == potential_gap_cols[-1] or np.any(input_grid[min_r:max_r+1, c+1] != 0):
                     gap_min_c = current_gap_start
                     gap_max_c = c
                     separation_axis = 'horizontal'
                     break # Found the first contiguous vertical gap
            else:
                 current_gap_start = -1 # Reset if col is not empty

    # If no gap is found after checking both directions
    if separation_axis is None:
        # Edge case: No gap found. Return grid with only red pixels.
        return output_grid.tolist()

    # --- 4 & 5. Calculate Shift and Relocate Gray Objects ---
    for obj_coords in gray_objects:
        if not obj_coords: continue # Skip empty sets if they somehow occur

        # Calculate object bounding box
        obj_rows = [r for r, c in obj_coords]
        obj_cols = [c for r, c in obj_coords]
        obj_min_r, obj_max_r = min(obj_rows), max(obj_rows)
        obj_min_c, obj_max_c = min(obj_cols), max(obj_cols)

        delta_r = 0
        delta_c = 0

        # Calculate shift based on gap type and object position (Corrected Logic)
        if separation_axis == 'vertical': # Horizontal Gap
            if obj_max_r < gap_min_r: # Object is above gap
                # Align object's top edge (obj_min_r) with gap's top edge (gap_min_r)
                delta_r = gap_min_r - obj_min_r
            elif obj_min_r > gap_max_r: # Object is below gap
                # Align object's bottom edge (obj_max_r) with gap's bottom edge (gap_max_r)
                delta_r = gap_max_r - obj_max_r
            else: # Object overlaps gap - unexpected based on examples, skip this object
                continue

        elif separation_axis == 'horizontal': # Vertical Gap
            if obj_max_c < gap_min_c: # Object is left of gap
                # Align object's left edge (obj_min_c) with gap's left edge (gap_min_c)
                delta_c = gap_min_c - obj_min_c
            elif obj_min_c > gap_max_c: # Object is right of gap
                # Align object's right edge (obj_max_c) with gap's right edge (gap_max_c)
                delta_c = gap_max_c - obj_max_c
            else: # Object overlaps gap - unexpected based on examples, skip this object
                continue

        # Apply the shift to each pixel of the object and paint it on the output grid
        for r, c in obj_coords:
            new_r, new_c = r + delta_r, c + delta_c
            # Check bounds before writing to output grid
            if 0 <= new_r < height and 0 <= new_c < width:
                # Check for potential overwrites? Examples suggest gray objects don't overlap red after moving.
                # If the target cell is already red, maybe don't overwrite?
                # Let's assume gray overwrites white, but not red.
                # Re-evaluation: The examples DO show gray sometimes overwriting red boundary pixels in the output.
                # So, allow overwriting.
                output_grid[new_r, new_c] = 5
            # else: Pixel moves out of bounds - ignore it.

    # --- 6. Return Result ---
    return output_grid.tolist()