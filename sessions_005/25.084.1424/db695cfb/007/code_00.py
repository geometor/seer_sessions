import numpy as np
from collections import Counter

"""
Transformation Rule:

1.  **Initialization**: Create an output grid as a copy of the input grid.
2.  **Identify Roles**:
    *   Find all blue pixels (color 1); these are the 'sources'.
    *   Find all magenta pixels (color 6); these are the potential 'destinations'.
    *   Determine the 'background color' by finding the most frequent color in the input grid, excluding blue (1) and magenta (6). If only blue/magenta exist or the grid is empty otherwise, use white (0) as the background.
3.  **Determine Actual Destinations**:
    *   If any magenta pixels exist, they are the 'actual destinations'.
    *   If no magenta pixels exist, the blue pixels themselves serve as the 'actual destinations' for each other (a blue pixel cannot be its own destination).
4.  **Path Generation and Drawing**:
    *   Iterate through every unique pair of a source pixel `S` and an actual destination pixel `D`.
    *   If `S` is the same pixel as `D`, skip this pair.
    *   Set the `path_color` to blue (1).
    *   Calculate a path sequence from `S` towards `D`:
        *   Start at `current_pos = S`. Maintain a set `visited_on_this_path` containing only `S`.
        *   While true (loop broken internally):
            *   Find all valid 8-directional neighbors of `current_pos`, sorted by row then column index.
            *   Calculate the Manhattan distance from each neighbor to `D`.
            *   Find the minimum distance (`min_dist`) among these neighbors.
            *   Identify all neighbors (`min_dist_neighbors`) that achieve this `min_dist`.
            *   Apply tie-breaking to select the `next_step_info` (containing position and move delta) from `min_dist_neighbors`:
                1.  Prefer neighbors reached by a diagonal move (change in both row and column) over axial moves (change in only row or column).
                2.  If ties remain within diagonal or axial groups, the pre-sorting by row/column determines the choice (smallest row, then smallest column).
            *   Get the selected `next_pos` from `next_step_info`.
            *   If `next_pos` *is* the destination `D`, stop calculating this path segment (reached destination).
            *   If `next_pos` is already in `visited_on_this_path`, stop calculating this path segment (cycle detected).
            *   Mark `next_pos`: If the pixel at `next_pos` in the *current output grid* has the `background_color`, change its color to `path_color` (blue, 1).
            *   Add `next_pos` to `visited_on_this_path`.
            *   Update `current_pos = next_pos`.
            *   If no valid neighbors were found (e.g., current_pos is surrounded or only neighbor is D which was handled), stop this path segment.
5.  **Final Output**: Return the modified output grid after processing all source-destination pairs.
"""

import numpy as np
from collections import Counter

def find_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    return list(zip(*np.where(grid == color)))

def get_background_color(grid):
    """Finds the most common color excluding blue (1) and magenta (6). Defaults to 0."""
    counts = Counter(grid.flatten())
    if 1 in counts: del counts[1]
    if 6 in counts: del counts[6]
    if not counts: return 0 # Default to white if only 1/6 or empty
    # Check if 0 exists and is most common, otherwise return the most common
    if 0 in counts and counts[0] >= counts.most_common(1)[0][1]:
        return 0
    elif counts:
         return counts.most_common(1)[0][0]
    else: # Should only happen on truly empty grid after filtering
         return 0


def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points (tuples)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(r, c, height, width):
    """Gets valid 8-directional neighbors for a given coordinate.

    Returns:
        list: A list of tuples, where each tuple contains:
              ((neighbor_row, neighbor_col), (delta_row, delta_col)).
              Sorted by row, then column index.
    """
    neighbors = []
    # Order matters for tie-breaking: check smaller row/col first implicitly
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(((nr, nc), (dr, dc)))
    # Sort neighbors for consistent tie-breaking: row, then column
    neighbors.sort(key=lambda x: (x[0][0], x[0][1]))
    return neighbors


def transform(input_grid):
    """
    Applies the path-drawing transformation based on blue sources and magenta/blue destinations.
    Paths are drawn with blue (1), avoiding cycles and stopping before the destination.
    """
    # 1. Initialization
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify Roles
    source_pixels = find_pixels(input_grid, 1) # Blue
    magenta_pixels = find_pixels(input_grid, 6) # Magenta
    background_color = get_background_color(input_grid)

    # 3. Determine Actual Destinations
    if magenta_pixels:
        destination_pixels = magenta_pixels
    else:
        # If no magenta, blue pixels target each other
        destination_pixels = source_pixels

    # Exit early if no sources or destinations to pair with
    if not source_pixels or not destination_pixels:
        return output_grid
    # Specific check for blue->blue case where only one blue exists
    if not magenta_pixels and len(source_pixels) <= 1:
        return output_grid

    # 4. Path Generation and Drawing
    path_color = 1 # Paths are always blue

    for start_pos in source_pixels:
        for end_pos in destination_pixels:
            # 4a. Skip if source is the same as destination (relevant for blue->blue)
            if start_pos == end_pos:
                continue

            # 4c. Calculate path sequence from S towards D
            current_pos = start_pos
            visited_on_this_path = {start_pos} # Track visited for cycle detection

            while True:
                # Find neighbors and calculate distances to the end_pos
                neighbors_info = get_neighbors(current_pos[0], current_pos[1], height, width)

                valid_next_steps = []
                min_dist = float('inf')

                for neighbor_pos, move_delta in neighbors_info:
                    # Calculate distance for all neighbors
                    dist = manhattan_distance(neighbor_pos, end_pos)
                    valid_next_steps.append({'pos': neighbor_pos, 'delta': move_delta, 'dist': dist})
                    # Find minimum distance among potential next steps
                    # Important: Don't filter out end_pos here, let tie-breaking handle it if needed
                    # Only exclude it from being a *step* later.
                    if neighbor_pos != current_pos: # Avoid comparing distance from current pos to itself if somehow included
                         min_dist = min(min_dist, dist)


                # If no valid moves possible (e.g., trapped)
                if not valid_next_steps:
                    break

                # Filter neighbors with the minimum distance
                min_dist_neighbors = [n for n in valid_next_steps if n['dist'] == min_dist]

                # Handle cases where the only min_dist neighbor is the current position itself (shouldn't happen with get_neighbors)
                # or if min_dist_neighbors is empty (should also not happen if valid_next_steps wasn't empty)
                if not min_dist_neighbors:
                     break # Cannot proceed

                # Tie-breaking logic
                diagonal_moves = [n for n in min_dist_neighbors if abs(n['delta'][0]) == 1 and abs(n['delta'][1]) == 1]
                axial_moves = [n for n in min_dist_neighbors if abs(n['delta'][0]) != abs(n['delta'][1])] # Includes 0,1 and 1,0 moves

                next_step_info = None
                if diagonal_moves:
                    # Select the first diagonal move based on pre-sorted neighbors (row, then col)
                    next_step_info = diagonal_moves[0]
                elif axial_moves:
                     # Select the first axial move based on pre-sorted neighbors (row, then col)
                    next_step_info = axial_moves[0]
                else:
                     # This might happen if the only min_dist neighbor is the destination itself,
                     # and it's neither diagonal nor axial relative to current_pos (e.g. distance 1 away)
                     # Or if multiple neighbors have same min dist but none fit diagonal/axial cleanly - use first overall.
                     if min_dist_neighbors:
                         next_step_info = min_dist_neighbors[0]
                     else:
                         break # Cannot determine next step

                if next_step_info is None: # Safety break
                    break

                next_pos = next_step_info['pos']

                # Termination condition: Stop if the chosen next step *is* the destination
                if next_pos == end_pos:
                    break

                # Cycle detection: Stop if we are about to move to a previously visited pixel on this path
                if next_pos in visited_on_this_path:
                    break

                # Mark the pixel if it's background color
                # Check the *current* state of the output grid
                if output_grid[next_pos] == background_color:
                    output_grid[next_pos] = path_color # Use blue (1)

                # Update path tracking
                visited_on_this_path.add(next_pos)
                current_pos = next_pos


    # 5. Final Output
    return output_grid