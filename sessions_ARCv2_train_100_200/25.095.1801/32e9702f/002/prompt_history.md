
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5
5 3 3 3 3 5 5 5
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
3 3 5 5 5 5 5 5
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
4 4 4
0 0 0
0 0 0
```


**output:**
```
4 4 5
5 5 5
5 5 5
```


## train_3

**input:**
```
7 7 7 7 0 0 0
0 0 0 0 0 0 0
0 0 7 7 7 0 0
0 0 0 0 0 0 0
0 7 7 7 7 7 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
7 7 7 5 5 5 5
5 5 5 5 5 5 5
5 7 7 7 5 5 5
5 5 5 5 5 5 5
7 7 7 7 7 5 5
5 5 5 5 5 5 5
5 5 5 5 5 5 5
```

Okay, let's break down the transformation logic based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** The task operates on 2D grids where each cell contains a single digit (0-9), likely representing colors or states. Input and output grids maintain the same dimensions for each example.
2.  **Background Color:** Color 0 consistently acts as a background element in the input grids.
3.  **Foreground Objects:** Non-zero digits (3, 4, 7 in the examples) represent foreground objects or patterns, often forming connected horizontal lines or simple shapes.
4.  **Transformation Goal:** The primary goal seems to be replacing the background color (0) with a new color (5).
5.  **Conditional Modification:** A secondary transformation modifies certain foreground cells (non-zero digits) by changing them to color 5, based on specific conditions related to their position and the structure they belong to.

**Facts (YAML):**


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2
  cell_content: digits (0-9)
  input_output_size_relation: identical
objects:
  - object: cell
    properties:
      - value: digit (color)
      - position: (row, column)
  - object: grid
    properties:
      - dimensions: (height, width)
      - cells: collection of cell objects
  - object: connected_component
    properties:
      - color: non-zero digit
      - cells: set of connected cells with the same color (using 4-way adjacency)
      - location: position within the grid (e.g., bounding box, specific rows/columns)
      - features:
          - resides_in_first_row: boolean
          - rightmost_cell_position: (row, column)
actions:
  - action: replace_value
    target: cell
    conditions:
      - initial_value == 0
    new_value: 5
  - action: replace_value
    target: cell
    conditions:
      - initial_value != 0
      - cell belongs to a connected_component
      - connected_component.resides_in_first_row == true
      - cell position == connected_component.rightmost_cell_position
    new_value: 5
relationships:
  - relationship: adjacency
    between: cell, cell
    type: 4-way (up, down, left, right)
  - relationship: membership
    between: cell, connected_component
constants:
  - background_color: 0
  - replacement_color: 5
  - target_row_index: 0
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through each cell of the input grid. If a cell's value is 0, change the corresponding cell's value in the output grid to 5.
3.  Identify all distinct connected components formed by non-zero colored cells in the input grid (using 4-way adjacency).
4.  For each identified non-zero connected component:
    a.  Check if all cells belonging to this component are located in the first row (row index 0).
    b.  If the component is entirely within the first row, find the cell within that component that has the largest column index (the "rightmost" cell).
    c.  Change the value of this specific rightmost cell in the output grid to 5.
5.  All other non-zero cells (those not part of a component entirely in the first row, or those part of such a component but not the rightmost cell) retain their original value in the output grid.
6.  Return the modified output grid.
```python
import copy

"""
1. Create a copy of the input grid to serve as the output grid.
2. Iterate through each cell of the input grid. If a cell's value is 0, change the corresponding cell's value in the output grid to 5.
3. Identify all distinct connected components formed by non-zero colored cells in the input grid (using 4-way adjacency).
4. For each identified non-zero connected component:
    a. Check if all cells belonging to this component are located in the first row (row index 0).
    b. If the component is entirely within the first row, find the cell within that component that has the largest column index (the "rightmost" cell).
    c. Change the value of this specific rightmost cell in the output grid to 5.
5. All other non-zero cells (those not part of a component entirely in the first row, or those part of such a component but not the rightmost cell) retain their original value in the output grid.
6. Return the modified output grid.
"""

def _find_connected_components(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-zero cells in the grid using 4-way adjacency.

    Args:
        grid: The input grid.

    Returns:
        A list of components, where each component is a list of (row, col) tuples.
    """
    if not grid or not grid[0]:
        return []

    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # If cell is non-zero and not yet visited, start a search (BFS)
            if grid[r][c] != 0 and (r, c) not in visited:
                component_color = grid[r][c]
                current_component = []
                queue = [(r, c)]
                visited.add((r, c))

                while queue:
                    row, col = queue.pop(0)
                    current_component.append((row, col))

                    # Check neighbors (4-way adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if it has the same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] == component_color and \
                           (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))

                components.append(current_component)

    return components


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the specified rules:
    - Replaces background color 0 with 5.
    - For non-zero components located entirely in the first row,
      replaces the rightmost cell of the component with 5.
    """
    # 1. Create a copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # 2. Replace background color 0 with 5
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:
                output_grid[r][c] = 5

    # 3. Identify all distinct non-zero connected components
    components = _find_connected_components(input_grid)

    # 4. Process each component
    for component in components:
        if not component: continue # Skip if component is empty (should not happen with current logic)

        # 4a. Check if all cells are in the first row (row index 0)
        is_in_first_row = all(r == 0 for r, c in component)

        if is_in_first_row:
            # 4b. Find the rightmost cell (largest column index)
            rightmost_cell = max(component, key=lambda item: item[1])
            rm_r, rm_c = rightmost_cell

            # 4c. Change the value of this rightmost cell to 5 in the output grid
            output_grid[rm_r][rm_c] = 5

    # 5. Other non-zero cells already retain their original values due to the initial copy.
    # 6. Return the modified output grid
    return output_grid
```
