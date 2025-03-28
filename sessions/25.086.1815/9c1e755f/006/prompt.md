
Previous Code:
```python
"""
The transformation rule involves filling white (0) areas based on rules triggered by adjacent gray (5) segments. There are two distinct rules: one for horizontal gray segments and one for vertical gray segments.

1.  **Horizontal Propagation Rule:**
    a.  Identify all maximal horizontal segments of gray pixels (5).
    b.  For each segment located at row `r` spanning columns `c_start` to `c_end`:
        i.  Iterate through each column `c_source` from `c_start` to `c_end`.
        ii. Search vertically downwards starting from the pixel below the segment at `(r + 1, c_source)`. Find the *first* pixel `(r_source, c_source)` that is neither white (0) nor gray (5).
        iii. If such a source pixel is found with color `source_color`:
            1. Propagate `source_color` horizontally to the right within row `r_source`.
            2. Iterate through target columns `c_target` from `c_source + 1` to `c_end`.
            3. If the pixel at `(r_source, c_target)` in the *output* grid is currently white (0), change its color to `source_color`.
            4. **Stop** searching further down in column `c_source` for this horizontal segment (use `break` after finding the first source in the downward search).

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

    return min_r, max_r, min_c, max_c


def transform(input_grid):
    """
    Applies the propagation and tiling rules based on gray segments.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    H, W = input_np.shape

    # --- Horizontal Propagation ---
    processed_horizontal_pixels = set() # Track gray pixels already part of a processed segment
    for r in range(H):
        for c in range(W):
            # Check if this pixel is gray and hasn't been processed
            if input_np[r, c] == 5 and (r, c) not in processed_horizontal_pixels:
                c_start = c
                c_end = c
                # Find the end of the horizontal segment
                while c_end + 1 < W and input_np[r, c_end + 1] == 5:
                    c_end += 1

                # Mark all pixels in this segment as processed
                for k in range(c_start, c_end + 1):
                    processed_horizontal_pixels.add((r, k))

                # Apply the propagation rule for this segment
                for c_source_col in range(c_start, c_end + 1):
                    # Search downwards from below the segment in this column
                    for r_source_row in range(r + 1, H):
                        source_color = input_np[r_source_row, c_source_col]
                        # Check if it's a valid source color (non-white, non-gray)
                        if source_color != 0 and source_color != 5:
                            # Propagate this color horizontally to the right in its own row
                            for c_fill in range(c_source_col + 1, c_end + 1):
                                # Only fill if the target pixel in the output is white
                                if output_np[r_source_row, c_fill] == 0:
                                    output_np[r_source_row, c_fill] = source_color
                            # Found the first source in this column, stop searching downwards
                            break
                    # Continue to the next column under the segment


    # --- Vertical Propagation ---
    processed_vertical_pixels = set() # Track gray pixels already part of a processed segment
    for c in range(W):
        for r in range(H):
            # Check if this pixel is gray and hasn't been processed
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
                        # Check grid bounds (r_adj is implicitly checked by loop)
                        if input_np[r_adj, c_adj_col] != 0 and input_np[r_adj, c_adj_col] != 5:
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
                        relative_target_row = r_source_top - 1 - r_target # 0 for row just above, 1 for row above that, etc.
                        relative_source_row = (pattern_height - 1) - (relative_target_row % pattern_height) # Cycles from bottom (h-1) to top (0)
                        r_source = r_source_top + relative_source_row

                        # Fill the target row based on the source row pattern
                        for c_target in range(c_source_left, c_source_right + 1):
                             # Check target bounds (should be fine, but safety check)
                            if not (0 <= r_target < H and 0 <= c_target < W):
                                continue
                            # Only fill if the target pixel in the output is white
                            if output_np[r_target, c_target] == 0:
                                # Check source bounds (should be fine due to bbox/modulo, but safety)
                                if not (r_source_top <= r_source <= r_source_bottom and c_source_left <= c_target <= c_source_right):
                                     continue
                                source_color = input_np[r_source, c_target]
                                # Ensure we only copy non-white/non-gray from pattern block
                                if source_color != 0 and source_color != 5:
                                     output_np[r_target, c_target] = source_color


    # Convert back to list of lists for the required output format
    output_list = output_np.tolist()
    return output_list
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0
0 2 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0
0 2 2 2 2 2 2 0 0 0
0 1 1 1 1 1 1 0 0 0
0 2 2 2 2 2 2 0 0 0
0 6 6 6 6 6 6 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0
0 2 2 2 2 2 2 0 0 0
0 1 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 25
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
5 4 3 3 4 4 4 0 0 0
5 7 3 7 7 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 5 5 5 5
5 0 0 0 0 0 3 0 0 0
5 0 0 0 0 0 3 0 0 0
5 0 0 0 0 0 7 0 0 0
5 0 0 0 0 0 3 0 0 0
5 0 0 0 0 0 7 0 0 0
5 0 0 0 0 0 7 0 0 0
5 6 3 6 3 0 0 0 0 0
5 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 5 5 5 5
5 6 3 6 3 0 3 3 3 3
5 2 2 2 2 0 3 3 3 3
5 6 3 6 3 0 7 7 7 7
5 2 2 2 2 0 3 3 3 3
5 6 3 6 3 0 7 7 7 7
5 2 2 2 2 0 7 7 7 7
5 6 3 6 3 0 0 0 0 0
5 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 5 5 5 5
5 6 3 6 3 0 3 3 3 3
5 2 2 2 2 0 3 0 0 0
5 6 3 6 3 0 7 0 0 0
5 2 2 2 2 0 3 0 0 0
5 6 3 6 3 0 7 0 0 0
5 2 2 2 2 0 7 0 0 0
5 6 3 6 3 0 0 0 0 0
5 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.0

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 6 6 6 9 9 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 6 6 6 9 9 9 0
0 0 5 6 6 6 9 9 9 0
0 0 5 6 6 6 9 9 9 0
0 0 5 6 6 6 9 9 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 6 6 6 9 9 9 0
0 0 5 6 6 6 9 9 9 0
0 0 5 6 6 6 9 9 9 0
0 0 5 6 6 6 9 9 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
