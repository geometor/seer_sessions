```python
import numpy as np
from collections import Counter, deque

"""
Transforms the input grid by finding specific 3x3 patterns ("stamps") and using them to flood-fill adjacent areas.

1.  **Analyze Input:**
    *   Determine the background color (C_bg) by finding the most frequent color in the input grid.

2.  **Find Stamps:**
    *   Scan the input grid for 3x3 subgrids.
    *   A valid "stamp" is a 3x3 subgrid with:
        *   A uniform border color (C_frame).
        *   A single center pixel color (C_center).
        *   The border color C_frame must *not* be the background color C_bg.
    *   Store each found stamp's 3x3 grid, its center color (C_center), frame color (C_frame), and its top-left position (r_stamp, c_stamp).

3.  **Identify Target Regions and Apply Stamp Pattern (Flood Fill & Tiling):**
    *   Initialize the output grid as a copy of the input grid.
    *   Keep track of pixels that have been modified globally using a set `modified_pixels`.
    *   For each identified stamp S located at (r_stamp, c_stamp) with center color C_center and its 3x3 pattern `stamp_grid`:
        *   Identify the coordinates occupied by the stamp itself: `stamp_coords`.
        *   Find initial "seed" pixels: These are pixels directly adjacent (8-connectivity) to `stamp_coords`.
        *   Filter seeds: Keep only seed pixels (r, c) where the color `input_grid[r, c]` is either the background color (C_bg) OR the stamp's center color (C_center).
        *   Perform a flood fill (BFS) starting from these filtered seed pixels:
            *   Use a queue and a `visited_fill` set (specific to this stamp's fill) to manage the search.
            *   The fill expands to adjacent pixels (nr, nc) if:
                *   (nr, nc) is within grid bounds.
                *   (nr, nc) has not been visited *during this specific fill*.
                *   The color `input_grid[nr, nc]` is either C_bg OR C_center.
            *   Collect all pixels visited during the flood fill into a set `region_to_fill`.
        *   Apply the stamp pattern to the `region_to_fill`:
            *   Iterate through each pixel coordinate (r, c) in `region_to_fill`.
            *   Check if (r, c) is already in the global `modified_pixels` set. If yes, skip (first modification wins).
            *   Calculate the corresponding indices within the stamp's 3x3 grid using modulo arithmetic relative to the stamp's top-left corner:
                *   `stamp_r_idx = (r - r_stamp) % 3`
                *   `stamp_c_idx = (c - c_stamp) % 3`
            *   Update the `output_grid` at position (r, c) with the color from the stamp's pattern: `output_grid[r, c] = stamp_grid[stamp_r_idx, stamp_c_idx]`.
            *   Add the coordinate (r, c) to the global `modified_pixels` set.

4.  **Finalize:**
    *   Return the `output_grid`. Pixels not part of any filled region remain unchanged from their original input color.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    if not colors.size:
        return 0 # Default for empty grid
    return colors[np.argmax(counts)]

def find_stamps(grid, background_color):
    """
    Finds 3x3 stamp patterns with a uniform border color different from the background.
    Returns a list of dictionaries, each containing stamp info.
    """
    stamps_info = []
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            frame_color = subgrid[0, 0]
            
            # Check if frame color is the background
            if frame_color == background_color:
                continue

            # Check for uniform border more robustly
            border_coords = [
                (0, 0), (0, 1), (0, 2),
                (1, 0),         (1, 2),
                (2, 0), (2, 1), (2, 2)
            ]
            is_uniform_border = all(subgrid[br, bc] == frame_color for br, bc in border_coords)

            if is_uniform_border:
                center_color = subgrid[1, 1]
                stamps_info.append({
                    'grid': subgrid.copy(),
                    'frame_color': frame_color,
                    'center_color': center_color,
                    'row': r,
                    'col': c
                })
    return stamps_info

def flood_fill_region(grid, start_coords, fill_colors, stamp_coords):
    """
    Performs a flood fill (BFS) starting from start_coords.
    Fills regions where pixels have one of the fill_colors.
    Does not fill pixels within the stamp_coords itself.
    Returns the set of coordinates belonging to the filled region.
    """
    height, width = grid.shape
    q = deque(list(start_coords)) # Use list to ensure iteration order if needed, though set is fine for queue
    visited_fill = set(start_coords)
    region_coords = set(start_coords)

    while q:
        r, c = q.popleft()

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc

                # Check bounds
                if not (0 <= nr < height and 0 <= nc < width):
                    continue
                
                neighbor_coord = (nr, nc)

                # Check if already visited in this fill or part of the stamp
                if neighbor_coord in visited_fill or neighbor_coord in stamp_coords:
                    continue

                # Check if neighbor has a valid fill color
                if grid[nr, nc] in fill_colors:
                    visited_fill.add(neighbor_coord)
                    q.append(neighbor_coord)
                    region_coords.add(neighbor_coord)

    return region_coords


def get_adjacent_pixels(grid_shape, coords_set):
    """
    Finds all unique pixels adjacent (8-connectivity) to any pixel in coords_set,
    excluding pixels within coords_set itself. Used to find initial seeds.
    """
    height, width = grid_shape
    adjacent = set()
    for r_orig, c_orig in coords_set:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r_orig + dr, c_orig + dc
                # Check bounds
                if 0 <= nr < height and 0 <= nc < width:
                    neighbor_coord = (nr, nc)
                    # Add if not part of the original set
                    if neighbor_coord not in coords_set:
                        adjacent.add(neighbor_coord)
    return adjacent

def transform(input_grid):
    """
    Applies the stamp-based flood fill and tiling transformation.
    """
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)
    
    # 1. Analyze Input: Find background color
    background_color = find_background_color(input_grid)

    # 2. Find Stamps
    stamps = find_stamps(input_grid, background_color)

    # 3. Identify Target Regions and Apply Stamp Pattern
    modified_pixels = set() # Track globally modified pixels

    for stamp in stamps:
        stamp_grid = stamp['grid']
        stamp_center_color = stamp['center_color']
        r_stamp, c_stamp = stamp['row'], stamp['col']

        # Define the stamp's own coordinates
        stamp_coords = set()
        for r_offset in range(3):
            for c_offset in range(3):
                 stamp_coords.add((r_stamp + r_offset, c_stamp + c_offset))

        # Define the colors that can be filled by this stamp
        fillable_colors = {background_color, stamp_center_color}

        # Find initial seed pixels adjacent to the stamp
        initial_adjacent = get_adjacent_pixels((height, width), stamp_coords)

        # Filter seeds: must be a fillable color and not already modified
        seed_pixels = set()
        for r, c in initial_adjacent:
            # Check if the pixel has a fillable color in the *original* grid
            # And ensure it wasn't modified by a *previous* stamp's fill
            if input_grid[r, c] in fillable_colors and (r, c) not in modified_pixels:
                 seed_pixels.add((r, c))
        
        # If no valid seeds, continue to the next stamp
        if not seed_pixels:
            continue

        # Perform flood fill starting from seed pixels
        # The fill propagates based on original grid colors, ignoring the stamp area itself
        region_to_fill = flood_fill_region(input_grid, seed_pixels, fillable_colors, stamp_coords)
        
        # Apply tiling to the identified region
        for r, c in region_to_fill:
            # Check if already modified by another stamp (first modification wins)
            if (r, c) not in modified_pixels:
                # Calculate stamp indices using modulo relative to stamp's top-left
                stamp_r_idx = (r - r_stamp) % 3
                stamp_c_idx = (c - c_stamp) % 3

                # Update the output grid
                output_grid[r, c] = stamp_grid[stamp_r_idx, stamp_c_idx]
                modified_pixels.add((r, c)) # Mark pixel as globally modified

    # 4. Finalize
    return output_grid
```