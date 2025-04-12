import numpy as np
from collections import deque

"""
Transforms an input grid by conditionally filling enclosed white regions (color 0).

The transformation follows these steps:

1.  **Count Distinct Colors:** Determine the number of unique non-white colors (`num_distinct_shape_colors`) in the input grid.
2.  **Identify White Regions and Properties:** Find all contiguous white regions using 8-way adjacency. For each region, determine:
    a.  `touches_border`: If any pixel is on the grid edge.
    b.  `adjacent_non_white_colors`: The set of unique non-white colors adjacent (8-way) to the region.
    c.  `touches_external_white`: If any pixel in the region is adjacent (8-way) to a white pixel *not* belonging to the same contiguous region.
3.  **Determine Fill Rule:** Select a color mapping based on `num_distinct_shape_colors`:
    *   If <= 2 distinct colors: Rule A {Red(2): Green(3), Yellow(4): Orange(7)}.
    *   If >= 3 distinct colors: Rule B {Red(2): Orange(7), Yellow(4): Green(3), Orange(7): Green(3)}.
4.  **Fill Qualifying Regions:** Create a copy of the input. A region is filled if it meets ALL three conditions: (a) `touches_border` is False, (b) `adjacent_non_white_colors` has exactly one color, and (c) `touches_external_white` is True. If qualified, fill the region with the color mapped from its single adjacent non-white color using the selected rule.
5.  **Return Result:** The modified grid copy.
"""

def _find_white_regions_and_properties(grid: np.ndarray) -> list[tuple[set[tuple[int, int]], set[int], bool, bool]]:
    """
    Identifies contiguous white regions and their properties using BFS.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list where each element represents a white region and contains:
        - A set of (row, col) tuples for pixels in the region.
        - A set of adjacent non-white colors.
        - A boolean indicating if the region touches the border.
        - A boolean indicating if the region touches external white pixels.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions_data = []

    for r in range(height):
        for c in range(width):
            # Start BFS for a new white region if it's white and not visited
            if grid[r, c] == 0 and not visited[r, c]:
                region_pixels = set()
                adjacent_non_white_colors = set()
                region_touches_border = False
                queue = deque([(r, c)])
                visited[r, c] = True
                region_touches_external_white = False # Initialize for this region

                # --- BFS to find all pixels in the current region ---
                processed_in_bfs = set([(r,c)]) # Keep track of pixels added to queue/processed
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_pixels.add((curr_r, curr_c))

                    # Check if the current pixel touches the border
                    if not region_touches_border and (curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1):
                        region_touches_border = True

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc
                            neighbor_pos = (nr, nc)

                            # Check if neighbor is within bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = grid[nr, nc]

                                if neighbor_color == 0: # Neighbor is white
                                    # If white and not yet visited/queued for this region's BFS
                                    if not visited[nr, nc]:
                                        visited[nr, nc] = True
                                        processed_in_bfs.add(neighbor_pos)
                                        queue.append(neighbor_pos)
                                    # If white, but already visited (either by this BFS or a previous one)
                                    # AND it's not part of the current region's BFS exploration
                                    # -> this means it's an external white pixel adjacent to the current region boundary
                                    elif neighbor_pos not in processed_in_bfs:
                                        region_touches_external_white = True

                                elif neighbor_color > 0: # Neighbor is non-white
                                    adjacent_non_white_colors.add(neighbor_color)
                            # else: neighbor is out of bounds (implicitly handled by border check)

                # --- Correction for touches_external_white check ---
                # The BFS inherently finds all connected white pixels. If during the BFS of a region,
                # we encounter a neighbor that is white BUT already visited (meaning it belongs to
                # a *different* white region or the main background), then we have touched external white.
                # The previous logic checked this correctly within the loop.
                # Let's re-verify the logic more explicitly after the BFS.
                # (Alternative approach - less efficient but perhaps clearer):
                # After finding all region_pixels via BFS...
                # Check neighbors of all region_pixels again:
                # if neighbor is white AND neighbor not in region_pixels -> touches external white

                # --- Explicit check post-BFS (optional, previous logic might be sufficient) ---
                # if not region_touches_external_white: # Only run if not already found
                #     for pr, pc in region_pixels:
                #         for dr in [-1, 0, 1]:
                #             for dc in [-1, 0, 1]:
                #                 if dr == 0 and dc == 0: continue
                #                 nr, nc = pr + dr, pc + dc
                #                 if 0 <= nr < height and 0 <= nc < width:
                #                     if grid[nr, nc] == 0 and (nr, nc) not in region_pixels:
                #                         region_touches_external_white = True
                #                         break
                #         if region_touches_external_white: break


                # Store the collected data for this region
                regions_data.append((
                    region_pixels,
                    adjacent_non_white_colors,
                    region_touches_border,
                    region_touches_external_white # Use the flag set during BFS
                ))

    return regions_data


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by conditionally filling enclosed white regions.
    """
    # Initialize grid and output
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()

    # Step 1: Count Distinct Colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # Step 3: Determine Fill Rule
    fill_map = {}
    if num_distinct_shape_colors <= 2:
        # Rule Set A
        fill_map = {
            2: 3,  # Red -> Green
            4: 7,  # Yellow -> Orange
        }
    else:
        # Rule Set B
        fill_map = {
            2: 7,  # Red -> Orange
            4: 3,  # Yellow -> Green
            7: 3,  # Orange -> Green
        }

    # Step 2: Identify White Regions and Properties
    regions_data = _find_white_regions_and_properties(grid)

    # Step 4: Fill Qualifying Regions
    for region_pixels, adjacent_colors, touches_border, touches_external_white in regions_data:
        # Check the three conditions for filling
        is_fillable = (
            not touches_border and
            len(adjacent_colors) == 1 and
            touches_external_white
        )

        if is_fillable:
            enclosing_color = list(adjacent_colors)[0]
            # Check if the enclosing color has a mapping in the selected rule set
            if enclosing_color in fill_map:
                fill_color = fill_map[enclosing_color]
                # Fill the region in the output grid
                for pr, pc in region_pixels:
                    output_grid[pr, pc] = fill_color
            # Else: If enclosing_color is not in the map, region remains white (no action needed).

    # Step 5: Return Result
    return output_grid.tolist()