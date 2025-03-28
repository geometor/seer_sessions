
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
## General Assessment

The previous code successfully solved Examples 2 and 4, which primarily involved the vertical tiling rule. However, it failed on Examples 1 and 3, both of which rely heavily on the horizontal propagation rule. The transformed output for these failed examples shows that only the *first* non-background color found below the horizontal gray segment in the starting column was propagated horizontally. The expected output clearly shows that *all* non-background colors found vertically below the segment (within the segment's column span) should be propagated horizontally across the columns covered by the segment.

The error stems from the interpretation and implementation of the horizontal propagation rule. The previous logic included a `break` after finding the first source color in the downward search for each column under the gray segment. This prevented subsequent colors in the same column from being propagated.

**Strategy for Resolution:**

1.  Modify the horizontal propagation rule description to explicitly state that the search for source colors below the gray segment should continue downwards for the entire height of the grid for each column under the segment.
2.  The corresponding implementation change will involve removing the `break` statement within the downward search loop (`for r_source_row in range(r + 1, H):`) in the horizontal propagation section of the code.

## Metrics Gathering

Let's examine the differences in the failed examples:

**Example 1:**
*   Input Grid (relevant part):
    
```
    0 5 5 5 5 5 5 0
    0 2 0 0 0 0 0 0
    0 1 0 0 0 0 0 0
    0 2 0 0 0 0 0 0
    0 6 0 0 0 0 0 0
    0 1 0 0 0 0 0 0
    0 1 0 0 0 0 0 0
    ```

*   Expected Output (relevant part):
    
```
    0 5 5 5 5 5 5 0
    0 2 2 2 2 2 2 0
    0 1 1 1 1 1 1 0
    0 2 2 2 2 2 2 0
    0 6 6 6 6 6 6 0
    0 1 1 1 1 1 1 0
    0 1 1 1 1 1 1 0
    ```

*   Transformed Output (relevant part):
    
```
    0 5 5 5 5 5 5 0
    0 2 2 2 2 2 2 0
    0 1 0 0 0 0 0 0
    0 2 0 0 0 0 0 0
    0 6 0 0 0 0 0 0
    0 1 0 0 0 0 0 0
    0 1 0 0 0 0 0 0
    ```

*   Analysis: The code correctly identified the red pixel (2) at (2, 1) below the gray segment (row 1, cols 1-6) and propagated it horizontally to fill row 2, cols 2-6. However, it stopped searching downwards in column 1 after finding the first color (red). It missed the blue (1) at (3, 1), red (2) at (4, 1), magenta (6) at (5, 1), blue (1) at (6, 1), and blue (1) at (7, 1), which should have been propagated across their respective rows (rows 3-7) within the segment's horizontal extent (cols 2-6).

**Example 3:**
*   Input Grid (relevant part):
    
```
    0 0 5 5 5 5
    0 0 3 0 0 0
    0 0 3 0 0 0
    0 0 7 0 0 0
    0 0 3 0 0 0
    0 0 7 0 0 0
    0 0 7 0 0 0
    ```

*   Expected Output (relevant part):
    
```
    0 0 5 5 5 5
    0 0 3 3 3 3
    0 0 3 3 3 3
    0 0 7 7 7 7
    0 0 3 3 3 3
    0 0 7 7 7 7
    0 0 7 7 7 7
    ```

*   Transformed Output (relevant part):
    
```
    0 0 5 5 5 5
    0 0 3 3 3 3
    0 0 3 0 0 0
    0 0 7 0 0 0
    0 0 3 0 0 0
    0 0 7 0 0 0
    0 0 7 0 0 0
    ```

*   Analysis: Similar to Example 1. The gray segment is at row 0, cols 6-9. The code processed column 6. It found green (3) at (1, 6) and propagated it. It found orange (7) at (3, 6) and propagated it. It found orange (7) at (5, 6) and propagated it. It found orange (7) at (6, 6) and propagated it. Crucially, it *missed* propagating the green (3) at (2, 6) and the green (3) at (4, 6) because of the incorrect `break` logic tied to finding the *first* color in the downward scan *per column*. The rule should be: for *each* column under the gray segment, find *all* non-white/non-gray colors below it, and for *each* of those found colors, propagate it horizontally to the right within its row, up to the boundary of the gray segment.

## YAML Facts


```yaml
task_description: Applies two transformation rules based on the presence and orientation of gray (5) segments to fill adjacent white (0) areas.
grid_properties:
  - size: Variable height and width (1x1 to 30x30).
  - background_color: white (0).
  - active_color: gray (5) acts as a trigger.
  - pattern_colors: Various non-white, non-gray colors (1-4, 6-9).

objects:
  - type: segment
    properties:
      - color: gray (5)
      - contiguity: Maximal contiguous horizontal or vertical line.
  - type: pixel
    properties:
      - color: Any color (0-9)
      - location: (row, column) coordinates
  - type: pattern_source
    properties:
      - location: Below a horizontal gray segment or right of a vertical gray segment.
      - color: Not white (0) and not gray (5).
  - type: pattern_block (for vertical rule)
    properties:
      - location: Connected component of pattern_source pixels right of a vertical gray segment, within its row bounds.
      - shape: Rectangular bounding box.
      - content: A grid of pattern_source pixels.

actions:
  - name: find_gray_segments
    input: input_grid
    output: list of horizontal segments, list of vertical segments (location, extent)
  - name: horizontal_propagation
    trigger: horizontal gray segment at (r, c_start) to (r, c_end)
    input: input_grid, segment location
    output: modified_grid
    steps:
      - For each column `c_source` from `c_start` to `c_end`:
        - Search vertically downwards from `(r + 1, c_source)`.
        - For *each* pixel `(r_source, c_source)` found with a `source_color` (not white or gray):
          - Propagate `source_color` horizontally to the right within row `r_source`.
          - For each column `c_target` from `c_source + 1` to `c_end`:
            - If the pixel at `(r_source, c_target)` is white (0), change its color to `source_color`.
  - name: vertical_tiling
    trigger: vertical gray segment at (r_top, c) to (r_bottom, c)
    input: input_grid, segment location
    output: modified_grid
    steps:
      - Check column `c + 1` for seed pixels (non-white/gray) between rows `r_top` and `r_bottom`.
      - If seeds exist:
        - Find the connected component of non-white/gray pixels containing seeds (bounded by rows `r_top` to `r_bottom`, columns `c + 1` onwards).
        - Determine the bounding box `(r_source_top, r_source_bottom, c_source_left, c_source_right)` of this component (pattern block).
        - If a valid pattern block exists:
          - Calculate pattern height `H_pattern`.
          - Tile upwards: For each target row `r_target` from `r_source_top - 1` down to `r_top`:
            - Calculate the corresponding source row `r_source` using modulo arithmetic based on `H_pattern`.
            - For each target column `c_target` from `c_source_left` to `c_source_right`:
              - If `(r_target, c_target)` is white (0):
                - Get `source_color` from input grid at `(r_source, c_target)`.
                - If `source_color` is not white (0) or gray (5), set `(r_target, c_target)` to `source_color`.

final_grid_construction:
  - Start with a copy of the input grid.
  - Apply horizontal propagation rule for all horizontal gray segments.
  - Apply vertical tiling rule for all vertical gray segments. The order might matter if rules overlap or interact, but based on examples, applying horizontal then vertical seems correct. The modifications happen on the same output grid copy.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  **Horizontal Propagation Rule:**
    a.  Identify all maximal horizontal segments of gray pixels (5).
    b.  For each horizontal segment located at row `r` spanning columns `c_start` to `c_end`:
        i.  Iterate through each column `c_source` from `c_start` to `c_end`.
        ii. Search vertically downwards starting from the pixel below the segment at `(r + 1, c_source)`.
        iii. For **every** pixel `(r_source, c_source)` found during this downward search that has a color `source_color` which is neither white (0) nor gray (5):
            1. Propagate this `source_color` horizontally to the right within its own row `r_source`.
            2. Iterate through target columns `c_target` from `c_source + 1` to `c_end`.
            3. If the pixel at `(r_source, c_target)` in the *output* grid is currently white (0), change its color to `source_color`.
3.  **Vertical Tiling Rule:**
    a.  Identify all maximal vertical segments of gray pixels (5).
    b.  For each vertical segment located at column `c` spanning rows `r_top` to `r_bottom`:
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
4.  Return the modified output grid.
