
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on vertical red lines and associated fill colors.

1. Find unique 'fill colors' (not white=0, red=2, yellow=4) in scan order (top-to-bottom, left-to-right).
2. Find all distinct, contiguous, vertical segments composed only of red (2) pixels. Record each segment's column index, start row, and end row.
3. Sort the red segments first by their start row index (ascending) and then by their column index (ascending).
4. Associate the sorted red segments with the identified fill colors sequentially. The i-th segment corresponds to the i-th fill color.
5. For each associated (segment, fill_color) pair:
   a. Determine the fill side (left or right of the red segment). Count the number of fillable pixels (white=0 only) in the *original input grid* immediately to the left (in column segment_col - 1) and immediately to the right (in column segment_col + 1) of the segment, but only considering rows spanned by the segment (from start_row to end_row).
   b. If the count on the right is greater than the count on the left, the fill direction is RIGHT.
   c. If the count on the left is greater than the count on the right, the fill direction is LEFT.
   d. If the counts are equal and non-zero, the fill direction is RIGHT (tie-breaker).
   e. If both counts are zero, or the chosen fill side is outside the grid, no fill operation is performed for this segment.
6. Perform a flood fill operation on the chosen side:
   a. Identify the initial "seed" pixels for the flood fill. These are the pixels in the column immediately adjacent to the red segment on the determined fill side (column segment_col + direction), within the segment's row bounds (start_row to end_row). Only include seeds that are initially fillable (white=0) in the *current state* of the output grid.
   b. If there are no valid seed pixels, skip the fill operation for this segment.
   c. Starting from the seed pixels, perform a flood fill on the `output_grid`:
      i. Use a queue and a set to track visited pixels for this specific fill operation.
      ii. Change the color of fillable pixels (white=0 only) encountered during the fill to the associated `fill_color`.
      iii. The flood fill propagates horizontally and vertically (up, down, left, right) to adjacent pixels.
      iv. The fill is constrained: it only affects pixels whose row index is within the original red segment's row bounds (start_row to end_row).
      v. The fill stops at pixels that are not fillable (i.e., not white=0), including yellow=4, red=2, and other fill colors, or pixels outside the vertical bounds.
7. Return the modified grid.
"""

import numpy as np
from collections import deque

def find_fill_colors(grid):
    """
    Finds unique fill colors (not 0, 2, or 4) in scan order.
    """
    fill_colors = []
    seen_colors = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Fill colors are those not white(0), red(2), or yellow(4)
            if color not in {0, 2, 4} and color not in seen_colors:
                fill_colors.append(color)
                seen_colors.add(color)
    return fill_colors

def find_red_segments(grid):
    """
    Finds all vertical red (2) segments and returns them as a list of dicts:
    {'col': c, 'start_row': start_row, 'end_row': end_row}.
    Segments are sorted by start_row, then col.
    """
    rows, cols = grid.shape
    segments = []
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is red and not yet part of a found segment
            if grid[r, c] == 2 and not visited[r, c]:
                # Found the potential start of a vertical segment
                start_row = r
                end_row = r
                # Explore downwards to find the end of the segment
                while end_row + 1 < rows and grid[end_row + 1, c] == 2:
                    end_row += 1

                # Mark the cells of this segment as visited
                for row_idx in range(start_row, end_row + 1):
                    if row_idx < rows: # Boundary check is technically redundant due to loop condition, but safe
                       visited[row_idx, c] = True

                # Store the segment information
                segments.append({'col': c, 'start_row': start_row, 'end_row': end_row})

    # Sort segments primarily by start_row, secondarily by col
    segments.sort(key=lambda s: (s['start_row'], s['col']))
    return segments

def flood_fill(grid, seeds, fill_color, segment_row_bounds, fillable_color):
    """
    Performs a flood fill on the grid, constrained vertically.
    Modifies the grid in place.
    Only fills cells with `fillable_color`.
    """
    rows, cols = grid.shape
    if not seeds: # No starting points
        return

    q = deque(seeds)
    visited = set(seeds) # Initialize visited with seeds
    min_row, max_row = segment_row_bounds

    while q:
        r, c = q.popleft()

        # Check if the current cell is still fillable (it might have been filled by another process if seeds overlapped somehow, though unlikely here)
        # Ensure we are within the vertical bounds (seeds are checked, but neighbors need checking)
        if not (min_row <= r <= max_row) or grid[r,c] != fillable_color:
            continue

        # Fill the current cell
        grid[r, c] = fill_color

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            # Check vertical constraint (within segment rows)
            if not (min_row <= nr <= max_row):
                 continue

            # Check if it's the specific fillable color
            if grid[nr, nc] != fillable_color:
                continue

            # Check if already visited for this specific flood fill
            if (nr, nc) in visited:
                continue

            # Add to queue and mark visited
            visited.add((nr, nc))
            q.append((nr, nc))


def transform(input_grid):
    """
    Applies the transformation rule based on red lines and fill colors.
    Fills white (0) areas adjacent to red lines based on counts of adjacent white pixels.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    # Define the *only* color that can be replaced by the fill
    fillable_color = 0 # Only white is fillable

    # 1. Find fill colors in scan order
    fill_colors = find_fill_colors(input_grid)

    # 2. & 3. Find and sort vertical red segments
    red_segments = find_red_segments(input_grid)

    # 4. Associate segments with fill colors
    num_segments = len(red_segments)
    num_colors = len(fill_colors)

    # Iterate through matched pairs of segments and colors
    for i in range(min(num_segments, num_colors)):
        segment = red_segments[i]
        fill_color = fill_colors[i]

        seg_col = segment['col']
        start_row = segment['start_row']
        end_row = segment['end_row']
        segment_row_bounds = (start_row, end_row) # For flood fill constraint

        # 5. Determine fill side based on adjacent WHITE pixels in the ORIGINAL grid
        count_left = 0
        left_col = seg_col - 1
        if 0 <= left_col < cols:
            for r in range(start_row, end_row + 1):
                # Check against the *original input grid* and only count white (0)
                if input_grid[r, left_col] == fillable_color:
                    count_left += 1

        count_right = 0
        right_col = seg_col + 1
        if 0 <= right_col < cols:
             for r in range(start_row, end_row + 1):
                 # Check against the *original input grid* and only count white (0)
                 if input_grid[r, right_col] == fillable_color:
                     count_right += 1

        direction = 0 # Default: no fill
        if count_right > count_left:
            direction = 1 # Fill Right
        elif count_left > count_right:
            direction = -1 # Fill Left
        # Tie-breaker: If counts are equal AND non-zero, fill Right
        elif count_left == count_right and count_right > 0:
             direction = 1 # Fill Right

        # If no direction determined (e.g., both counts 0, or segment at edge), skip
        if direction == 0:
            continue

        # 6. Prepare seeds and perform flood fill on the output grid
        start_fill_col = seg_col + direction

        # Check if the starting column for the fill is within grid bounds
        if not (0 <= start_fill_col < cols):
             continue

        seeds = []
        for r in range(start_row, end_row + 1):
             # Add point as a seed only if it's within vertical bounds and IS CURRENTLY the fillable color in the target column of the output_grid
             # This uses output_grid because previous fills might have blocked potential seeds
             if output_grid[r, start_fill_col] == fillable_color:
                 seeds.append((r, start_fill_col))

        # If there are valid starting points for the fill
        if seeds:
            # Perform the flood fill, modifying output_grid in place
            flood_fill(output_grid, seeds, fill_color, segment_row_bounds, fillable_color)

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 2 0 4 4 0 4 0 0 0 0
0 0 0 0 0 0 2 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 2 4 4 0 0 0 0 0 0 0
0 0 0 0 5 0 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 0 0 0 0 0 0 0 0 0 0
4 4 4 0 4 2 0 0 0 7 0 0 0 0 0 0
0 4 4 4 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 2 0 0 0 4 0 0 0 0 0
0 5 0 5 5 0 2 0 4 4 0 4 0 0 0 0
0 0 5 5 5 5 2 4 4 4 4 0 0 0 0 0
0 0 0 0 5 5 2 4 4 0 0 0 0 0 0 0
0 0 0 5 5 5 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 5 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 7 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 7 7 7 0 0 0 0 0 0 0
4 4 4 0 4 2 7 0 7 7 7 0 0 0 0 0
0 4 4 4 0 2 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 2 0 0 0 4 0 0 0 0 0
5 5 5 5 5 5 2 0 4 4 0 4 0 0 0 0
5 5 5 5 5 5 2 4 4 4 4 0 0 0 0 0
5 5 5 5 5 5 2 4 4 0 0 0 0 0 0 0
5 5 5 5 5 5 2 4 4 4 0 0 0 0 0 0
5 5 5 5 5 5 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 7 7 7 7 7 7 7 7 7 7
0 0 4 4 4 2 7 7 7 7 7 7 7 7 7 7
4 4 4 0 4 2 7 7 7 7 7 7 7 7 7 7
0 4 4 4 0 2 7 7 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 51
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 39.84375

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 8 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 0 4 4 2 8 8 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 3 0 3 3
0 0 0 0 0 0 0 0 4 4 0 2 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 8 8 8 8 8 8 8 8
0 0 0 4 4 4 2 8 8 8 8 8 8 8 8 8
0 0 0 4 4 4 2 8 8 8 8 8 8 8 8 8
0 0 0 4 4 4 2 8 8 8 8 8 8 8 8 8
0 0 0 0 4 4 2 8 8 8 8 8 8 8 8 8
0 0 0 0 0 4 2 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 3 3 3 3
0 0 0 0 0 0 0 0 0 4 0 2 3 3 3 3
0 0 0 0 0 0 0 4 4 0 4 2 3 3 3 3
0 0 0 0 0 0 0 0 4 4 0 2 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 50
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 44.64285714285714
**Metrics Analysis:**
*   **Colors & Segments:** The code correctly identifies the fill colors (gray=5, orange=7 for Ex1; azure=8, green=3 for Ex2) in scan order and finds the red segments, sorting them correctly (top-to-bottom, then left-to-right).
*   **Association:** The first color (5) is associated with the first segment (col 6, rows 1-6) in Ex1. The second color (7) with the second segment (col 5, rows 11-14). This matches the expected output pattern. Similarly for Ex2: color 8 with segment (col 6, 1-6); color 3 with segment (col 11, 9-12).
*   **Side Determination:**
    *   Ex1, Seg1: Left=6, Right=2 -> Choose Left (Correct, matches expected gray fill).
    *   Ex1, Seg2: Left=1, Right=4 -> Choose Right (Correct, matches expected orange fill).
    *   Ex2, Seg1: Left=0, Right=6 -> Choose Right (Correct, matches expected azure fill).
    *   Ex2, Seg2: Left=2, Right=4 -> Choose Right (Correct, matches expected green fill).
*   **Fill Area Discrepancy:** The core issue remains the *extent* of the flood fill. The previous code filled excessively. The new hypothesis is that the fill should replace a contiguous area of *white* pixels adjacent to the chosen side of the red segment, bounded only by *non-white* pixels present in the *original input grid* or the grid boundaries. The vertical bounds of the segment itself (`start_row`, `end_row`) should *not* constrain the fill's spread beyond determining the initial seed points.

**Final Check on Tie-breaking:**
The previous code had a tie-breaker: `elif count_left == count_right and count_right > 0: direction = 1 # Fill Right`. We didn't encounter a tie in these examples. Let's keep it for now, as it might be relevant for other cases.

**Summary of Changes Needed:**
1.  Modify the `flood_fill` function.
2.  It should take the `input_grid` as an argument to check for boundaries.
3.  Remove the `segment_row_bounds` argument and the associated vertical check (`min_row <= nr <= max_row`).
4.  The fill should propagate from seeds into neighbor `(nr, nc)` *only if* `input_grid[nr, nc] == 0` (white).
5.  The fill changes the color `output_grid[r, c]` to `fill_color` *only if* `input_grid[r, c] == 0`. (This ensures we only ever fill areas that were originally white).
6.  The `seeds` should still be determined based on white cells in the `output_grid` adjacent to the segment, to handle cases where previous fills might block a seed. `if output_grid[r, start_fill_col] == fillable_color: seeds.append((r, start_fill_col))`

Let's reconsider point 6. If a previous fill blocked a seed point that was originally white, should we still try to fill from other seeds in that region? Yes. The fill originates from the *region* adjacent to the segment. If *any* white cell adjacent to the segment (on the chosen side, within the segment's vertical extent) exists in the *current* `output_grid`, it can act as a seed. The fill then propagates based on the *input* grid's white space.

Refined Seed Generation:
`seeds = []`
`for r in range(start_row, end_row + 1):`
  `# Check if the adjacent cell in the target column is white IN THE INPUT`
  `if 0 <= start_fill_col < cols and input_grid[r, start_fill_col] == 0:`
     `# Also check if it hasn't ALREADY been filled in the output grid`
     `if output_grid[r, start_fill_col] == 0:`
         `seeds.append((r, start_fill_col))`

Refined Flood Fill Logic:
- Takes `output_grid`, `seeds`, `fill_color`, `input_grid`.
- Uses a queue `q` initialized with `seeds`.
- Uses a `visited` set, initialized with `seeds`.
- While `q` is not empty:
    - Dequeue `(r, c)`.
    - Set `output_grid[r, c] = fill_color`.
    - For each neighbor `(nr, nc)`:
        - Check grid bounds.
        - Check if `input_grid[nr, nc] == 0`.
        - Check if `(nr, nc)` not in `visited`.
        - If all pass, add `(nr, nc)` to `q` and `visited`.

This looks much better. The fill starts from valid adjacent points and expands through the originally white space defined by the input grid, stopping at any non-white input pixel or boundary.## General Assessment

The provided code attempts to solve the task by identifying vertical red lines, associating them with fill colors found elsewhere in the grid, determining a fill direction (left/right) based on adjacent white space, and performing a flood fill.

The analysis of the two examples shows that the code correctly identifies the red segments, finds the fill colors in the correct order, and correctly determines the side (left/right) on which to fill for each segment.

However, the `flood_fill` implementation is flawed. It incorrectly constrains the fill vertically to the bounds of the red segment and fills too extensively, ignoring non-white pixels (like yellow) present in the input grid that should act as boundaries. The transformed outputs show large rectangular fills instead of the more complex shapes bounded by other colors seen in the expected outputs.

The strategy for resolving the errors is to modify the `flood_fill` logic:
1.  The fill should use the *input* grid to determine boundaries. The fill should only spread into cells that were originally white (0) in the input.
2.  Any non-white cell (0) in the input grid should act as a hard boundary for the fill.
3.  The vertical constraint imposed by the red segment's start and end rows should be removed from the fill propagation logic; it should only apply to identifying the initial seed pixels adjacent to the segment.
4.  The fill operation modifies the `output_grid`, ensuring subsequent fills respect areas already filled.

## Metrics

Based on the code execution and visual inspection:

**Example 1:**
*   **Input:** 16x16 grid.
*   **Fill Colors (Scan Order):** Gray (5), Orange (7).
*   **Red Segments (Sorted):**
    *   Segment 1: col=6, start_row=1, end_row=6
    *   Segment 2: col=5, start_row=11, end_row=14
*   **Association:** Segment 1 <-> Gray (5), Segment 2 <-> Orange (7).
*   **Side Determination:**
    *   Segment 1: Adjacent White Count (Input): Left=6, Right=2 -> Fill Left. (Matches Expected)
    *   Segment 2: Adjacent White Count (Input): Left=1, Right=4 -> Fill Right. (Matches Expected)
*   **Output Discrepancy:** The code filled large rectangular areas bounded only by the segment's vertical extent and grid edges/red line. The expected output shows fills bounded by yellow (4) pixels present in the input.

**Example 2:**
*   **Input:** 14x16 grid.
*   **Fill Colors (Scan Order):** Azure (8), Green (3).
*   **Red Segments (Sorted):**
    *   Segment 1: col=6, start_row=1, end_row=6
    *   Segment 2: col=11, start_row=9, end_row=12
*   **Association:** Segment 1 <-> Azure (8), Segment 2 <-> Green (3).
*   **Side Determination:**
    *   Segment 1: Adjacent White Count (Input): Left=0, Right=6 -> Fill Right. (Matches Expected)
    *   Segment 2: Adjacent White Count (Input): Left=2, Right=4 -> Fill Right. (Matches Expected)
*   **Output Discrepancy:** Similar to Example 1, the code filled large rectangular areas. The expected output shows fills bounded by yellow (4) pixels present in the input.

**Key Findings:**
*   Yellow (4) pixels act as barriers defining the fill region.
*   The fill region is the contiguous area of white (0) pixels in the *input* grid that is adjacent to the determined side of the red segment.
*   The vertical extent of the red segment only matters for finding initial adjacent points (seeds), not for constraining the fill propagation.

## Facts (YAML)


```yaml
task_description: Flood fill areas adjacent to vertical red lines using specified colors, bounded by non-white pixels from the input.

objects:
  - type: grid
    properties:
      - 2D array of integers (0-9) representing colors.
      - Size varies (up to 30x30).
  - type: vertical_red_line
    properties:
      - A contiguous segment of red (2) pixels in a single column.
      - Defined by column index, start row, end row.
      - Acts as a trigger for a fill operation.
      - Acts as a boundary for fills originating from other lines.
  - type: fill_color_source
    properties:
      - Pixels with colors other than white (0), red (2), or yellow (4).
      - Their values determine the colors used for filling.
      - The order they appear in a top-to-bottom, left-to-right scan matters.
  - type: white_area
    properties:
      - Contiguous regions of white (0) pixels in the input grid.
      - Target areas for flood fills.
  - type: boundary_pixels
    properties:
      - Any non-white (0) pixel in the input grid (e.g., red (2), yellow (4), initial fill_color_source pixels, potentially others).
      - Define the limits of the flood fill propagation.
      - Grid edges also act as boundaries.

actions:
  - name: find_fill_colors
    description: Identify unique colors (not 0, 2, 4) in scan order (top-down, left-right).
  - name: find_red_segments
    description: Locate all vertical contiguous red (2) pixel segments. Record column, start row, end row for each.
  - name: sort_red_segments
    description: Order the found red segments primarily by start row (ascending), secondarily by column index (ascending).
  - name: associate_colors_segments
    description: Pair the Nth sorted red segment with the Nth found fill color.
  - name: determine_fill_side
    description: For each segment, count the white (0) pixels in the input grid immediately left and right, within the segment's row bounds. Fill the side with more white pixels. If equal and >0, fill right.
  - name: flood_fill_adjacent_area
    description: >
      For each (segment, fill_color, side) triplet:
      1. Identify initial seed points: white (0) pixels in the current grid state, located in the column adjacent to the segment on the chosen side, and within the segment's original row bounds.
      2. If seeds exist, perform a flood fill starting from these seeds:
         - The fill modifies the output grid.
         - The fill changes only pixels that were originally white (0) in the input grid to the `fill_color`.
         - The fill propagates horizontally and vertically.
         - The fill stops at grid boundaries or any pixel that was *not* white (0) in the *input* grid.

final_state: The output grid reflects the input grid with the specified white areas flood-filled according to the rules.
```


## Natural Language Program

1.  **Initialize:** Create a copy of the input grid, which will become the output grid.
2.  **Identify Fill Colors:** Scan the input grid (top-to-bottom, left-to-right) and collect the unique colors that are *not* white (0), red (2), or yellow (4). Store these "fill colors" in the order they are first encountered.
3.  **Identify Red Segments:** Find all distinct, contiguous, vertical segments composed only of red (2) pixels in the input grid. For each segment, record its column index, start row index, and end row index.
4.  **Sort Red Segments:** Sort the identified red segments first by their start row index (ascending) and then by their column index (ascending).
5.  **Associate and Fill:** Iterate through the sorted red segments and the identified fill colors simultaneously. For the i-th segment and the i-th fill color (if both exist):
    a.  **Determine Fill Side:** Compare the number of white (0) pixels *in the input grid* in the column immediately to the left of the segment versus the column immediately to the right. Only count pixels whose row index is between the segment's start and end rows (inclusive).
        *   If the right count is greater, choose the right side.
        *   If the left count is greater, choose the left side.
        *   If the counts are equal and greater than zero, choose the right side (tie-breaker).
        *   If both counts are zero or the chosen side is outside the grid, do nothing for this segment and proceed to the next.
    b.  **Identify Seed Pixels:** Find all pixels `(r, c)` such that:
        *   `c` is the column index immediately adjacent to the red segment on the determined fill side.
        *   `r` is within the red segment's row bounds (start\_row <= r <= end\_row).
        *   The pixel `(r, c)` is white (0) in the *input* grid.
        *   The pixel `(r, c)` is currently white (0) in the *output* grid (i.e., not already filled by a previous step).
    c.  **Perform Flood Fill:** If any seed pixels were identified:
        *   Start a flood fill operation on the `output_grid` using the identified seed pixels.
        *   Use the associated `fill_color`.
        *   The fill propagates to adjacent (up, down, left, right) pixels.
        *   A pixel `(nr, nc)` is filled *only if* it is within the grid boundaries AND the corresponding pixel `(nr, nc)` in the *input grid* was white (0).
        *   The fill continues until no more reachable valid pixels can be filled.
6.  **Return:** Return the modified output grid.
