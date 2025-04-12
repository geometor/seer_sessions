"""
Identifies enclosed white regions (color 0) within an input grid and fills them based on specific criteria and rules.

The transformation involves the following steps:

1.  **Analyze Grid Colors:** Determine the number of unique non-white colors (`num_distinct_shape_colors`) present in the input grid.
2.  **Identify White Regions and Properties:**
    *   Find all contiguous regions of white pixels using 8-way adjacency.
    *   For each white region, determine:
        *   `touches_border`: Whether any pixel in the region lies on the grid's outer edge.
        *   `adjacent_non_white_colors`: The set of unique colors of non-white pixels adjacent (8-way) to the region.
        *   `touches_external_white`: Whether any pixel in the region is adjacent (8-way) to a white pixel that is *not* part of the same contiguous region.
3.  **Select Fill Mapping Rule:** Choose a color transformation map based on `num_distinct_shape_colors`:
    *   **Rule A (<= 2 distinct colors):** Red(2) -> Green(3), Yellow(4) -> Orange(7).
    *   **Rule B (>= 3 distinct colors):** Red(2) -> Orange(7), Yellow(4) -> Green(3), Orange(7) -> Green(3).
4.  **Apply Conditional Filling:**
    *   A white region is filled *only if* all three conditions are met:
        1.  `touches_border` is False.
        2.  `adjacent_non_white_colors` contains exactly one color.
        3.  `touches_external_white` is True.
    *   If all conditions are met, the region is filled with the color determined by the selected fill rule and the single adjacent non-white color.
    *   Otherwise, the region remains white.
5.  **Output:** Return the modified grid.
"""

import numpy as np
from collections import deque

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
    all_white_pixels = set(zip(*np.where(grid == 0))) # Pre-calculate all white pixel locations

    for r in range(height):
        for c in range(width):
            # Start BFS for a new white region if it's white and not visited
            if grid[r, c] == 0 and not visited[r, c]:
                region_pixels = set()
                adjacent_non_white_colors = set()
                region_touches_border = False
                queue = deque([(r, c)])
                visited[r, c] = True

                # --- BFS to find all pixels in the current region ---
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

                            # Check if neighbor is within bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = grid[nr, nc]
                                neighbor_pos = (nr, nc)

                                if neighbor_color == 0: # Neighbor is white
                                    if not visited[nr, nc]:
                                        visited[nr, nc] = True
                                        queue.append(neighbor_pos)
                                # else: Neighbor is non-white
                                elif neighbor_color > 0:
                                    adjacent_non_white_colors.add(neighbor_color)
                # --- End of BFS for the current region ---

                # --- Check if region touches external white pixels ---
                region_touches_external_white = False
                for pr, pc in region_pixels:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = pr + dr, pc + dc
                            neighbor_pos = (nr, nc)
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is white AND not part of the current region
                                if grid[nr, nc] == 0 and neighbor_pos not in region_pixels:
                                     # Optimization: If neighbor is white and outside the current region, it MUST be external white
                                     # because all white pixels connected to the starting point were already added to region_pixels by BFS.
                                     region_touches_external_white = True
                                     break # Found one external white neighbor, no need to check more for this pixel
                    if region_touches_external_white:
                        break # Found one external white neighbor for the whole region, no need to check more pixels

                # Store the collected data for this region
                regions_data.append((
                    region_pixels,
                    adjacent_non_white_colors,
                    region_touches_border,
                    region_touches_external_white
                ))

    return regions_data


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by conditionally filling enclosed white regions.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Initialize grid and output
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()

    # 1. Analyze Grid Colors: Count distinct non-white colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # 3. Select Fill Mapping Rule based on the count
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
            7: 3,  # Orange -> Green (Reinstated)
        }

    # 2. Identify White Regions and Properties
    regions_data = _find_white_regions_and_properties(grid)

    # 4. Apply Conditional Filling
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
            # Else: If enclosing_color is not in the map, region remains white.

    # 5. Return Output
    return output_grid.tolist()