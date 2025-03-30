import numpy as np
from collections import deque

"""
Transforms the input grid by performing flood fills adjacent to vertical red lines.

1. Initialize the output grid as a copy of the input grid.
2. Find unique 'fill colors' by scanning the input grid (top-to-bottom, left-to-right). Fill colors are any color other than white (0), red (2), or yellow (4). Store them in the order they appear.
3. Find all distinct, contiguous, vertical segments composed only of red (2) pixels in the input grid. Record each segment's column index, start row, and end row.
4. Sort the red segments first by their start row index (ascending) and then by their column index (ascending).
5. Associate the Nth sorted red segment with the Nth found fill color.
6. For each associated (segment, fill_color) pair:
    a. Determine the fill side (left or right) by counting white (0) pixels in the *input grid* immediately adjacent to the segment (left column vs. right column), within the segment's row bounds (start_row to end_row).
    b. Fill on the side with more adjacent white pixels. If counts are equal and non-zero, fill right (tie-breaker). If counts are zero, or the chosen side is off-grid, do nothing for this segment.
    c. Identify initial 'seed' pixels for the fill. These are pixels `(r, c)` where `c` is the adjacent column on the chosen fill side, `r` is within the segment's row bounds, `input_grid[r, c]` is white (0), and `output_grid[r, c]` is currently white (0).
    d. If seed pixels exist, perform a flood fill on the `output_grid` starting from these seeds using the `fill_color`.
    e. The flood fill propagates horizontally and vertically to adjacent pixels `(nr, nc)`.
    f. A pixel `(nr, nc)` is filled (changed to `fill_color` in the `output_grid`) *only if* it is within the grid boundaries AND the corresponding pixel `input_grid[nr, nc]` was originally white (0). Non-white pixels in the input grid act as boundaries.
7. Return the modified output grid.
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
                    if row_idx < rows:
                       visited[row_idx, c] = True

                # Store the segment information
                segments.append({'col': c, 'start_row': start_row, 'end_row': end_row})

    # Sort segments primarily by start_row, secondarily by col
    segments.sort(key=lambda s: (s['start_row'], s['col']))
    return segments

def flood_fill(output_grid, seeds, fill_color, input_grid):
    """
    Performs a flood fill on the output_grid, constrained by non-white pixels
    in the input_grid. Modifies output_grid in place.
    """
    rows, cols = output_grid.shape
    if not seeds: # No starting points
        return

    q = deque(seeds)
    # Keep track of visited cells for *this specific fill operation*
    # Initialize visited with the seeds themselves
    visited_this_fill = set(seeds)

    while q:
        r, c = q.popleft()

        # Fill the current cell *in the output grid*
        # Check if it's still white (though seeds should guarantee this initially)
        # This check is mainly for safety if seeds could overlap strangely,
        # but primarily the propagation logic below handles boundaries.
        # We rely on the fact that seeds were already checked against input_grid == 0
        # and output_grid == 0.
        if output_grid[r,c] == 0: # Check if it hasn't been filled by this *same* fill process already (handled by visited) or a *prior* fill process
            output_grid[r, c] = fill_color

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            # Check if the neighbor *in the input grid* is fillable (white=0)
            if input_grid[nr, nc] != 0:
                continue

            # Check if already visited *for this specific flood fill*
            if (nr, nc) in visited_this_fill:
                continue

            # Check if the neighbor in the output grid hasn't *already* been
            # filled by a *previous* fill operation (or is a non-white original pixel)
            # This prevents re-filling or filling over other colors.
            if output_grid[nr, nc] != 0:
                 continue

            # Add valid neighbor to queue and mark visited for this fill
            visited_this_fill.add((nr, nc))
            q.append((nr, nc))


def transform(input_grid):
    """
    Applies the flood fill transformation based on red lines and fill colors.
    """
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    fillable_color = 0 # Explicitly state that only white is fillable

    # 2. Find fill colors in scan order
    fill_colors = find_fill_colors(input_grid)

    # 3. & 4. Find and sort vertical red segments
    red_segments = find_red_segments(input_grid)

    # 5. Associate segments with fill colors and process
    num_segments = len(red_segments)
    num_colors = len(fill_colors)

    # Iterate through matched pairs of segments and colors
    for i in range(min(num_segments, num_colors)):
        segment = red_segments[i]
        fill_color = fill_colors[i]

        seg_col = segment['col']
        start_row = segment['start_row']
        end_row = segment['end_row']

        # 6a. Determine fill side based on adjacent WHITE pixels in the ORIGINAL grid
        count_left = 0
        left_col = seg_col - 1
        if 0 <= left_col < cols:
            for r in range(start_row, end_row + 1):
                 # Check against the *original input grid* and only count white (0)
                 if 0 <= r < rows and input_grid[r, left_col] == fillable_color:
                    count_left += 1

        count_right = 0
        right_col = seg_col + 1
        if 0 <= right_col < cols:
             for r in range(start_row, end_row + 1):
                 # Check against the *original input grid* and only count white (0)
                 if 0 <= r < rows and input_grid[r, right_col] == fillable_color:
                     count_right += 1

        # 6b. Decide direction
        direction = 0 # Default: no fill
        if count_right > count_left:
            direction = 1 # Fill Right
        elif count_left > count_right:
            direction = -1 # Fill Left
        # Tie-breaker: If counts are equal AND non-zero, fill Right
        elif count_left == count_right and count_right > 0:
             direction = 1 # Fill Right

        # If no direction determined or side off-grid, skip
        if direction == 0:
            continue

        fill_side_col = seg_col + direction
        if not (0 <= fill_side_col < cols):
             continue

        # 6c. Identify seed pixels
        seeds = []
        for r in range(start_row, end_row + 1):
             # Check row bounds (redundant due to loop, but safe)
             if 0 <= r < rows:
                 # Seed must be originally white in input
                 if input_grid[r, fill_side_col] == fillable_color:
                     # Seed must also be currently white in output (not filled previously)
                     if output_grid[r, fill_side_col] == fillable_color:
                         seeds.append((r, fill_side_col))

        # 6d. & 6e. & 6f. Perform flood fill if seeds exist
        if seeds:
            # Perform the flood fill, modifying output_grid in place
            # The fill uses input_grid to check boundaries/fillable areas
            flood_fill(output_grid, seeds, fill_color, input_grid)

    # 7. Return the modified grid
    return output_grid