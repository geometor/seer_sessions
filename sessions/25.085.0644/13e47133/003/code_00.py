import numpy as np
from collections import Counter, deque

"""
Transformation Rule:
1. Identify the background color (most frequent, excluding Red=2).
2. Identify the divider intersection point (h, v):
    - 'v' is the index of the first complete vertical Red column.
    - 'h' is the index of the first row where the horizontal Red segment starts at column 'v' (i.e., grid[h, v] == 2 and grid[h, v+1] == 2).
3. Identify initiator pixels (non-background, non-Red).
4. Create an output grid, initially a copy of the input.
5. Perform flood fill on the output grid starting from neighbors of each initiator pixel. Fill replaces background color with initiator color, stopping at Red, other colors, or grid edges.
6. Check if the Bottom-Left (BL) quadrant (rows >= h, cols < v) of the *input* grid contains any initiators.
7. If the input BL quadrant has no initiators, take the Top-Left (TL) quadrant (rows < h, cols < v) of the *output* grid, flip it vertically, and paste it into the BL quadrant of the *output* grid.
8. Return the final output grid.
"""

def find_background_color(grid, divider_color):
    """Finds the most frequent color excluding the divider color."""
    pixels = grid[grid != divider_color]
    if pixels.size == 0:
        # Default to 0 if only divider color exists or grid is empty,
        # though examples suggest a dominant background exists.
        return 0
    count = Counter(pixels)
    background_color = count.most_common(1)[0][0]
    return background_color

def find_dividing_intersection(grid, divider_color):
    """
    Finds the intersection point (h, v) defined by the vertical divider
    and the start of the horizontal divider segment.
    'v' is the index of the first full vertical divider column.
    'h' is the index of the first row where grid[h, v] and grid[h, v+1] are divider_color.
    Returns (h, v) or (None, None) if not found.
    """
    rows, cols = grid.shape
    v_idx = None
    h_idx = None

    # Find vertical divider index 'v' (first full column of divider_color)
    for c in range(cols):
        if np.all(grid[:, c] == divider_color):
            v_idx = c
            break

    if v_idx is None:
        # No full vertical divider found
        return None, None

    # Check if v_idx+1 is within bounds for horizontal check
    if v_idx + 1 >= cols:
        # Vertical divider is at the right edge, no horizontal segment possible from it
        return None, v_idx # Return v_idx but None for h

    # Find horizontal start row 'h'
    for r in range(rows):
        # Check if the cell at (r, v_idx) and the one to its right are the divider color
        if grid[r, v_idx] == divider_color and grid[r, v_idx + 1] == divider_color:
            h_idx = r
            break

    # h_idx might still be None if no horizontal segment starts at v_idx
    return h_idx, v_idx

def find_initiators(grid, background_color, divider_color):
    """Finds coordinates and colors of initiator pixels."""
    initiators = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            pixel_color = grid[r, c]
            if pixel_color != background_color and pixel_color != divider_color:
                initiators.append({'row': r, 'col': c, 'color': pixel_color})
    return initiators

def flood_fill(grid, start_r, start_c, fill_color, target_color, divider_color):
    """
    Performs flood fill on grid, starting from neighbors of (start_r, start_c),
    replacing target_color with fill_color. Stops at grid edges, divider_color,
    or any color that is not target_color. Modifies grid in place.
    """
    rows, cols = grid.shape
    q = deque()
    visited = set() # Tracks visited cells *for this specific fill operation*

    # Seed the queue with valid neighbors of the initiator location
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = start_r + dr, start_c + dc
        # Check bounds and if the neighbor is the target color
        if (0 <= nr < rows and 0 <= nc < cols and
                grid[nr, nc] == target_color):
            # Check visited *before* adding to queue
            if (nr, nc) not in visited:
                q.append((nr, nc))
                visited.add((nr, nc))

    # Process the queue
    while q:
        r, c = q.popleft()

        # Double check conditions for the current cell (r, c)
        # Should be target_color because we only added target_color cells
        if grid[r, c] == target_color:
            # Fill the cell
            grid[r, c] = fill_color

            # Check neighbors (4-directional)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Add neighbor to queue if valid, is target color, and not visited
                if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr, nc] == target_color and
                        (nr, nc) not in visited):
                    visited.add((nr, nc))
                    q.append((nr, nc))
        # If grid[r,c] is not target_color, it means another fill might have reached it first,
        # or it's a divider/initiator - either way, stop exploring from here.


def check_initiators_in_region(grid, r_start, r_end, c_start, c_end, background_color, divider_color):
    """Checks if any initiator pixels exist within the specified region [r_start:r_end, c_start:c_end]."""
    # Ensure bounds are valid before slicing/iterating
    r_end = min(r_end, grid.shape[0])
    c_end = min(c_end, grid.shape[1])
    r_start = max(r_start, 0)
    c_start = max(c_start, 0)

    if r_start >= r_end or c_start >= c_end:
        return False # Region is empty

    region = grid[r_start:r_end, c_start:c_end]
    
    # Check if any pixel in the region is neither background nor divider
    for r in range(region.shape[0]):
        for c in range(region.shape[1]):
            if region[r, c] != background_color and region[r, c] != divider_color:
                return True # Found an initiator
    return False # No initiators found

def transform(input_grid):
    """
    Applies flood fill from initiators and conditionally reflects the
    top-left quadrant to the bottom-left based on initiator presence
    in the input grid's bottom-left quadrant.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape
    divider_color = 2 # Red

    # --- Step 1 & 2: Identify Grid Elements & Intersection ---
    background_color = find_background_color(input_np, divider_color)
    h_intersect, v_intersect = find_dividing_intersection(input_np, divider_color)

    # Handle cases where intersection wasn't properly found (e.g., no full V divider)
    # Based on examples, we expect h and v to be found. If not, the logic breaks down.
    # Returning input might be safest default, but problem constraints likely guarantee intersection.
    if h_intersect is None or v_intersect is None:
         print(f"Warning: Could not find valid intersection point (h={h_intersect}, v={v_intersect}). Returning copy of input.")
         # Or raise an error, depending on expected behavior for invalid inputs.
         # For ARC, often best to return input copy if assumptions fail.
         return output_np.tolist()

    # --- Step 3: Identify Initiators ---
    initiators = find_initiators(input_np, background_color, divider_color)

    # --- Step 5: Perform Flood Fill ---
    # Apply flood fill from each initiator onto the output grid
    for init in initiators:
        r_init, c_init, color_init = init['row'], init['col'], init['color']
        # The flood fill modifies output_np in place
        flood_fill(output_np, r_init, c_init, color_init, background_color, divider_color)

    # --- Step 6, 7, 8, 9: Conditional Reflection ---
    # Define Bottom-Left quadrant bounds for input grid check
    bl_r_start, bl_r_end = h_intersect, rows
    bl_c_start, bl_c_end = 0, v_intersect

    # Check the INPUT grid's bottom-left region for initiators
    bottom_left_has_initiators = check_initiators_in_region(
        input_np, bl_r_start, bl_r_end, bl_c_start, bl_c_end, background_color, divider_color
    )

    if not bottom_left_has_initiators:
        # Define Top-Left quadrant bounds for output grid extraction
        tl_r_start, tl_r_end = 0, h_intersect
        tl_c_start, tl_c_end = 0, v_intersect

        # Check if TL region has valid dimensions before proceeding
        if tl_r_end > tl_r_start and tl_c_end > tl_c_start:
            # Extract the processed top-left region from the OUTPUT grid
            top_left_region = output_np[tl_r_start:tl_r_end, tl_c_start:tl_c_end]

            # Flip it vertically
            flipped_tl_region = np.flipud(top_left_region)

            # Define Bottom-Left quadrant bounds for output grid pasting
            # (Bounds are the same as the input check region)

            # Ensure dimensions match before pasting
            target_bl_shape = (bl_r_end - bl_r_start, bl_c_end - bl_c_start)
            if flipped_tl_region.shape == target_bl_shape:
                # Paste the flipped region into the bottom-left of the OUTPUT grid
                output_np[bl_r_start:bl_r_end, bl_c_start:bl_c_end] = flipped_tl_region
            else:
                # This case indicates an issue, maybe h_intersect or v_intersect was 0 or at boundary
                print(f"Warning: Shape mismatch during reflection. Flipped TL shape {flipped_tl_region.shape} vs Target BL shape {target_bl_shape}. Skipping reflection.")

    # --- Step 10: Return Result ---
    output_grid = output_np.tolist()
    return output_grid