
## train_1

**input:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 7 7 7 7 0
0 3 0 0 3 0 0 7 0 7 7 0
0 0 3 0 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 0 7 7 0
0 0 3 3 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 0 0 8 0 0
6 8 0 0 8 0 0 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```


**output:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 5 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 5 4
0 0 0 0 0 0 0 4 4 4
```


## train_3

**input:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 0 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 0 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```


**output:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```

Okay, let's break down the transformation.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are grids of digits (0-9).
2.  **Objects:** The primary objects are contiguous regions (connected components) of identical non-zero digits. Let's call these "shapes". The digit forming the shape boundary is the "border color". The digit `0` typically represents the background or empty space.
3.  **Action:** The core action is filling certain areas of `0`s within the grid with a specific non-zero digit.
4.  **Target Areas:** The `0`s being filled are those located in the "interior" of a shape. A `0` is considered interior if it's completely surrounded by the shape's border color, meaning a path of `0`s starting from that cell cannot reach the edge of the grid without passing through the border color. Shapes that are "open" (their interior `0`s can reach the grid edge via other `0`s) are not filled (e.g., the '5' shape in train_2).
5.  **Fill Color Determination:** The color used to fill the interior depends primarily on the border color (`C`) of the shape being filled.
    *   For some border colors (3 and 7), the fill color is the same as the border color.
    *   For other border colors (2 and 8), there seems to be a fixed mapping to a different fill color (2->7, 8->1).
    *   For border color 4, the fill color depends on the *other* shapes present in the grid. Specifically, it seems related to the minimum border color among the other shapes.
    *   For border color 5, no filling occurred (though the example shape was also open).
6.  **No Change:** Cells that are not interior `0`s of a shape remain unchanged.

**YAML Facts:**

```yaml
elements:
  - element: grid
    properties:
      - type: 2D array of integers (0-9)
      - size: variable (rows x columns)
  - element: cell
    properties:
      - value: integer (0-9)
      - position: (row, column)
  - element: shape
    properties:
      - type: connected component of identical non-zero cells
      - border_color: integer (C > 0)
      - cells: list of cell positions
      - interior_zeros: list of cell positions (value 0) fully enclosed by the shape's border_color cells (cannot reach grid boundary via 0-valued cells)
  - element: fill_color
    properties:
      - value: integer (F > 0)
relationships:
  - type: spatial
    description: Cells are adjacent (orthogonally and diagonally). Shapes occupy specific regions of the grid. Interior zeros are enclosed by a shape.
actions:
  - action: identify_shapes
    input: grid
    output: list of shapes (with border_color, cells)
  - action: find_interior_zeros
    input: shape, grid
    output: list of interior_zero positions for that shape
  - action: determine_fill_color
    input: shape (border_color C), all_shapes
    output: fill_color F or None
    logic:
      - Based on C:
        - C=3 -> F=3
        - C=7 -> F=7
        - C=8 -> F=1
        - C=2 -> F=7
        - C=4 -> depends on minimum border_color (min_obd) of *other* shapes:
          - if min_obd = 5 -> F=5
          - if min_obd = 3 -> F=6
          - otherwise -> F=None (no fill)
        - C=5 -> F=None (no fill)
        - Other C -> Undefined by examples (assume F=None or F=C)
  - action: fill_grid
    input: grid, shape, interior_zeros, fill_color F
    output: modified grid
    condition: F is not None and interior_zeros is not empty
    effect: Changes the value of interior_zero cells to F
```

**Natural Language Program:**

1.  Iterate through the input grid to identify all distinct connected components ("shapes") formed by identical non-zero digits. Record the border color (`C`) and the cell coordinates for each shape.
2.  For each identified shape:
    a.  Determine the set of interior `0` cells. An interior `0` cell is one from which a path consisting only of `0` cells cannot reach any cell on the boundary of the grid. This can be found using a flood-fill algorithm starting from `0` cells adjacent to the shape's border cells, marking all reachable `0`s that do not hit the boundary. Alternatively, flood-fill from all boundary `0`s and mark reachable `0`s; any remaining unmarked `0`s are interior.
    b.  If the shape has no interior `0` cells, proceed to the next shape.
    c.  Determine the fill color (`F`) based on the shape's border color (`C`):
        i.  If `C` is 3, set `F` to 3.
        ii. If `C` is 7, set `F` to 7.
        iii.If `C` is 8, set `F` to 1.
        iv. If `C` is 2, set `F` to 7.
        v.  If `C` is 4:
            1.  Find all *other* shapes in the grid.
            2.  Collect their border colors into a set.
            3.  If the set of other border colors is empty, do not assign a fill color (`F` remains undetermined).
            4.  Otherwise, find the minimum value (`min_obd`) in the set of other border colors.
            5.  If `min_obd` is 5, set `F` to 5.
            6.  Else if `min_obd` is 3, set `F` to 6.
            7.  Otherwise (if `min_obd` is not 5 or 3), do not assign a fill color (`F` remains undetermined).
        vi. If `C` is 5 (or any other digit not specified above), do not assign a fill color (`F` remains undetermined).
    d.  If a fill color `F` was determined in the previous step, change the value of all identified interior `0` cells for the current shape to `F` in the output grid.
3.  Return the modified grid.
```python
import copy
import collections

"""
Identifies connected components (shapes) of identical non-zero digits in the input grid.
For each shape, it determines if it encloses any regions of zeros (interior zeros).
An interior zero region is one that cannot reach the grid boundary by moving only through other zeros.
If a shape encloses interior zeros, a fill color is determined based on the shape's border color (C):
- C=3 -> Fill=3
- C=7 -> Fill=7
- C=8 -> Fill=1
- C=2 -> Fill=7
- C=4 -> Fill depends on the minimum border color (min_obd) of *other* shapes in the grid:
    - If min_obd=5, Fill=5
    - If min_obd=3, Fill=6
    - Otherwise, no fill.
- C=5 (or others) -> No fill.
The identified interior zero cells are then filled with the determined fill color in the output grid.
Cells not part of an enclosed zero region remain unchanged.
"""

def find_shapes(grid: list[list[int]]) -> list[dict]:
    """
    Finds all connected components of identical non-zero digits.

    Args:
        grid: The input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a shape
        and contains 'color' (the digit) and 'cells' (a set of (row, col) tuples).
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    shapes = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                shape_cells = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                shape_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check orthogonal and diagonal neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and grid[nr][nc] == color:
                                visited.add((nr, nc))
                                shape_cells.add((nr, nc))
                                q.append((nr, nc))
                shapes.append({'color': color, 'cells': shape_cells})
    return shapes

def find_interior_zeros(grid: list[list[int]], shape_cells: set) -> set:
    """
    Finds zero cells that are enclosed by the given shape.

    Args:
        grid: The input grid.
        shape_cells: A set of (row, col) tuples representing the cells of a single shape.

    Returns:
        A set of (row, col) tuples representing the interior zero cells enclosed by the shape.
    """
    rows = len(grid)
    cols = len(grid[0])
    potential_interior = set()
    q = collections.deque()
    visited_zeros = set() # Zeros visited during any BFS starting from shape adjacency

    # 1. Find initial zero neighbors of the shape
    for r_s, c_s in shape_cells:
        # Only check orthogonal neighbors for starting the zero search
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r_s + dr, c_s + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    potential_interior.add((nr, nc))

    interior_zeros = set()

    # 2. For each connected component of potential interior zeros, check if it reaches the boundary
    for r_init, c_init in potential_interior:
        if (r_init, c_init) in visited_zeros:
            continue

        component_zeros = set()
        q_zeros = collections.deque([(r_init, c_init)])
        visited_zeros.add((r_init, c_init))
        component_zeros.add((r_init, c_init))
        reaches_boundary = False

        while q_zeros:
            r, c = q_zeros.popleft()

            # Check if this zero touches the boundary
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                reaches_boundary = True
                # Optimization: if one cell reaches boundary, the whole component does.
                # No need to break here, let the BFS complete to mark all visited.

            # Explore neighbors (orthogonal only for zero-path finding)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and \
                   grid[nr][nc] == 0 and (nr, nc) not in visited_zeros:
                    visited_zeros.add((nr, nc))
                    component_zeros.add((nr, nc))
                    q_zeros.append((nr, nc))

        # If the component did not reach the boundary, add its cells to interior_zeros
        if not reaches_boundary:
            interior_zeros.update(component_zeros)

    return interior_zeros


def determine_fill_color(shape_color: int, all_shapes: list[dict], current_shape_cells: set) -> int | None:
    """
    Determines the fill color based on the shape's color and other shapes present.

    Args:
        shape_color: The color (digit) of the current shape.
        all_shapes: A list of all shapes found in the grid.
        current_shape_cells: The cells of the current shape (to exclude it when finding 'other' shapes).

    Returns:
        The fill color (int) or None if no fill should occur.
    """
    if shape_color == 3:
        return 3
    if shape_color == 7:
        return 7
    if shape_color == 8:
        return 1
    if shape_color == 2:
        return 7
    if shape_color == 4:
        other_border_colors = set()
        for shape in all_shapes:
            # Check if it's a different shape instance
            if shape['cells'] != current_shape_cells:
                 other_border_colors.add(shape['color'])

        if not other_border_colors:
            return None # No other shapes

        min_obd = min(other_border_colors)
        if min_obd == 5:
            return 5
        if min_obd == 3:
            return 6
        else:
            return None # Min other border color is not 5 or 3
    # Default case (includes C=5 and any other unspecified colors)
    return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying shapes, finding their enclosed
    interior zeros, determining the correct fill color based on specific rules,
    and filling those zeros.

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        A new 2D list representing the transformed grid.
    """
    # initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    if not input_grid or not input_grid[0]:
        return output_grid # Handle empty grid case
    rows = len(input_grid)
    cols = len(input_grid[0])

    # 1. Identify all shapes in the grid
    all_shapes = find_shapes(input_grid)

    # 2. Process each shape
    for shape in all_shapes:
        shape_color = shape['color']
        shape_cells = shape['cells']

        # 3. Find interior zeros for the current shape
        # Need to pass the original grid state for finding zeros correctly
        interior_zeros = find_interior_zeros(input_grid, shape_cells)

        if not interior_zeros:
            continue # No interior zeros for this shape

        # 4. Determine the fill color
        fill_color = determine_fill_color(shape_color, all_shapes, shape_cells)

        # 5. Fill the interior zeros in the output grid if a fill color was determined
        if fill_color is not None:
            for r, c in interior_zeros:
                # Ensure we only fill actual zeros (safety check)
                if output_grid[r][c] == 0:
                     output_grid[r][c] = fill_color

    return output_grid
```
