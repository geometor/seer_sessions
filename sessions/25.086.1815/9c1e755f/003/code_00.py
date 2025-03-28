import numpy as np
from collections import deque

"""
The transformation rule involves identifying horizontal and vertical segments of gray pixels (color 5). These segments trigger color propagation into adjacent white space (color 0).

1.  **Horizontal Propagation:**
    - Find all maximal horizontal gray segments.
    - For each segment (at row `r`, columns `c_start` to `c_end`):
    - Check the row below (`r + 1`).
    - For each column `c_source` from `c_start` to `c_end`:
        - If the pixel `input[r + 1, c_source]` has a color (not 0/white, not 5/gray):
            - Propagate this `source_color` rightwards from `(r + 1, c_source + 1)` to `(r + 1, c_end)`.
            - Fill only pixels in the `output` grid that are currently white (0).

2.  **Vertical Propagation:**
    - Find all maximal vertical gray segments.
    - For each segment (at column `c`, rows `r_top` to `r_bottom`):
    - Check the column to the right (`c + 1`) within the segment's row bounds (`r_top` to `r_bottom`).
    - Identify seed pixels (not 0/white, not 5/gray) at `(r_adj, c + 1)`.
    - If seeds exist, find the bounding box of the connected component formed by these seeds and other adjacent non-white/non-gray pixels, constrained by the segment's row bounds (`r_top` to `r_bottom`) and columns `c + 1` onwards.
    - If a valid pattern block is found (bbox: `r_source_top` to `r_source_bottom`, `c_source_left` to `c_source_right`):
        - Tile this pattern (from the `input` grid) vertically upwards, starting from row `r_source_top - 1` up to `r_top`.
        - Use modulo arithmetic based on the pattern height to determine the source row for each target row.
        - Fill only pixels in the `output` grid that are currently white (0) within the pattern's column bounds (`c_source_left` to `c_source_right`).
"""

def find_connected_component_bbox(grid, seed_points, r_min_bound, r_max_bound, c_min_bound):
    """
    Finds the bounding box of the connected component of non-white, non-gray pixels
    containing the seed points, constrained by row and column bounds. Uses BFS.
    Returns (min_r, max_r, min_c, max_c) or None if no valid component.
    """
    if not seed_points:
        return None

    H, W = grid.shape
    q = deque(seed_points)
    visited = set(seed_points)
    component_points = set(seed_points)

    # Initial component points must satisfy bounds
    for r, c in list(seed_points): # Use list copy for safe removal
        if not (r_min_bound <= r <= r_max_bound and c >= c_min_bound):
             # This check might be redundant if seeds are chosen carefully,
             # but adds safety. BFS neighbours check below is primary filter.
             seed_points.remove((r,c))
             visited.remove((r,c))
             component_points.remove((r,c))

    if not seed_points: # Check again if initial seeds were out of bounds
        return None

    # Reset queue and visited with filtered seeds
    q = deque(seed_points)
    visited = set(seed_points)

    while q:
        r, c = q.popleft()

        # Explore neighbors (4-way adjacency)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check grid bounds
            if not (0 <= nr < H and 0 <= nc < W):
                continue

            # Check task-specific bounds for component growth
            # Component must stay within vertical segment's row influence
            # and to the right of the segment's adjacent column.
            if not (r_min_bound <= nr <= r_max_bound and nc >= c_min_bound):
                continue

            # Check if neighbor is part of the component (non-white, non-gray)
            if grid[nr, nc] == 0 or grid[nr, nc] == 5:
                continue

            # Check if visited
            if (nr, nc) in visited:
                continue

            # Add valid neighbor to queue, visited set, and component points
            visited.add((nr, nc))
            q.append((nr, nc))
            component_points.add((nr, nc))

    # Compute exact bbox from all component points found
    if not component_points:
        return None

    min_r = min(r for r, c in component_points)
    max_r = max(r for r, c in component_points)
    min_c = min(c for r, c in component_points)
    max_c = max(c for r, c in component_points)

    return min_r, max_r, min_c, max_c


def transform(input_grid):
    """
    Applies the propagation rules based on gray segments and adjacent patterns.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    H, W = input_np.shape

    # --- Horizontal Propagation ---
    processed_horizontal_pixels = set() # Track gray pixels already part of a processed segment
    for r in range(H):
        for c in range(W):
            # Check if this pixel is gray and hasn't been processed as part of a segment yet
            if input_np[r, c] == 5 and (r, c) not in processed_horizontal_pixels:
                c_start = c
                c_end = c
                # Find the end of the horizontal segment
                while c_end + 1 < W and input_np[r, c_end + 1] == 5:
                    c_end += 1

                # Mark all pixels in this segment as processed
                for k in range(c_start, c_end + 1):
                    processed_horizontal_pixels.add((r, k))

                # Check row below for source pixels, if it exists
                r_source_row = r + 1
                if r_source_row < H:
                    # Iterate through EACH column below the segment
                    for c_source in range(c_start, c_end + 1):
                        source_color = input_np[r_source_row, c_source]
                        # Check if it's a valid source color (non-white, non-gray)
                        if source_color != 0 and source_color != 5:
                            # Propagate this specific color horizontally to the right
                            # starting from the position right next to the source
                            for c_fill in range(c_source + 1, c_end + 1):
                                # Only fill if the target pixel in the output is white
                                if output_np[r_source_row, c_fill] == 0:
                                    output_np[r_source_row, c_fill] = source_color
                                # We don't break here; continue checking other white cells
                                # This allows different source colors under the same bar
                                # to fill their respective areas.


    # --- Vertical Propagation ---
    processed_vertical_pixels = set() # Track gray pixels already part of a processed segment
    for c in range(W):
        for r in range(H):
            # Check if this pixel is gray and hasn't been processed as part of a segment yet
            if input_np[r, c] == 5 and (r, c) not in processed_vertical_pixels:
                r_top = r
                r_bottom = r
                # Find the end of the vertical segment
                while r_bottom + 1 < H and input_np[r_bottom + 1, c] == 5:
                    r_bottom += 1

                # Mark all pixels in this segment as processed
                for k in range(r_top, r_bottom + 1):
                    processed_vertical_pixels.add((k, c))

                # Check column to the right for source pattern seeds
                c_adj_col = c + 1
                if c_adj_col < W:
                    seed_points = []
                    # Find seeds adjacent to the segment in the column to the right
                    for r_adj in range(r_top, r_bottom + 1):
                        if input_np[r_adj, c_adj_col] != 0 and input_np[r_adj, c_adj_col] != 5:
                            # Ensure seed is within grid bounds (already checked by r_adj loop and c_adj_col<W)
                            seed_points.append((r_adj, c_adj_col))

                    if not seed_points:
                        continue # No adjacent pattern found for this segment

                    # Find the bounding box of the connected component starting from the seeds
                    # Bounding the search: rows r_top to r_bottom, columns c_adj_col onwards
                    bbox = find_connected_component_bbox(input_np, seed_points, r_top, r_bottom, c_adj_col)

                    if bbox is None:
                        continue # No valid component found

                    r_source_top, r_source_bottom, c_source_left, c_source_right = bbox
                    pattern_height = r_source_bottom - r_source_top + 1

                    if pattern_height <= 0:
                        continue # Invalid pattern height

                    # Perform vertical tiling upwards
                    # Iterate target rows upwards from just above the pattern up to the top of the gray segment influence
                    for r_target in range(r_source_top - 1, r_top - 1, -1):
                        # Calculate corresponding source row using modulo arithmetic
                        # Source row index relative to the start of the pattern block
                        relative_target_row = r_source_top - 1 - r_target # 0 for row just above, 1 for row above that, etc.
                        relative_source_row = (pattern_height - 1) - (relative_target_row % pattern_height) # Cycles from bottom (h-1) to top (0)
                        r_source = r_source_top + relative_source_row

                        # Fill the target row based on the source row pattern
                        for c_target in range(c_source_left, c_source_right + 1):
                            # Only fill if the target pixel in the output is white
                            if output_np[r_target, c_target] == 0:
                                source_color = input_np[r_source, c_target]
                                # Ensure we only copy non-white/non-gray from pattern block
                                if source_color != 0 and source_color != 5:
                                     output_np[r_target, c_target] = source_color


    # Convert back to list of lists for the required output format
    output_list = output_np.tolist()
    return output_list