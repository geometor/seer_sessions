import numpy as np
from collections import deque

"""
The transformation rule involves identifying horizontal and vertical segments of gray pixels (color 5).
These gray segments act as triggers and boundaries for propagating adjacent colored patterns (non-white 0, non-gray 5) into adjacent white space (color 0).

1.  **Horizontal Propagation:** If a non-white, non-gray pixel exists immediately below a horizontal gray segment, its color is propagated horizontally to the right, filling any white pixels in the same row, up to the end column of the gray segment above it.

2.  **Vertical Propagation:** If a pattern (a connected block of non-white, non-gray pixels) exists immediately to the right of a vertical gray segment, this pattern block is tiled/repeated vertically upwards, filling white space in the same columns, up to the top row of the gray segment. The tiling repeats the source pattern block cyclically from bottom to top.

The process involves:
- Finding all maximal gray segments (horizontal and vertical).
- For each segment, finding the adjacent source pattern (if any).
- Applying the corresponding propagation rule (horizontal fill or vertical tiling) to modify a copy of the input grid.
"""

def find_connected_component_bbox(grid, seed_points, r_min_bound, r_max_bound, c_min_bound):
    """
    Finds the bounding box of the connected component of non-white, non-gray pixels
    containing the seed points, constrained by row and column bounds. Uses BFS.
    """
    if not seed_points:
        return None

    H, W = grid.shape
    q = deque(seed_points)
    visited = set(seed_points)
    component_points = set(seed_points)

    min_r, max_r = float('inf'), float('-inf')
    min_c, max_c = float('inf'), float('-inf')

    for r, c in seed_points:
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)

    while q:
        r, c = q.popleft()

        # Update bounding box based on component points found so far
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)

        # Explore neighbors (4-way adjacency)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check grid bounds
            if not (0 <= nr < H and 0 <= nc < W):
                continue

            # Check task-specific bounds
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

    # Recompute exact bbox from all component points found
    if not component_points:
        return None # Should not happen if seed_points is not empty

    final_min_r = min(r for r, c in component_points)
    final_max_r = max(r for r, c in component_points)
    final_min_c = min(c for r, c in component_points)
    final_max_c = max(c for r, c in component_points)

    return final_min_r, final_max_r, final_min_c, final_max_c


def transform(input_grid):
    """
    Applies the propagation rules based on gray segments and adjacent patterns.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    H, W = input_np.shape

    # --- Horizontal Propagation ---
    processed_horizontal_starts = set()
    for r in range(H):
        for c in range(W):
            if (r, c) in processed_horizontal_starts:
                continue
            # Found potential start of a horizontal gray segment
            if input_np[r, c] == 5:
                c_start = c
                c_end = c
                # Find the end of the horizontal segment
                while c_end + 1 < W and input_np[r, c_end + 1] == 5:
                    c_end += 1

                # Mark all pixels in this segment as processed for starting horizontal checks
                for k in range(c_start, c_end + 1):
                    processed_horizontal_starts.add((r, k))

                # Check row below for source pixels
                r_source_row = r + 1
                if r_source_row < H:
                    for c_source in range(c_start, c_end + 1):
                        source_color = input_np[r_source_row, c_source]
                        # Check if it's a valid source color (non-white, non-gray)
                        if source_color != 0 and source_color != 5:
                            # Propagate horizontally to the right within bounds
                            for c_fill in range(c_source + 1, c_end + 1):
                                # Only fill if the target pixel is white
                                if output_np[r_source_row, c_fill] == 0:
                                    output_np[r_source_row, c_fill] = source_color
                                # Stop propagation in this row if we hit a non-white pixel
                                elif output_np[r_source_row, c_fill] != source_color:
                                     # This behavior (stopping) isn't explicitly shown but seems safer
                                     # than overwriting existing colors. Let's stick to only filling white (0).
                                     pass # Keep the original logic, only fill 0s.


    # --- Vertical Propagation ---
    processed_vertical_starts = set()
    for c in range(W):
        for r in range(H):
            if (r, c) in processed_vertical_starts:
                continue
            # Found potential start of a vertical gray segment
            if input_np[r, c] == 5:
                r_top = r
                r_bottom = r
                # Find the end of the vertical segment
                while r_bottom + 1 < H and input_np[r_bottom + 1, c] == 5:
                    r_bottom += 1

                # Mark all pixels in this segment as processed for starting vertical checks
                for k in range(r_top, r_bottom + 1):
                    processed_vertical_starts.add((k, c))

                # Check column to the right for source pattern seeds
                c_adj_col = c + 1
                if c_adj_col < W:
                    seed_points = []
                    for r_adj in range(r_top, r_bottom + 1):
                        if input_np[r_adj, c_adj_col] != 0 and input_np[r_adj, c_adj_col] != 5:
                            seed_points.append((r_adj, c_adj_col))

                    if not seed_points:
                        continue # No adjacent pattern found for this segment

                    # Find the bounding box of the connected component starting from the seeds
                    bbox = find_connected_component_bbox(input_np, seed_points, r_top, r_bottom, c_adj_col)

                    if bbox is None:
                        continue # No valid component found

                    r_source_top, r_source_bottom, c_source_left, c_source_right = bbox
                    pattern_height = r_source_bottom - r_source_top + 1

                    if pattern_height <= 0:
                        continue # Invalid pattern height

                    # Perform vertical tiling upwards
                    for r_target in range(r_source_top - 1, r_top - 1, -1): # Iterate target rows upwards (r_source_top-1 down to r_top)
                        # Calculate corresponding source row using modulo arithmetic
                        # We want to map r_target to a row within [r_source_top, r_source_bottom]
                        # The pattern repeats every pattern_height rows.
                        # The row r_source_bottom should map to r_source_bottom - pattern_height, etc.
                        # r_source = r_source_bottom - (distance_from_bottom % pattern_height)
                        distance_from_r_source_bottom = r_source_bottom - r_target
                        r_source = r_source_bottom - (distance_from_r_source_bottom % pattern_height)

                        # Fill the target row based on the source row pattern
                        for c_target in range(c_source_left, c_source_right + 1):
                            # Only fill if the target pixel is white
                            if output_np[r_target, c_target] == 0:
                                source_color = input_np[r_source, c_target]
                                # Ensure we only copy non-white/non-gray from pattern block in case bbox included some zeros/grays unexpectedly
                                if source_color != 0 and source_color != 5:
                                     output_np[r_target, c_target] = source_color


    # Convert back to list of lists for the required output format
    output_list = output_np.tolist()
    return output_list