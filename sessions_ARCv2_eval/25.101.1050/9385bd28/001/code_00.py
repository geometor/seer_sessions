import numpy as np
from collections import Counter

"""
Transformation Rule:

1.  Identify the background color (most frequent color in the input grid).
2.  Determine the source-to-fill color mapping based on color adjacency to the background:
    a. Find 'source' colors: non-background colors where at least one pixel of that color is orthogonally adjacent to the background color.
    b. Find 'potential fill-determining' colors (PFDs): non-background colors where *no* pixel of that color is orthogonally adjacent to the background color.
    c. If PFDs exist:
        - Each source color maps to the PFD color that is 'closest'. Closeness is defined as the minimum Manhattan distance between any pixel of the source color and any pixel of the PFD color.
        - Ties in distance are broken by choosing the PFD color with the lower numerical index (color value).
    d. If no PFDs exist:
        - Each source color maps to itself (identity map). Source colors that are not adjacent to the background are ignored.
3.  Initialize the output grid as a copy of the input grid.
4.  Perform an iterative flood-fill process until no changes occur in a full grid scan:
    a. In each iteration, calculate the next state of the grid based on the current state.
    b. For each pixel `(r, c)` in the grid:
        i.  Examine its orthogonal neighbors in the *current* grid state.
        ii. Collect 'fill influences' from neighbors:
            - If a neighbor has a color `N` which is a source color (from step 2a), its influence is the corresponding fill color `F` from the mapping (step 2c/2d).
            - If a neighbor has a color `N` which is itself one of the fill colors active in the mapping, its influence is `N`.
        iii. If there are any fill influences, determine the 'winning' fill color: the influencing fill color with the lowest numerical index (highest priority).
        iv. Consider the current color `C` at `(r, c)`.
        v.  If `C` is the background color, update the pixel in the *next* grid state to the winning fill color.
        vi. If `C` is not the background color, update the pixel in the *next* grid state to the winning fill color *only if* the winning fill color's index is strictly lower than `C`'s index (i.e., the winning fill has higher priority).
    c. After scanning all pixels, update the current grid state to the calculated next state.
5.  Once an iteration completes with no changes, return the final grid state.
"""

def get_neighbors(h, w, r, c):
    """ Get orthogonal neighbor coordinates within grid bounds. """
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < h - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < w - 1: neighbors.append((r, c + 1))
    return neighbors

def find_background_color(grid_np):
    """ Finds the most frequent color in the grid. """
    # Faster way for potentially large grids if numpy is available
    colors, counts = np.unique(grid_np, return_counts=True)
    return colors[np.argmax(counts)]

def derive_source_fill_map(grid_np, background_color):
    """ Derives the source-to-fill color mapping based on adjacency rules. """
    h, w = grid_np.shape
    unique_colors = np.unique(grid_np)
    non_background_colors = unique_colors[unique_colors != background_color]

    if len(non_background_colors) == 0:
        return {} # No non-background colors, no mapping needed

    color_pixels = {c: [] for c in non_background_colors}
    for r in range(h):
        for c in range(w):
            color = grid_np[r, c]
            if color != background_color:
                color_pixels[color].append((r, c))

    # Determine which colors are adjacent to background (sources)
    # and which are not (potential fill determiners - PFDs)
    sources = set()
    non_adjacent_fills = set(non_background_colors) # Assume non-adjacent initially
    for color in non_background_colors:
        is_adj = False
        # Check if *any* pixel of this color touches the background
        if color not in color_pixels: continue # Should not happen
        for r, c in color_pixels[color]:
             for nr, nc in get_neighbors(h, w, r, c):
                 if grid_np[nr, nc] == background_color:
                     is_adj = True
                     break
             if is_adj:
                 break # Found adjacency, no need to check more pixels for this color
        if is_adj:
            sources.add(color)
            if color in non_adjacent_fills:
                non_adjacent_fills.remove(color) # Correct its status

    source_map = {}
    # Case 1: PFDs exist - map sources to closest PFD
    if non_adjacent_fills:
        # Calculate all pairwise min distances between source pixels and PFD pixels
        min_dists = {} # Stores min distance from any pixel of s to any pixel of f: (s, f) -> min_dist
        for s in sources:
            if not color_pixels[s]: continue # Skip if source color has no pixels (edge case)
            for f in non_adjacent_fills:
                if not color_pixels[f]: continue # Skip if fill color has no pixels (edge case)

                current_min = float('inf')
                # Find min Manhattan distance between any pixel of s and any pixel of f
                for r_s, c_s in color_pixels[s]:
                    for r_f, c_f in color_pixels[f]:
                        dist = abs(r_s - r_f) + abs(c_s - c_f)
                        current_min = min(current_min, dist)
                min_dists[(s, f)] = current_min

        # For each source, find the PFD f with the minimum distance
        for s in sources:
            best_f = -1
            min_dist_for_s = float('inf')

            # Iterate through potential fills 'f' for this source 's'
            for f in non_adjacent_fills:
                 dist_key = (s, f)
                 if dist_key not in min_dists: continue # Should exist if calculated above

                 dist = min_dists[dist_key]
                 # Check if this f is closer than the current best_f
                 if dist < min_dist_for_s:
                      min_dist_for_s = dist
                      best_f = f
                 # If distance is the same, tie-break using lower color index
                 elif dist == min_dist_for_s:
                      if best_f == -1 or f < best_f:
                           best_f = f

            # Assign the determined mapping if a best fill was found
            if best_f != -1:
                 source_map[s] = best_f
            # else: If a source couldn't map (e.g., no PFDs reachable?), it won't fill.

    # Case 2: No PFDs exist - use identity map for sources
    else:
        for s in sources:
            source_map[s] = s

    return source_map


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the flood fill transformation based on derived source-fill mapping.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    h, w = input_grid_np.shape

    # Handle edge case of uniform grid or empty grid
    if h == 0 or w == 0 or len(np.unique(input_grid_np)) <= 1:
        return input_grid

    # 1. Identify Background Color
    background_color = find_background_color(input_grid_np)

    # 2. Derive Source-Fill Mapping
    source_fill_map = derive_source_fill_map(input_grid_np, background_color)

    # If no sources map to anything, return input as no fill can happen
    if not source_fill_map:
         return input_grid

    # Get the set of actual fill colors used in the map values
    fill_colors = set(source_fill_map.values())

    # 3. Initialize Output Grid
    output_grid_np = np.copy(input_grid_np)

    # 4. Iterative Flood Fill
    while True:
        changed = False
        # Create a grid for the next state based on the current 'output_grid_np'
        next_grid_np = np.copy(output_grid_np)

        for r in range(h):
            for c in range(w):
                current_color = output_grid_np[r, c] # Color in the *current* state

                # Store potential fill colors influencing (r,c) with their priority
                # We use the color index itself as priority (lower index = higher priority)
                potential_fills_priority = {} # {priority: color}

                # Check neighbors in the *current* state grid
                for nr, nc in get_neighbors(h, w, r, c):
                    neighbor_color = output_grid_np[nr, nc]

                    # Ignore background neighbors
                    if neighbor_color == background_color:
                        continue

                    fill_candidate = -1 # Reset for each neighbor

                    # Check if neighbor is a source -> find its fill color
                    if neighbor_color in source_fill_map:
                        fill_candidate = source_fill_map[neighbor_color]
                    # Check if neighbor is already a fill color itself
                    elif neighbor_color in fill_colors:
                         fill_candidate = neighbor_color

                    # If this neighbor provides a valid fill influence
                    if fill_candidate != -1:
                        priority = fill_candidate # Priority is the color index
                        # Store the candidate color if it's the best for this priority level found so far
                        # (Handles cases where multiple neighbors might map to the same fill)
                        # We only need the lowest color index for any given priority level.
                        if priority not in potential_fills_priority:
                             potential_fills_priority[priority] = fill_candidate
                        # This secondary check shouldn't be needed if priority == color index
                        # else:
                        #    potential_fills_priority[priority] = min(fill_candidate, potential_fills_priority[priority])


                # If any neighbor provided a fill influence for pixel (r,c)
                if potential_fills_priority:
                    # Find the highest priority (lowest index) winning fill color
                    winning_priority = min(potential_fills_priority.keys())
                    winning_fill_color = potential_fills_priority[winning_priority]

                    # Decide whether to update the pixel in the *next* grid state
                    # Case A: Current pixel is background
                    if current_color == background_color:
                        # Update if the calculated next state is different
                        if next_grid_np[r, c] != winning_fill_color:
                             next_grid_np[r, c] = winning_fill_color
                             changed = True
                    # Case B: Current pixel is not background
                    elif current_color != winning_fill_color: # Avoid self-overwrite checks
                        current_priority = current_color
                        # Update only if winning fill has strictly higher priority (lower index)
                        if winning_priority < current_priority:
                             if next_grid_np[r, c] != winning_fill_color:
                                 next_grid_np[r, c] = winning_fill_color
                                 changed = True
                        # If winning_priority >= current_priority, the existing color stays or wins.


        # Update the grid state for the next iteration
        output_grid_np = next_grid_np

        # If no pixels were changed in this full iteration, the process has stabilized
        if not changed:
            break

    # 5. Return the final grid state
    return output_grid_np.tolist()