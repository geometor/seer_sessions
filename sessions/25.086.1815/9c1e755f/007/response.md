```python
"""
The transformation rule involves filling white (0) areas based on rules triggered by adjacent gray (5) segments. There are two distinct rules: one for horizontal gray segments and one for vertical gray segments.

1.  **Horizontal Propagation Rule:**
    a.  Identify all maximal horizontal segments of gray pixels (5).
    b.  For each segment located at row `r` spanning columns `c_start` to `c_end`:
        i.  Iterate through each column `c_source` from `c_start` to `c_end`.
        ii. Search vertically downwards starting from the pixel below the segment at `(r + 1, c_source)`.
        iii. For **every** pixel `(r_source, c_source)` found during this downward search that has a color `source_color` which is neither white (0) nor gray (5):
            1. Propagate this `source_color` horizontally to the right within its own row `r_source`.
            2. Iterate through target columns `c_target` from `c_source + 1` to `c_end`.
            3. If the pixel at `(r_source, c_target)` in the *output* grid is currently white (0), change its color to `source_color`.

2.  **Vertical Tiling Rule:**
    a.  Identify all maximal vertical segments of gray pixels (5).
    b.  For each segment located at column `c` spanning rows `r_top` to `r_bottom`:
        i.  Check the column immediately to the right (`c + 1`). Identify all "seed" pixels `(r_adj, c + 1)` within the segment's row bounds (`r_top <= r_adj <= r_bottom`) that are neither white (0) nor gray (5).
        ii. If seed pixels are found:
            1.  Determine the connected component of non-white, non-gray pixels containing these seeds, constrained to rows `r_top` to `r_bottom` and columns `c + 1` onwards.
            2.  Find the bounding box `(r_source_top, r_source_bottom, c_source_left, c_source_right)` of this component (this defines the "pattern block").
            3.  If a valid pattern block exists (height > 0):
                a.  Calculate the pattern height: `H_pattern = r_source_bottom - r_source_top + 1`.
                b.  Iterate upwards through target rows `r_target` from `r_source_top - 1` down to `r_top`.
                c.  For each `r_target`, calculate the corresponding source row `r_source` within the pattern block using modulo arithmetic: `relative_target_row = r_source_top - 1 - r_target`; `relative_source_row = (H_pattern - 1) - (relative_target_row % H_pattern)`; `r_source = r_source_top + relative_source_row`.
                d.  Iterate through target columns `c_target` from `c_source_left` to `c_source_right`.
                e.  If the pixel at `(r_target, c_target)` in the *output* grid is currently white (0):
                    i.  Get the color `source_color` from the *input* grid at `(r_source, c_target)`.
                    ii. If `source_color` is neither white (0) nor gray (5), change the color of the output pixel `(r_target, c_target)` to `source_color`.
"""

import numpy as np
from collections import deque

def find_connected_component_bbox(grid, seed_points, r_min_bound, r_max_bound, c_min_bound):
    """
    Finds the bounding box of the connected component of non-white, non-gray pixels
    containing the seed points, constrained by row and column bounds. Uses BFS.
    Returns (min_r, max_r, min_c, max_c) or None if no valid component.
    """
    if not seed_points:
        return None

    H, W = grid.shape
    q = deque()
    visited = set()
    component_points = set()

    # Initial validation and queue setup
    for r, c in seed_points:
        # Basic check: seed must be non-white/non-gray and within grid
        if not (0 <= r < H and 0 <= c < W) or grid[r, c] == 0 or grid[r, c] == 5:
             continue
        # Check if seed meets the specific task constraints
        if r_min_bound <= r <= r_max_bound and c >= c_min_bound:
            if (r, c) not in visited:
                q.append((r, c))
                visited.add((r, c))
                component_points.add((r, c))

    if not q: # No valid seeds found
        return None

    while q:
        r, c = q.popleft()

        # Explore neighbors (4-way adjacency)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check grid bounds
            if not (0 <= nr < H and 0 <= nc < W):
                continue

            # Check task-specific bounds for component growth
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

    # Add check to ensure bbox reflects actual component points within bounds
    # Although BFS should handle this, double-checking
    if min_r < r_min_bound or max_r > r_max_bound or min_c < c_min_bound:
         # This case shouldn't happen if BFS constraints are correct, but good safety check
         print(f"Warning: BBox {min_r, max_r, min_c, max_c} exceeds bounds {r_min_bound, r_max_bound, c_min_bound}. Seed points: {seed_points}")
         # Recalculate bbox strictly within bounds if necessary, or return None if empty
         filtered_points = {(r, c) for r, c in component_points if r_min_bound <= r <= r_max_bound and c >= c_min_bound}
         if not filtered_points: return None
         min_r = min(r for r, c in filtered_points)
         max_r = max(r for r, c in filtered_points)
         min_c = min(c for r, c in filtered_points)
         max_c = max(c for r, c in filtered_points)


    return min_r, max_r, min_c, max_c


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    H, W = input_np.shape

    # --- Horizontal Propagation Rule ---
    processed_horizontal_pixels = set() # Track gray pixels already part of a processed segment
    for r in range(H):
        for c in range(W):
            # Check if this pixel is gray (5) and hasn't been processed as part of a horizontal segment yet
            if input_np[r, c] == 5 and (r, c) not in processed_horizontal_pixels:
                c_start = c
                c_end = c
                # Find the full horizontal extent of the gray segment
                while c_end + 1 < W and input_np[r, c_end + 1] == 5:
                    c_end += 1

                # Mark all pixels in this segment as processed to avoid redundant checks
                for k in range(c_start, c_end + 1):
                    processed_horizontal_pixels.add((r, k))

                # Apply the propagation rule for this segment
                # Iterate through each column covered by the gray segment
                for c_source_col in range(c_start, c_end + 1):
                    # Search downwards from below the segment in this specific column
                    for r_source_row in range(r + 1, H):
                        source_color = input_np[r_source_row, c_source_col]
                        # Check if it's a valid source color (neither white 0 nor gray 5)
                        if source_color != 0 and source_color != 5:
                            # Propagate this color horizontally to the right within its own row (r_source_row)
                            # Iterate through target columns from the next column over up to the end of the gray segment
                            for c_fill in range(c_source_col + 1, c_end + 1):
                                # Only fill if the target pixel in the output grid is currently white (0)
                                if output_np[r_source_row, c_fill] == 0:
                                    output_np[r_source_row, c_fill] = source_color
                            # **Removed the 'break' statement here**
                            # Continue searching downwards in the same column (c_source_col) for more source colors


    # --- Vertical Tiling Rule ---
    processed_vertical_pixels = set() # Track gray pixels already part of a processed segment
    for c in range(W):
        for r in range(H):
            # Check if this pixel is gray (5) and hasn't been processed as part of a vertical segment yet
            if input_np[r, c] == 5 and (r, c) not in processed_vertical_pixels:
                r_top = r
                r_bottom = r
                # Find the full vertical extent of the gray segment
                while r_bottom + 1 < H and input_np[r_bottom + 1, c] == 5:
                    r_bottom += 1

                # Mark all pixels in this segment as processed to avoid redundant checks
                for k in range(r_top, r_bottom + 1):
                    processed_vertical_pixels.add((k, c))

                # Check the column immediately to the right for source pattern seeds
                c_adj_col = c + 1
                if c_adj_col < W:
                    seed_points = []
                    # Find seeds adjacent to the segment (within row bounds) in the column to the right
                    for r_adj in range(r_top, r_bottom + 1):
                        # Check pixel is non-white (0) and non-gray (5)
                        if input_np[r_adj, c_adj_col] != 0 and input_np[r_adj, c_adj_col] != 5:
                            seed_points.append((r_adj, c_adj_col))

                    # If no seed points were found, continue to the next gray segment
                    if not seed_points:
                        continue

                    # Find the bounding box of the connected component starting from the seeds
                    # Component search is constrained: rows r_top to r_bottom, columns c_adj_col onwards
                    bbox = find_connected_component_bbox(input_np, seed_points, r_top, r_bottom, c_adj_col)

                    # If no valid component/bbox found, continue to the next gray segment
                    if bbox is None:
                        continue

                    r_source_top, r_source_bottom, c_source_left, c_source_right = bbox
                    pattern_height = r_source_bottom - r_source_top + 1

                    # Ensure pattern has a positive height
                    if pattern_height <= 0:
                        continue

                    # Perform vertical tiling upwards from the pattern block
                    # Iterate target rows upwards: from row just above the pattern (r_source_top - 1)
                    # up to the top influence row (r_top)
                    for r_target in range(r_source_top - 1, r_top - 1, -1):
                        # Calculate corresponding source row within the pattern using modulo arithmetic
                        # relative_target_row counts how many rows above the pattern we are (0, 1, 2...)
                        relative_target_row = r_source_top - 1 - r_target
                        # relative_source_row cycles from bottom (H_pattern - 1) up to top (0) of the pattern block
                        relative_source_row = (pattern_height - 1) - (relative_target_row % pattern_height)
                        # Calculate the absolute source row index
                        r_source = r_source_top + relative_source_row

                        # Fill the target row based on the corresponding source row pattern
                        # Iterate through columns defined by the pattern's bounding box
                        for c_target in range(c_source_left, c_source_right + 1):
                             # Safety check for target bounds (although r_target should be okay)
                            if not (0 <= r_target < H and 0 <= c_target < W):
                                continue
                            # Only fill if the target pixel in the output grid is currently white (0)
                            if output_np[r_target, c_target] == 0:
                                # Safety check for source bounds (although r_source/c_target should be okay)
                                if not (r_source_top <= r_source <= r_source_bottom and c_source_left <= c_target <= c_source_right):
                                     continue
                                # Get the color from the *input* grid's pattern block
                                source_color = input_np[r_source, c_target]
                                # Ensure we only copy non-white (0) and non-gray (5) colors from the pattern
                                if source_color != 0 and source_color != 5:
                                     output_np[r_target, c_target] = source_color


    # Convert the final numpy array back to a list of lists for the required output format
    output_list = output_np.tolist()
    return output_list
```