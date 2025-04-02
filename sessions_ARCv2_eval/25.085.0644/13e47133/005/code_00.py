import numpy as np
from collections import Counter
import math

"""
Transformation Rule:
1.  **Identify Grid Structure:**
    *   Determine the background color (the most frequent color, excluding Red=2).
    *   Identify the Red (color 2) divider lines: find the index `v` of the first complete vertical Red column and the index `h` of the first row where the horizontal Red line segment begins at column `v`. This defines the intersection point `(h, v)`.
2.  **Identify Initiators:** Locate all pixels in the input grid whose color is neither the background color nor Red. Record their positions (row, col) and colors.
3.  **Perform Quadrant-Based Filling:**
    *   Create an output grid as a copy of the input grid.
    *   Define the four quadrants based on `h` and `v`: Top-Left (TL: `rows < h, cols < v`), Top-Right (TR: `rows < h, cols > v`), Bottom-Left (BL: `rows >= h, cols < v`), Bottom-Right (BR: `rows >= h, cols > v`).
    *   For each quadrant independently:
        *   Find all initiators located *within* that specific quadrant.
        *   For every pixel `(r, c)` *within* that quadrant that has the background color in the input grid:
            *   Calculate the Manhattan distance from `(r, c)` to every initiator *within the same quadrant*.
            *   Find the minimum distance.
            *   Identify all initiators within the quadrant at that minimum distance.
            *   Apply tie-breaking: select the initiator among the closest ones that has the lowest color index. If colors are tied, select the one with the lowest row index; if rows are tied, select the one with the lowest column index.
            *   Set the color of the pixel `(r, c)` in the *output grid* to the color of the selected initiator.
4.  **Conditional BL Quadrant Reflection:**
    *   Check the *input grid's* BL quadrant (rows `h` to end, columns `0` to `v-1`) to see if it contains any initiator pixels.
    *   **If** the input BL quadrant contains **no** initiator pixels:
        *   Define the TL region in the *output grid* (rows `0` to `h-1`, columns `0` to `v-1`) and the BL region in the *output grid* (rows `h` to end, columns `0` to `v-1`). Let their heights be `h_tl = h` and `h_bl = rows - h`.
        *   Determine the height `h_copy = min(h_tl, h_bl)`.
        *   If `h_copy > 0` and `v > 0` (i.e., TL region is not empty):
            *   Extract the bottom `h_copy` rows from the TL region of the output grid (`output_grid[h_tl - h_copy : h_tl, 0:v]`).
            *   Flip this extracted sub-grid vertically.
            *   Place the flipped sub-grid into the top `h_copy` rows of the BL region in the output grid (rows `h` to `h + h_copy - 1`).
            *   **If** the BL region is taller than the TL region (`h_bl > h_tl`):
                *   Take the row that was just placed at the top of the BL region (row `h` in the output grid).
                *   Fill all remaining rows in the BL region (from `h + h_copy` to the end) by repeating this row.
5.  **Return Output:** The modified output grid is the result.
"""

def find_background_color(grid, divider_color):
    """Finds the most frequent color excluding the divider color."""
    pixels = grid[grid != divider_color]
    if pixels.size == 0:
        # Default to 0 if only divider color exists or grid is empty
        return 0
    count = Counter(pixels)
    # Handle case where all non-divider pixels are unique - return lowest index?
    # Based on examples, seems there's always a dominant background.
    if not count:
         # If only divider color existed, pixels was empty. If grid only had one
         # other color, count will have one entry. If grid was empty, pixels was empty.
         # This case *shouldn't* be hit if there are non-divider pixels.
         # Fallback, though unlikely needed for this task based on examples.
         unique_colors = np.unique(grid[grid != divider_color])
         return unique_colors[0] if unique_colors.size > 0 else 0

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
        return None, None # No full vertical divider found

    # Check if v_idx+1 is within bounds for horizontal check
    if v_idx + 1 >= cols:
        # Vertical divider is at the right edge, no horizontal segment possible starting from it
        # Need to check if *any* horizontal segment exists. Let's search row by row.
        for r in range(rows):
            if np.any(grid[r, :] == divider_color) and grid[r, v_idx] == divider_color:
                 # Found a row with a divider segment that includes the vertical line
                 # Let's refine 'h' to be the *first* such row where grid[h,v-1] is also divider? No.
                 # Let's stick to the original definition: where horizontal segment *starts* at v
                 # If v+1 is out of bounds, this definition fails.
                 # Let's redefine h slightly: the first row index containing the horizontal divider segment.
                 is_horizontal_segment = False
                 for c_check in range(cols -1):
                     if grid[r, c_check] == divider_color and grid[r, c_check+1] == divider_color:
                         is_horizontal_segment = True
                         break
                 if is_horizontal_segment and grid[r, v_idx] == divider_color:
                     h_idx = r
                     break
        # If no horizontal segment found connected to v_idx, h_idx remains None.
        # But the original definition was grid[h,v]==2 AND grid[h,v+1]==2.
        # So if v+1 is out of bounds, h cannot be found by that definition.
        # Let's revert to the stricter interpretation based on the successful examples.
        return None, v_idx # Cannot find 'h' if v is at the right edge based on original definition.

    # Find horizontal start row 'h' using the original definition
    for r in range(rows):
        # Check if the cell at (r, v_idx) and the one to its right are the divider color
        if grid[r, v_idx] == divider_color and grid[r, v_idx + 1] == divider_color:
            h_idx = r
            break

    # h_idx might still be None if no horizontal segment starts *at* v_idx
    # If h_idx is None but v_idx was found, return v_idx but None for h
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

def manhattan_distance(r1, c1, r2, c2):
    """Calculates Manhattan distance between two points."""
    return abs(r1 - r2) + abs(c1 - c2)

def fill_quadrant_voronoi(grid, output_grid, bounds, all_initiators, bg_color):
    """Fills a quadrant based on closest initiator using Manhattan distance."""
    r_start, r_end, c_start, c_end = bounds
    rows, cols = grid.shape

    # Filter initiators to only those within this quadrant's bounds
    quadrant_initiators = [
        init for init in all_initiators
        if r_start <= init['row'] < r_end and c_start <= init['col'] < c_end
    ]

    if not quadrant_initiators:
        return # No initiators in this quadrant, nothing to fill

    # Iterate through each cell in the quadrant
    for r in range(r_start, r_end):
        for c in range(c_start, c_end):
            # Only fill background cells
            if grid[r, c] == bg_color:
                min_dist = math.inf
                closest_initiators_at_min_dist = []

                # Find distance to each initiator in this quadrant
                for init in quadrant_initiators:
                    dist = manhattan_distance(r, c, init['row'], init['col'])

                    if dist < min_dist:
                        min_dist = dist
                        closest_initiators_at_min_dist = [init]
                    elif dist == min_dist:
                        closest_initiators_at_min_dist.append(init)

                # Apply tie-breaking if necessary
                if len(closest_initiators_at_min_dist) > 1:
                    # Sort by color index, then row, then col
                    closest_initiators_at_min_dist.sort(key=lambda i: (i['color'], i['row'], i['col']))
                    winning_initiator = closest_initiators_at_min_dist[0]
                elif len(closest_initiators_at_min_dist) == 1:
                    winning_initiator = closest_initiators_at_min_dist[0]
                else:
                    # Should not happen if grid[r,c] is bg_color and quadrant_initiators is not empty
                    continue

                # Update the output grid
                output_grid[r, c] = winning_initiator['color']


def check_initiators_in_region(grid, r_start, r_end, c_start, c_end, background_color, divider_color):
    """Checks if any initiator pixels exist within the specified region [r_start:r_end, c_start:c_end]."""
    # Ensure bounds are valid before slicing/iterating
    rows, cols = grid.shape
    r_end = min(r_end, rows)
    c_end = min(c_end, cols)
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
    Applies Voronoi-like fill within quadrants based on Manhattan distance
    and conditionally reflects/repeats the top-left quadrant to the bottom-left.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape
    divider_color = 2 # Red

    # --- Step 1: Identify Grid Structure ---
    background_color = find_background_color(input_np, divider_color)
    h_intersect, v_intersect = find_dividing_intersection(input_np, divider_color)

    # Handle cases where intersection wasn't properly found
    if h_intersect is None or v_intersect is None:
         # Task constraints likely guarantee intersection, but good practice to handle
         print(f"Warning: Could not find valid intersection point (h={h_intersect}, v={v_intersect}). Returning copy of input.")
         return output_np.tolist()

    # --- Step 2: Identify Initiators ---
    initiators = find_initiators(input_np, background_color, divider_color)

    # --- Step 3: Perform Quadrant-Based Filling ---
    # Define quadrant bounds (exclusive for end row/col)
    tl_bounds = (0, h_intersect, 0, v_intersect)
    tr_bounds = (0, h_intersect, v_intersect + 1, cols)
    bl_bounds = (h_intersect, rows, 0, v_intersect) # Starts from row h
    br_bounds = (h_intersect, rows, v_intersect + 1, cols) # Starts from row h

    # Fill each quadrant
    fill_quadrant_voronoi(input_np, output_np, tl_bounds, initiators, background_color)
    fill_quadrant_voronoi(input_np, output_np, tr_bounds, initiators, background_color)
    fill_quadrant_voronoi(input_np, output_np, bl_bounds, initiators, background_color)
    fill_quadrant_voronoi(input_np, output_np, br_bounds, initiators, background_color)

    # --- Step 4: Conditional BL Quadrant Reflection ---
    # Define Bottom-Left quadrant bounds for input grid check (inclusive start, exclusive end)
    bl_check_r_start, bl_check_r_end = h_intersect, rows
    bl_check_c_start, bl_check_c_end = 0, v_intersect

    # Check the INPUT grid's bottom-left region for initiators
    bottom_left_has_initiators = check_initiators_in_region(
        input_np, bl_check_r_start, bl_check_r_end, bl_check_c_start, bl_check_c_end, background_color, divider_color
    )

    if not bottom_left_has_initiators:
        # Define TL and BL regions in the output grid
        h_tl = h_intersect
        w_tl = v_intersect
        h_bl = rows - h_intersect
        w_bl = v_intersect # Widths must match

        # Proceed only if TL region exists
        if h_tl > 0 and w_tl > 0:
            h_copy = min(h_tl, h_bl)

            # Extract the bottom h_copy rows from the filled TL quadrant
            sub_tl = output_np[h_tl - h_copy : h_tl, 0:w_tl]

            # Flip vertically
            flipped_sub_tl = np.flipud(sub_tl)

            # Paste into the top h_copy rows of the BL quadrant
            output_np[h_intersect : h_intersect + h_copy, 0:w_bl] = flipped_sub_tl

            # If BL is taller than TL, repeat the top row of the pasted section
            if h_bl > h_tl:
                # Ensure there are rows left to fill
                if h_intersect + h_copy < rows:
                    # Get the row that was just pasted at the top of BL (index h_intersect)
                    repeat_row = output_np[h_intersect, 0:w_bl]
                    # Fill remaining rows
                    for r_extra in range(h_intersect + h_copy, rows):
                        output_np[r_extra, 0:w_bl] = repeat_row
                # else: # h_bl > h_tl but h_intersect + h_copy == rows; should not happen if h_copy = h_tl < h_bl
                #    pass # No more rows to fill, just pasted up to the end


    # --- Step 5: Return Result ---
    output_grid = output_np.tolist()
    return output_grid