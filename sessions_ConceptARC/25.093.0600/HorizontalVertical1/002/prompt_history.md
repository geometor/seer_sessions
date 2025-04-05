
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

Okay, let's break down this task.

## Perception of Elements

1.  **Input/Output:** Both are 2D grids of integers, representing colored pixels. 0 typically represents the background color.
2.  **Core Transformation:** The primary change involves filling specific areas within the grid. These areas are initially color 0 (background).
3.  **Shapes:** The non-zero colors form distinct shapes or boundaries in the grid.
4.  **Enclosed Areas:** The transformation targets areas of color 0 that are completely surrounded or enclosed by a single, uniform non-zero color. These enclosed areas do not touch the boundary of the grid.
5.  **Filling:** Enclosed areas identified in step 4 are filled with a new color in the output grid.
6.  **Fill Colors:** The colors used for filling seem to be consistently 3 and 7 across the examples.
7.  **Fill Color Determination:** The specific fill color (3 or 7) used for an enclosed area depends on the color of the shape enclosing it *and* the overall set of non-zero colors present in the entire input grid. The rule seems to change based on how many distinct non-zero colors are present.
    *   If only two non-zero colors exist (e.g., {2, 4} in `train_1`), the lower color (2) encloses areas filled with 3, and the higher color (4) encloses areas filled with 7.
    *   If three non-zero colors exist (e.g., {2, 4, 7} in `train_2`), the lowest color (2) encloses areas filled with 7, the middle color (4) encloses areas filled with 3, and the highest color (7) also encloses areas filled with 3.
8.  **Integrity:** The original shapes (non-zero colors) and the background cells not part of an enclosed area remain unchanged in the output.

## YAML Facts


```yaml
elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - role: represents a colored canvas
  - object: cell
    properties:
      - value: integer color (0 = background, non-zero = shape color)
      - position: (row, column)
  - object: shape
    properties:
      - composition: connected cells of the same non-zero color
      - color: the specific non-zero integer value
  - object: background_region
    properties:
      - composition: connected cells of color 0
  - object: enclosed_region
    properties:
      - type: background_region
      - condition_1: does not touch the grid boundary
      - condition_2: all adjacent non-zero cells belong to a single shape (have the same 'boundary_color')
  - object: fill_color
    properties:
      - possible_values: [3, 7]
      - determination_rule: dependent on boundary_color and the set of all non-zero colors in the input grid

properties_ Mappings:
  - name: input_color_set
    description: The set of unique non-zero colors present in the input grid.
  - name: fill_assignment_rule
    description: A rule mapping a boundary_color to a fill_color (3 or 7).
    details:
      - case: if input_color_set has 2 colors {c1, c2} (c1<c2), map c1->3, c2->7.
      - case: if input_color_set has 3 colors {c1, c2, c3} (c1<c2<c3), map c1->7, c2->3, c3->3.

actions:
  - identify_unique_colors: Scan the input grid to find the set of unique non-zero colors.
  - establish_fill_map: Based on the identified unique colors, determine the specific fill color (3 or 7) for each potential boundary color according to the fill_assignment_rule.
  - detect_enclosed_regions:
      - Iterate through background (0) cells.
      - For each unvisited background cell, perform a search (like BFS/DFS) to find connected background cells.
      - During the search, track if the region touches the grid boundary and collect the colors of all adjacent non-zero cells.
      - If the region does not touch the boundary and all adjacent non-zero cells have the *same* color (the boundary_color), identify it as an enclosed_region.
  - apply_fill: For each detected enclosed_region, find its boundary_color, look up the corresponding fill_color from the established fill_map, and update the cells of the region in the output grid with this fill_color.
  - preserve_others: Copy all cells from the input to the output that are not part of a filled enclosed_region.

relationships:
  - adjacency: Cells sharing an edge (not just a corner) are adjacent.
  - connectivity: Cells of the same color form connected components/regions/shapes through adjacency.
  - enclosure: A shape encloses a background_region if the region is finite and all adjacent cells outside the region belong to that single shape.
  - dependency: The fill_color choice depends on both the local boundary_color and the global input_color_set.
```


## Natural Language Program

1.  **Prepare Output:** Create a new grid by copying the input grid.
2.  **Analyze Input Colors:** Find all unique non-zero integer colors present in the input grid. Store them in a sorted list, `unique_colors`.
3.  **Define Fill Mapping:** Create a mapping (dictionary) called `color_to_fill`.
    *   If `unique_colors` contains two colors, `c1` and `c2` (where `c1 < c2`): set `color_to_fill[c1] = 3` and `color_to_fill[c2] = 7`.
    *   If `unique_colors` contains three colors, `c1`, `c2`, and `c3` (where `c1 < c2 < c3`): set `color_to_fill[c1] = 7`, `color_to_fill[c2] = 3`, and `color_to_fill[c3] = 3`.
4.  **Identify and Fill Enclosed Regions:**
    a.  Keep track of visited background cells to avoid redundant checks (e.g., using a boolean grid `visited_zeros`).
    b.  Iterate through every cell `(r, c)` in the grid.
    c.  If `input[r][c]` is 0 and `visited_zeros[r][c]` is false:
        i.   Start a search (like BFS) from `(r, c)` to find all connected background cells forming a potential region.
        ii.  During the search, record all cells belonging to this region (`region_cells`), check if any cell touches the grid boundary (`touches_boundary`), and collect all unique non-zero colors adjacent to any cell in the region (`adjacent_colors`). Mark visited background cells in `visited_zeros`.
        iii. After the search for this connected component is complete: If `touches_boundary` is false and `adjacent_colors` contains exactly one color `b`, then `region_cells` represents an enclosed region.
        iv.  Retrieve the appropriate fill color `f = color_to_fill[b]`.
        v.   For every cell `(rr, cc)` in `region_cells`, update the output grid: `output[rr][cc] = f`.
5.  **Return Result:** Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
Identifies connected regions of background cells (color 0) that are fully enclosed by a single non-zero color and do not touch the grid boundary. 
These enclosed regions are then filled with a specific color (3 or 7) based on the enclosing color and the set of all non-zero colors present in the input grid.

1.  Determine the set of unique non-zero colors in the input grid.
2.  Establish a mapping from each non-zero color to a fill color (3 or 7):
    - If 2 unique non-zero colors {c1, c2} (c1 < c2) exist: map c1 -> 3, c2 -> 7.
    - If 3 unique non-zero colors {c1, c2, c3} (c1 < c2 < c3) exist: map c1 -> 7, c2 -> 3, c3 -> 3.
3.  Iterate through each cell of the grid.
4.  If a background cell (0) is found that hasn't been visited yet:
    a. Perform a Breadth-First Search (BFS) starting from this cell to find all connected background cells (a region).
    b. During the BFS, track:
        - All cells belonging to the region.
        - Whether any cell in the region touches the grid boundary.
        - The set of unique non-zero colors adjacent to the region.
    c. Mark all visited background cells during the BFS.
5.  After the BFS for a region is complete:
    a. If the region did *not* touch the boundary and was adjacent to exactly *one* unique non-zero color (the boundary color):
        i. Determine the appropriate fill color using the mapping established in step 2 based on the boundary color.
        ii. Fill all cells of this region in the output grid with the determined fill color.
6.  All other cells (original non-zero colors and background cells not part of a fillable enclosed region) remain unchanged.
"""

def _get_neighbors(r, c, rows, cols):
    """ Helper to yield valid neighbor coordinates. """
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def transform(input_grid):
    """
    Transforms the input grid by filling enclosed background regions based on boundary color rules.
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_array)
    rows, cols = input_array.shape

    # 1. Analyze Input Colors
    unique_colors = sorted(list(np.unique(input_array[input_array != 0])))

    # 2. Define Fill Mapping
    color_to_fill = {}
    if len(unique_colors) == 2:
        c1, c2 = unique_colors
        color_to_fill[c1] = 3
        color_to_fill[c2] = 7
    elif len(unique_colors) == 3:
        c1, c2, c3 = unique_colors
        color_to_fill[c1] = 7
        color_to_fill[c2] = 3
        color_to_fill[c3] = 3
    # Add handling for other numbers of colors if necessary, though examples only show 2 or 3.

    # 4. Identify and Fill Enclosed Regions
    visited_zeros = np.zeros_like(input_array, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            # 4.c If it's a background cell (0) and not visited yet:
            if input_array[r, c] == 0 and not visited_zeros[r, c]:
                # 4.c.i Start BFS
                queue = deque([(r, c)])
                visited_zeros[r, c] = True
                region_cells = []
                adjacent_colors = set()
                touches_boundary = False

                # 4.c.ii Perform BFS
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_cells.append((curr_r, curr_c))

                    # Check boundary touch
                    if curr_r == 0 or curr_r == rows - 1 or curr_c == 0 or curr_c == cols - 1:
                        touches_boundary = True

                    # Check neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                        neighbor_val = input_array[nr, nc]
                        if neighbor_val == 0:
                            if not visited_zeros[nr, nc]:
                                visited_zeros[nr, nc] = True
                                queue.append((nr, nc))
                        else: # Non-zero neighbor
                            adjacent_colors.add(neighbor_val)
                
                # 5. Check conditions and fill
                if not touches_boundary and len(adjacent_colors) == 1:
                    boundary_color = list(adjacent_colors)[0]
                    # 5.a.i Check if this boundary color has a defined fill rule
                    if boundary_color in color_to_fill:
                        fill_color = color_to_fill[boundary_color]
                        # 5.a.ii Fill the region in the output grid
                        for rr, cc in region_cells:
                            output_grid[rr, cc] = fill_color

    # Return the result as a list of lists
    return output_grid.tolist()
```
