
Previous Code:
```python
"""
Transforms an input grid by identifying enclosed white regions (color 0) and filling them based on the color of the single surrounding shape. The specific fill color applied depends on the total number of distinct non-white colors present in the entire input grid.

1.  **Analyze Grid Colors:** Count the number of unique non-white colors (`num_distinct_shape_colors`) in the input grid.
2.  **Identify White Regions:** Find contiguous areas of white pixels (0) using 8-way adjacency.
3.  **Determine Enclosure Status:** A white region is "enclosed" if:
    a.  It does not touch the grid border.
    b.  All immediately adjacent non-white pixels belong to a single shape and have the same color (`enclosing_color`).
4.  **Select Fill Mapping:** Choose a fill rule based on `num_distinct_shape_colors`:
    *   If `num_distinct_shape_colors` is 2 or less: Red(2) fills Green(3), Yellow(4) fills Orange(7).
    *   If `num_distinct_shape_colors` is 3 or more: Red(2) fills Orange(7), Yellow(4) fills Green(3). Regions enclosed by Orange(7) are *not* filled (remain white).
5.  **Apply Transformations:** Create a copy of the input grid. For each "enclosed" white region, determine the fill color using the selected mapping and the region's `enclosing_color`. Update the pixels within the region in the copied grid.
6.  **Return Output:** Return the modified grid.
"""

import numpy as np
from collections import deque

def find_enclosed_regions(grid: np.ndarray) -> list[tuple[set[tuple[int, int]], set[int], bool]]:
    """
    Identifies contiguous white regions and checks their enclosure status.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list where each element represents a white region and contains:
        - A set of (row, col) tuples for pixels in the region.
        - A set of adjacent non-white colors.
        - A boolean indicating if the region touches the border.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions_data = []

    for r in range(height):
        for c in range(width):
            # Start BFS for a new white region if not visited
            if grid[r, c] == 0 and not visited[r, c]:
                region_pixels = set()
                adjacent_colors = set()
                is_border_touching = False
                queue = deque([(r, c)])
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_pixels.add((curr_r, curr_c))

                    # Check if the current pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_border_touching = True

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if neighbor is within bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = grid[nr, nc]
                                if neighbor_color == 0: # Neighbor is white
                                    if not visited[nr, nc]:
                                        visited[nr, nc] = True
                                        queue.append((nr, nc))
                                else: # Neighbor is non-white (part of a potential enclosing shape)
                                    adjacent_colors.add(neighbor_color)
                            # else: neighbor is out of bounds, implies border touching for the region pixel
                            # This is implicitly handled by the border check on curr_r, curr_c

                regions_data.append((region_pixels, adjacent_colors, is_border_touching))

    return regions_data


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling enclosed white regions based on
    the color of the enclosing shape and the total number of distinct
    shape colors in the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()

    # 1. Analyze Grid Colors: Count distinct non-white colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # 4. Select Fill Mapping based on the count
    fill_map = {}
    if num_distinct_shape_colors <= 2:
        # Rule Set A (for 2 or fewer distinct colors)
        fill_map = {
            2: 3,  # Red -> Green
            4: 7,  # Yellow -> Orange
        }
    else:
        # Rule Set B (for 3 or more distinct colors)
        # Note: Orange(7) is intentionally left out based on Example 2 output
        fill_map = {
            2: 7,  # Red -> Orange
            4: 3,  # Yellow -> Green
            # 7: 3, # Removed based on failed test analysis
        }

    # 2. & 3. Identify White Regions and Determine Enclosure Status
    regions_data = find_enclosed_regions(grid)

    # 5. Apply Transformations
    for region_pixels, adjacent_colors, is_border_touching in regions_data:
        # Check enclosure criteria
        is_enclosed = (not is_border_touching) and (len(adjacent_colors) == 1)

        if is_enclosed:
            enclosing_color = list(adjacent_colors)[0]
            # Check if the enclosing color has a mapping in the selected rule set
            if enclosing_color in fill_map:
                fill_color = fill_map[enclosing_color]
                # Fill the region in the output grid
                for pr, pc in region_pixels:
                    output_grid[pr, pc] = fill_color
            # Else: If enclosing_color is not in the map (like Orange(7) in rule B),
            # the region remains white (0), no action needed as output_grid is a copy.

    # 6. Return Output
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 0 0 0 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Expected Output:
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Transformed Output:
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 2 2 2 2 2 2 2 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.204081632653043
