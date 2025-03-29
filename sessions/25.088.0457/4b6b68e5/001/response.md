```python
import numpy as np
from collections import deque, Counter

"""
Identifies closed shapes formed by a single non-white color (boundary color).
For each closed shape, it finds the region enclosed within it (interior region).
It then identifies all non-white pixels within the interior region that are *not* the boundary color (marker pixels).
If marker pixels exist, it determines the most frequent color among them. If there's a tie in frequency, the color with the highest numerical value is chosen.
Finally, it fills the entire interior region (including original white pixels and marker pixels) with this determined fill color.
Pixels belonging to the boundary, pixels outside any closed shape, and pixels inside shapes that are not closed remain unchanged.
"""

def find_shape(grid, start_r, start_c, visited_boundaries):
    """
    Finds a contiguous shape of a single color using BFS.
    Marks visited pixels in visited_boundaries.
    """
    H, W = grid.shape
    q = deque([(start_r, start_c)])
    shape_color = grid[start_r, start_c]
    shape_pixels = set()
    visited_boundaries[start_r, start_c] = shape_color # Mark with its own color
    shape_pixels.add((start_r, start_c))

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and \
               visited_boundaries[nr, nc] == 0 and \
               grid[nr, nc] == shape_color:
                visited_boundaries[nr, nc] = shape_color
                shape_pixels.add((nr, nc))
                q.append((nr, nc))
    return shape_pixels, shape_color

def find_reachable(grid, starts, impassable_pixels):
    """
    Finds all pixels reachable from start points without crossing impassable pixels using BFS.
    """
    H, W = grid.shape
    q = deque(starts)
    reachable = set(starts)
    visited = np.zeros((H,W), dtype=bool) # Track visited for this specific flood fill

    for r, c in starts:
         if 0 <= r < H and 0 <= c < W:
            visited[r,c] = True

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and \
               not visited[nr, nc] and \
               (nr, nc) not in impassable_pixels:
                visited[nr, nc] = True
                reachable.add((nr, nc))
                q.append((nr, nc))
    return reachable


def transform(input_grid):
    """
    Transforms the input grid by finding enclosed regions within single-color boundaries
    and flood-filling them based on the most frequent internal marker color.
    """
    H, W = input_grid.shape
    output_grid = np.copy(input_grid)
    visited_boundaries = np.zeros_like(input_grid, dtype=int) # 0=not visited, >0=boundary color

    # Iterate through grid to find potential boundaries
    for r in range(H):
        for c in range(W):
            # If it's a non-white pixel and not yet part of an identified boundary
            if input_grid[r, c] != 0 and visited_boundaries[r, c] == 0:
                # 1. Find the complete boundary shape
                boundary_pixels, boundary_color = find_shape(input_grid, r, c, visited_boundaries)

                # 2. Determine the exterior region reachable from grid edges without crossing the current boundary
                edge_starts = []
                for i in range(H):
                    if (i, 0) not in boundary_pixels: edge_starts.append((i, 0))
                    if (i, W - 1) not in boundary_pixels: edge_starts.append((i, W - 1))
                for j in range(W):
                     if (0, j) not in boundary_pixels: edge_starts.append((0, j))
                     if (H - 1, j) not in boundary_pixels: edge_starts.append((H - 1, j))

                exterior_pixels = find_reachable(input_grid, edge_starts, boundary_pixels)

                # 3. Identify potential interior pixels (not boundary, not exterior)
                potential_interior_pixels = set()
                all_pixels = set((ir, ic) for ir in range(H) for ic in range(W))
                potential_interior_pixels = all_pixels - boundary_pixels - exterior_pixels

                # If there are potential interior pixels, they form the interior region(s)
                if potential_interior_pixels:
                    # Note: This assumes a single connected interior for a single boundary shape.
                    # Complex shapes might require processing connected components of potential_interior_pixels.
                    # However, ARC tasks often involve simple closed shapes.
                    interior_region_pixels = potential_interior_pixels

                    # 4. Collect marker colors from the *input* grid within the interior region
                    marker_colors = []
                    for ir, ic in interior_region_pixels:
                        pixel_color = input_grid[ir, ic]
                        if pixel_color != 0 and pixel_color != boundary_color:
                            marker_colors.append(pixel_color)

                    # 5. Determine fill color if markers exist
                    if marker_colors:
                        color_counts = Counter(marker_colors)
                        # Find the max frequency
                        max_freq = 0
                        for color in color_counts:
                           if color_counts[color] > max_freq:
                               max_freq = color_counts[color]

                        # Find colors with max frequency
                        candidate_colors = [color for color, count in color_counts.items() if count == max_freq]

                        # Choose the one with the highest numerical value if tied
                        fill_color = max(candidate_colors)

                        # 6. Fill the interior region in the output grid
                        for ir, ic in interior_region_pixels:
                            output_grid[ir, ic] = fill_color
                    else:
                        # If no markers, fill with white (0) or leave as is?
                        # Examples suggest filling based on markers. If no markers,
                        # what happens? Example 1 top-right shape has no markers, remains white.
                        # Example 3 has internal white and markers, all get filled.
                        # Let's assume if no markers, interior remains as is (which includes white).
                        # The code currently does this implicitly by only filling if markers exist.
                        # Let's explicitly fill white regions with white if no markers are present?
                        # No, the description says "fill the *entire* interior region ... with this determined fill color".
                        # This implies *if* a fill color is determined, *then* fill everything inside.
                        # If no markers, no fill color determined, so region stays as is. This matches Example 1.
                        pass


    return output_grid
```