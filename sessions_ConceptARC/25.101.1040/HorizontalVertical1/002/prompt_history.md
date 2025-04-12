
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
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


**output:**
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

Okay, let's analyze the task based on the provided examples.

**Perception**

The input grids contain one or more distinct, closed shapes made of non-white pixels (Red, Yellow, Orange) on a white background. These shapes enclose regions of the white background pixels. The core transformation involves identifying these enclosed white regions and filling them with a new color. The specific color used for filling depends on the color of the shape that encloses the region. Crucially, the rule mapping the enclosing color to the fill color appears to change based on the *total number of distinct non-white colors* present in the shapes within the input grid.

In the first example, there are two distinct shape colors (Red, Yellow). Red shapes enclose areas filled with Green, and Yellow shapes enclose areas filled with Orange.

In the second example, there are three distinct shape colors (Red, Yellow, Orange). Here, Red shapes enclose areas filled with Orange, Yellow shapes enclose areas filled with Green, and Orange shapes enclose areas filled with Green.

This suggests two different color-filling rules, selected based on whether two or three (or more) distinct non-white colors form the shapes in the input grid.

**Facts**


```yaml
elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: background
    properties:
      - color: white (0)
  - type: shape
    description: A contiguous block of non-white pixels.
    properties:
      - color: [red (2), yellow (4), orange (7), ...]
      - connectivity: Assumed 8-way adjacency for shape pixels.
  - type: enclosed_region
    description: A contiguous region of white (0) pixels that does not touch the grid border and is entirely surrounded by pixels of a single shape/color.
    properties:
      - color: white (0)
      - connectivity: Assumed 8-way adjacency for region pixels.
      - status: enclosed (boolean)
      - enclosing_color: The color of the single shape surrounding the region.
      - border_touching: (boolean) True if any pixel is on the grid edge.

grid_properties:
  - name: distinct_shape_colors
    description: The set of unique non-white colors present in the shapes of the input grid.
  - name: num_distinct_shape_colors
    description: The count of unique non-white colors.

transformation:
  - action: identify_shapes
    description: Locate all contiguous non-white shapes.
  - action: count_distinct_colors
    description: Determine the number of unique colors used in the identified shapes.
  - action: identify_white_regions
    description: Locate all contiguous white (0) regions.
  - action: check_enclosure
    description: For each white region, determine if it is enclosed.
    criteria:
      - Must not touch the grid border.
      - All adjacent (8-way) non-white pixels must belong to a single shape and have the same color.
  - action: determine_enclosing_color
    description: Identify the color of the shape enclosing a white region.
  - action: apply_fill_rule
    description: Select a fill color based on the enclosing color and the total number of distinct shape colors in the grid.
    rules:
      - condition: num_distinct_shape_colors <= 2
        mapping:
          - input_color: red (2)
            output_color: green (3)
          - input_color: yellow (4)
            output_color: orange (7)
          # Add other colors if observed in more examples
      - condition: num_distinct_shape_colors >= 3
        mapping:
          - input_color: red (2)
            output_color: orange (7)
          - input_color: yellow (4)
            output_color: green (3)
          - input_color: orange (7)
            output_color: green (3)
          # Add other colors if observed in more examples
  - action: fill_region
    description: Change the color of the pixels within an enclosed white region to the determined fill color.

output_constraints:
  - The grid dimensions remain unchanged.
  - The original shapes remain unchanged in color and position.
  - Only the enclosed white regions are modified.
  - Background pixels not part of an enclosed region remain white.
```


**Natural Language Program**

1.  **Analyze Input Shapes:** Identify all contiguous shapes formed by non-white pixels in the input grid. Determine the set of unique colors present in these shapes and count how many distinct colors there are (`num_distinct_shape_colors`).
2.  **Identify Candidate Regions:** Find all contiguous regions of white (0) pixels in the input grid.
3.  **Check for Enclosure:** For each white region identified:
    a.  Verify that no pixel in the region lies on the border of the grid.
    b.  Examine all pixels directly adjacent (including diagonals) to the white region.
    c.  Confirm that all adjacent pixels that are *not* white share the exact same single color (`enclosing_color`).
    d.  If both conditions (a and c) are met, the white region is considered "enclosed".
4.  **Determine Fill Rule:** Based on the `num_distinct_shape_colors` calculated in step 1:
    a.  If `num_distinct_shape_colors` is 2 or less, use Rule Set A: Red(2) fills Green(3), Yellow(4) fills Orange(7).
    b.  If `num_distinct_shape_colors` is 3 or more, use Rule Set B: Red(2) fills Orange(7), Yellow(4) fills Green(3), Orange(7) fills Green(3).
5.  **Apply Filling:** Create a copy of the input grid to serve as the output. For every white region identified as "enclosed" in step 3:
    a.  Determine the appropriate `fill_color` using the selected Rule Set (A or B) and the `enclosing_color` found in step 3c.
    b.  Change the color of all pixels within that enclosed region to the determined `fill_color` in the output grid.
6.  **Finalize Output:** Return the modified grid. Pixels that were not part of an enclosed white region retain their original color from the input grid.
```python
import numpy as np
from collections import deque

"""
Identifies enclosed regions of white pixels (0) within the input grid and fills them based on the color of the enclosing shape.

The fill color depends on the number of distinct non-white colors present in the shapes across the entire grid:

1.  **Count Distinct Shape Colors:** Determine the number of unique non-white colors (1-9) present in the input grid.
2.  **Identify White Regions:** Find contiguous regions of white pixels (0).
3.  **Check for Enclosure:** A white region is considered "enclosed" if:
    a. It does not touch the border of the grid.
    b. All adjacent non-white pixels surrounding the region belong to a single shape and have the same color.
4.  **Apply Fill Rule:**
    *   **If 2 or fewer distinct shape colors exist:**
        *   Regions enclosed by Red (2) are filled with Green (3).
        *   Regions enclosed by Yellow (4) are filled with Orange (7).
        *   (Other color mappings might exist but are not shown in examples).
    *   **If 3 or more distinct shape colors exist:**
        *   Regions enclosed by Red (2) are filled with Orange (7).
        *   Regions enclosed by Yellow (4) are filled with Green (3).
        *   Regions enclosed by Orange (7) are filled with Green (3).
        *   (Other color mappings might exist but are not shown in examples).
5.  **Output:** Return the modified grid with enclosed regions filled according to the rules. Shapes and unenclosed areas remain unchanged.
"""


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
    height, width = grid.shape
    output_grid = grid.copy()
    visited = np.zeros_like(grid, dtype=bool)

    # 1. Count Distinct Shape Colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # 4. Determine Fill Rule based on the count
    fill_map = {}
    if num_distinct_shape_colors <= 2:
        # Rule Set A (for 2 or fewer distinct colors)
        fill_map = {
            2: 3,  # Red -> Green
            4: 7,  # Yellow -> Orange
            # Add other rules if needed based on more examples
        }
    else:
        # Rule Set B (for 3 or more distinct colors)
        fill_map = {
            2: 7,  # Red -> Orange
            4: 3,  # Yellow -> Green
            7: 3,  # Orange -> Green
             # Add other rules if needed based on more examples
        }

    # 2. & 3. Identify White Regions and Check for Enclosure
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited[r, c]:
                # Start BFS for a potential white region
                region_pixels = set()
                adjacent_colors = set()
                is_border_touching = False
                queue = deque([(r, c)])
                visited[r, c] = True
                valid_region = True # Assume valid until proven otherwise

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
                                else: # Neighbor is non-white (part of a shape)
                                    adjacent_colors.add(neighbor_color)
                            else:
                                # Neighbor is out of bounds - this shouldn't happen if border check works
                                # but good for robustness
                                pass

                # 3. Final check for enclosure after exploring the whole region
                is_enclosed = (not is_border_touching) and (len(adjacent_colors) == 1)

                # 5. Apply Filling if enclosed
                if is_enclosed:
                    enclosing_color = list(adjacent_colors)[0]
                    if enclosing_color in fill_map:
                        fill_color = fill_map[enclosing_color]
                        for pr, pc in region_pixels:
                            output_grid[pr, pc] = fill_color
                    # else: keep original color (white) if no mapping exists


    return output_grid.tolist()
```
