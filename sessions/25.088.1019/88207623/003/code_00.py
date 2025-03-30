import numpy as np
from collections import deque

"""
Transforms the input grid based on vertical red lines and associated fill colors.

1. Find unique 'fill colors' (not white=0, red=2, yellow=4) in scan order (top-to-bottom, left-to-right).
2. Find all distinct, contiguous, vertical segments composed only of red (2) pixels. Record each segment's column index, start row, and end row.
3. Sort the red segments first by their start row index (ascending) and then by their column index (ascending).
4. Associate the sorted red segments with the identified fill colors sequentially. The i-th segment corresponds to the i-th fill color.
5. For each associated (segment, fill_color) pair:
   a. Determine the fill side (left or right of the red segment). Count the number of fillable pixels (white=0 or yellow=4) immediately to the left (in column segment_col - 1) and immediately to the right (in column segment_col + 1) of the segment, but only considering rows spanned by the segment (from start_row to end_row).
   b. If the count on the right is greater than the count on the left, the fill direction is RIGHT.
   c. If the count on the left is greater than the count on the right, the fill direction is LEFT.
   d. If the counts are equal and non-zero, the fill direction is RIGHT (tie-breaker).
   e. If both counts are zero, or the chosen fill side is outside the grid, no fill operation is performed for this segment.
6. Perform a flood fill operation on the chosen side:
   a. Identify the initial "seed" pixels for the flood fill. These are the pixels in the column immediately adjacent to the red segment on the determined fill side (column segment_col + direction), within the segment's row bounds (start_row to end_row). Only include seeds that are initially fillable (white=0 or yellow=4).
   b. If there are no valid seed pixels, skip the fill operation for this segment.
   c. Starting from the seed pixels, perform a flood fill:
      i. Use a queue and a set to track visited pixels for this specific fill operation.
      ii. Change the color of fillable pixels (white=0 or yellow=4) encountered during the fill to the associated `fill_color`.
      iii. The flood fill propagates horizontally and vertically (up, down, left, right) to adjacent pixels.
      iv. The fill is constrained: it only affects pixels whose row index is within the original red segment's row bounds (start_row to end_row).
      v. The fill stops at pixels that are not fillable (i.e., not white=0 or yellow=4) or are outside the vertical bounds.
7. Return the modified grid.
"""

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

def flood_fill(grid, seeds, fill_color, segment_row_bounds, fillable_colors):
    """
    Performs a flood fill on the grid, constrained vertically.
    Modifies the grid in place.
    """
    rows, cols = grid.shape
    q = deque(seeds)
    visited = set(seeds) # Initialize visited with seeds

    min_row, max_row = segment_row_bounds

    while q:
        r, c = q.popleft()

        # Current cell must be fillable (already checked for seeds, check again for neighbors)
        # This check should happen *before* filling
        # if grid[r, c] not in fillable_colors: # This check is implicitly handled by neighbor check
        #    continue

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

            # Check if fillable color
            if grid[nr, nc] not in fillable_colors:
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
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    fillable_colors = {0, 4} # Colors that can be replaced by the fill

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

        # 5. Determine fill side based on adjacent fillable pixels
        count_left = 0
        left_col = seg_col - 1
        if 0 <= left_col < cols:
            for r in range(start_row, end_row + 1):
                # Check against the *current state* of output_grid, as previous fills might change things
                # Although, fillable check {0,4} should be based on initial state? No, examples imply fill stops at boundaries created by prior fills. So use output_grid.
                if output_grid[r, left_col] in fillable_colors:
                    count_left += 1

        count_right = 0
        right_col = seg_col + 1
        if 0 <= right_col < cols:
             for r in range(start_row, end_row + 1):
                 if output_grid[r, right_col] in fillable_colors:
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

        # 6. Prepare seeds and perform flood fill
        start_fill_col = seg_col + direction

        # Check if the starting column for the fill is within grid bounds
        if not (0 <= start_fill_col < cols):
             continue

        seeds = []
        for r in range(start_row, end_row + 1):
             # Add point as a seed only if it's within bounds and initially fillable in the target column
             if output_grid[r, start_fill_col] in fillable_colors:
                 seeds.append((r, start_fill_col))

        # If there are valid starting points for the fill
        if seeds:
            # Perform the flood fill, modifying output_grid in place
            flood_fill(output_grid, seeds, fill_color, segment_row_bounds, fillable_colors)

    return output_grid