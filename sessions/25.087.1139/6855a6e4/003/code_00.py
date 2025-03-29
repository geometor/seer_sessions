import numpy as np

"""
Relocates gray (5) objects into the gap defined by static red (2) structures.

The transformation follows these steps:

1.  **Identify Structures**: Locate all red (2) pixels and all gray (5) pixels in the input grid. Red pixels remain fixed.
2.  **Find the Gap**: Analyze the arrangement of red pixels to find the empty space (gap) separating them.
    *   Determine the bounding box of all red pixels.
    *   Check for a contiguous block of empty rows strictly *inside* the vertical span of the red bounding box. If found, this is a horizontal gap (Vertical Separation). Record the gap's top (`gap_min_r`) and bottom (`gap_max_r`) rows.
    *   If no horizontal gap, check for a contiguous block of empty columns strictly *inside* the horizontal span of the red bounding box. If found, this is a vertical gap (Horizontal Separation). Record the gap's leftmost (`gap_min_c`) and rightmost (`gap_max_c`) columns.
3.  **Identify Gray Objects**: Find all distinct connected groups (objects) of gray pixels from the *original* input grid using 8-way connectivity (including diagonals).
4.  **Initialize Output**: Create an output grid containing only the static red pixels, with all other cells set to white (0).
5.  **Relocate Gray Objects**: Move each identified gray object into the determined gap based on the separation type:
    *   **If Vertical Separation (Horizontal Gap):**
        *   For each gray object, determine if its original position was above or below the gap.
        *   If above (`obj_max_r < gap_min_r`), calculate the downward vertical shift (`delta_r`) needed to place the object's bottom edge at row `gap_min_r - 1`.
        *   If below (`obj_min_r > gap_max_r`), calculate the upward vertical shift (`delta_r`) needed to place the object's top edge at row `gap_max_r + 1`.
        *   Apply the shift: For each pixel `(r, c)` in the object, paint the pixel at `(r + delta_r, c)` gray (5) in the output grid. Maintain the object's shape and horizontal position.
    *   **If Horizontal Separation (Vertical Gap):**
        *   For each gray object, determine if its original position was to the left or right of the gap.
        *   If left (`obj_max_c < gap_min_c`), calculate the rightward horizontal shift (`delta_c`) needed to place the object's right edge at column `gap_min_c - 1`.
        *   If right (`obj_min_c > gap_max_c`), calculate the leftward horizontal shift (`delta_c`) needed to place the object's left edge at column `gap_max_c + 1`.
        *   Apply the shift: For each pixel `(r, c)` in the object, paint the pixel at `(r, c + delta_c)` gray (5) in the output grid. Maintain the object's shape and vertical position.
6.  **Return Result**: The output grid containing the static red pixels and the relocated gray objects.
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
                q = [(r, c)]  # Queue for BFS
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
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
    Relocates gray objects into the gap defined by static red structures.

    Args:
        input_grid_list (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape

    # --- 1. Identify Structures ---
    red_coords = np.argwhere(input_grid == 2)
    # We need gray objects later, using the original grid

    # --- Initialize Output Grid (Keep red, clear everything else) ---
    output_grid = np.zeros_like(input_grid, dtype=int) # Initialize with white (0)
    if red_coords.size > 0:
        for r, c in red_coords:
            output_grid[r, c] = 2 # Keep red pixels

    # --- 3. Identify Gray Objects ---
    gray_objects = find_objects(input_grid, 5)

    # Handle edge case: no gray objects to move
    if not gray_objects:
        return output_grid.tolist()

    # Handle edge case: no red pixels to define a gap
    if red_coords.size == 0:
        # No gap defined, unclear what to do. Return grid with only red (which is none).
        # Or maybe return the original gray positions? Based on examples, seems red is always present.
        # Let's return the grid with only red (i.e., empty if no red).
         return output_grid.tolist() # Or maybe input_grid.tolist()? Let's stick to the initialized grid.

    # --- 2. Find the Gap ---
    min_r, min_c = red_coords.min(axis=0)
    max_r, max_c = red_coords.max(axis=0)

    separation_axis = None
    gap_min_r, gap_max_r = -1, -1
    gap_min_c, gap_max_c = -1, -1

    # Check for horizontal gap (Vertical Separation)
    h_gap_rows = [r for r in range(min_r + 1, max_r) if not np.any(input_grid[r, min_c:max_c+1] == 2)]
    if h_gap_rows:
        # Find the first contiguous block of gap rows
        start_r = h_gap_rows[0]
        end_r = start_r
        for i in range(1, len(h_gap_rows)):
            if h_gap_rows[i] == end_r + 1:
                end_r = h_gap_rows[i]
            else:
                 break # Stop if the gap rows are not contiguous
        # Check if the gap found is truly internal (not touching the bbox edges implicitly)
        # This is implicitly handled by range(min_r + 1, max_r)
        if end_r >= start_r: # Ensure at least one gap row found
             separation_axis = 'vertical'
             gap_min_r = start_r
             gap_max_r = end_r

    # Check for vertical gap (Horizontal Separation) only if no horizontal gap was found
    if separation_axis is None:
        v_gap_cols = [c for c in range(min_c + 1, max_c) if not np.any(input_grid[min_r:max_r+1, c] == 2)]
        if v_gap_cols:
            # Find the first contiguous block of gap columns
            start_c = v_gap_cols[0]
            end_c = start_c
            for i in range(1, len(v_gap_cols)):
                 if v_gap_cols[i] == end_c + 1:
                     end_c = v_gap_cols[i]
                 else:
                     break # Stop if the gap columns are not contiguous
            # Check if the gap found is truly internal
            if end_c >= start_c: # Ensure at least one gap column found
                 separation_axis = 'horizontal'
                 gap_min_c = start_c
                 gap_max_c = end_c

    # If no gap is found, return the grid with only red pixels
    if separation_axis is None:
        return output_grid.tolist()

    # --- 5. Relocate Gray Objects ---
    for obj_coords in gray_objects:
        if not obj_coords: continue # Skip empty objects if any

        obj_rows = [r for r, c in obj_coords]
        obj_cols = [c for r, c in obj_coords]
        obj_min_r, obj_max_r = min(obj_rows), max(obj_rows)
        obj_min_c, obj_max_c = min(obj_cols), max(obj_cols)

        delta_r = 0
        delta_c = 0

        if separation_axis == 'vertical':
            # Determine if object is above or below the gap and calculate vertical shift
            if obj_max_r < gap_min_r: # Object is above gap
                # Target bottom row of object is gap_min_r - 1
                delta_r = (gap_min_r - 1) - obj_max_r
            elif obj_min_r > gap_max_r: # Object is below gap
                # Target top row of object is gap_max_r + 1
                delta_r = (gap_max_r + 1) - obj_min_r
            else: # Object overlaps gap - behavior undefined? Assume skip or error. Let's skip.
                continue

        elif separation_axis == 'horizontal':
            # Determine if object is left or right of the gap and calculate horizontal shift
            if obj_max_c < gap_min_c: # Object is left of gap
                # Target right col of object is gap_min_c - 1
                delta_c = (gap_min_c - 1) - obj_max_c
            elif obj_min_c > gap_max_c: # Object is right of gap
                # Target left col of object is gap_max_c + 1
                delta_c = (gap_max_c + 1) - obj_min_c
            else: # Object overlaps gap - behavior undefined? Assume skip or error. Let's skip.
                continue

        # Apply the shift to each pixel of the object and paint it on the output grid
        for r, c in obj_coords:
            new_r, new_c = r + delta_r, c + delta_c
            # Check bounds before writing to output grid
            if 0 <= new_r < height and 0 <= new_c < width:
                output_grid[new_r, new_c] = 5
            # else: Pixel moves out of bounds - ignore it? This shouldn't happen if logic is correct for internal gaps.

    # --- 6. Return Result ---
    return output_grid.tolist()