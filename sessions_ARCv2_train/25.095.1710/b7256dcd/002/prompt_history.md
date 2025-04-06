
## train_1

**input:**
```
7 6 6 3 7
7 7 7 4 7
7 7 7 6 7
7 7 6 6 6
7 7 7 6 7
```


**output:**
```
7 3 3 7 7
7 7 7 7 7
7 7 7 4 7
7 7 4 4 4
7 7 7 4 7
```


## train_2

**input:**
```
7 7 7 6
3 7 6 6
7 7 6 7
7 7 7 7
1 6 6 6
7 7 6 7
```


**output:**
```
7 7 7 6
7 7 6 6
7 7 6 7
7 7 7 7
7 1 1 1
7 7 1 7
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are 2D grids of integers. The size of the grid can vary (5x5 in train_1, 6x4 in train_2).
2.  **Cell Values:** The grids contain integer values. The number 7 appears frequently and seems to act as a stable background or boundary element; it never changes its value or position.
3.  **Active Elements:** Numbers other than 7 (e.g., 1, 3, 4, 6) are the ones subject to transformation.
4.  **Connectivity:** The transformation appears to operate on connected components of non-7 numbers. Connectivity is defined by adjacent cells (up, down, left, right - Von Neumann neighborhood). A component is a group of non-7 cells where you can reach any cell in the group from any other cell by moving between adjacent non-7 cells.
5.  **Transformation Logic:** The final value of a cell depends on the properties of the connected component it belongs to. Key properties identified are:
    *   The size (number of cells) of the component.
    *   The set of unique numbers present within the component.
    *   The minimum numerical value within the component.
6.  **Specific Rules Observed:**
    *   Components of size 1 change to 7.
    *   Components containing only the number 6 change based on size (size 4 remains 6, size 5 becomes 4).
    *   In components with multiple distinct numbers, the cell(s) containing the minimum value change to 7, while other cells in that component change to the minimum value.

**Facts (YAML):**


```yaml
Elements:
  - Grid:
      description: A 2D array of integers representing the input and output states.
      properties:
        - dimensions: [rows, columns] (variable)
        - cells: Contains integer values.
  - Cell:
      description: An individual unit within the grid.
      properties:
        - value: Integer.
        - position: [row, column].
        - type: Can be 'background' (value 7) or 'active' (value != 7).
  - Connected Component:
      description: A group of adjacent 'active' cells (using Von Neumann neighborhood).
      properties:
        - cells: A set of cell positions belonging to the component.
        - size: The number of cells in the component.
        - unique_values: The set of distinct integer values present in the component's cells.
        - min_value: The minimum integer value among the component's cells.

Relationships:
  - Adjacency: Cells are adjacent if they share an edge (up, down, left, right).
  - Membership: An 'active' cell belongs to exactly one Connected Component.

Transformation:
  description: Modifies the values of 'active' cells based on the properties of their Connected Component.
  rules:
    - Background cells (value 7) remain unchanged.
    - Active cells are processed based on their component's properties (size, unique_values, min_value).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all connected components of cells having values other than 7. Use adjacency based on shared edges (up, down, left, right neighbours). Treat cells with value 7 as boundaries.
3.  For each identified connected component:
    a.  Determine the `size` (number of cells) of the component.
    b.  Determine the set of `unique_values` present in the component.
    c.  Determine the `min_value` among the cells in the component.
    d.  Apply transformation rules to each cell `(r, c)` with original value `v` within this component:
        i.  **Rule 1 (Size 1):** If `size` is 1, update the output grid at `(r, c)` to 7.
        ii. **Rule 2 (Size 4, only 6s):** If `size` is 4 AND `unique_values` is exactly `{6}`, the output value at `(r, c)` remains 6 (no change needed as output started as a copy).
        iii. **Rule 3 (Size 5, only 6s):** If `size` is 5 AND `unique_values` is exactly `{6}`, update the output grid at `(r, c)` to 4.
        iv. **Rule 4 (Minimum Value Cell):** If the component does not match Rule 2 or Rule 3, AND the cell's original value `v` is equal to `min_value`, update the output grid at `(r, c)` to 7.
        v.  **Rule 5 (Other Cells in Mixed Component):** If the component does not match Rule 1, 2, or 3, AND the cell's original value `v` is NOT equal to `min_value`, update the output grid at `(r, c)` to `min_value`.
4.  Return the modified output grid.
```python
import copy
from collections import deque

"""
Transforms a 2D grid of integers based on connected components of non-7 values.

1. Identifies connected components of cells with values other than 7 using 4-way adjacency (up, down, left, right). Cells with value 7 act as boundaries.
2. For each component:
    a. Calculates its size (number of cells).
    b. Finds the set of unique values within the component.
    c. Determines the minimum value within the component.
    d. Applies specific rules to modify the cells within the component in the output grid:
        - If size is 1, the cell's value becomes 7.
        - If size is 4 and all values are 6, the cells remain 6.
        - If size is 5 and all values are 6, the cells become 4.
        - Otherwise:
            - Cells originally holding the minimum value change to 7.
            - All other cells in the component change to the minimum value.
3. Cells with the value 7 remain unchanged throughout the process.
"""

def _get_neighbors(r, c, rows, cols):
    """Yields valid neighbor coordinates (up, down, left, right)."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def _find_component(start_r, start_c, grid, visited):
    """Finds a connected component using BFS."""
    rows = len(grid)
    cols = len(grid[0])
    if visited[start_r][start_c] or grid[start_r][start_c] == 7:
        return None, None # Already visited or a boundary cell

    component_cells = []
    component_values = []
    q = deque([(start_r, start_c)])
    visited[start_r][start_c] = True

    while q:
        r, c = q.popleft()
        component_cells.append((r, c))
        component_values.append(grid[r][c])

        for nr, nc in _get_neighbors(r, c, rows, cols):
            if not visited[nr][nc] and grid[nr][nc] != 7:
                visited[nr][nc] = True
                q.append((nr, nc))

    return component_cells, component_values


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid based on connected components.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Keep track of visited cells to avoid reprocessing components
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell to find components
    for r in range(rows):
        for c in range(cols):
            # If cell is active (not 7) and not yet visited, start a component search
            if input_grid[r][c] != 7 and not visited[r][c]:
                component_cells, component_values = _find_component(r, c, input_grid, visited)

                if component_cells: # Check if a valid component was found
                    # Determine component properties
                    size = len(component_cells)
                    unique_values = set(component_values)
                    min_value = min(component_values)

                    # Apply transformation rules to the cells in the component
                    for cell_r, cell_c in component_cells:
                        original_value = input_grid[cell_r][cell_c]

                        # Rule 1 (Size 1):
                        if size == 1:
                            output_grid[cell_r][cell_c] = 7
                        # Rule 2 (Size 4, only 6s): - No change needed as output started as copy
                        elif size == 4 and unique_values == {6}:
                            pass # Value remains 6
                        # Rule 3 (Size 5, only 6s):
                        elif size == 5 and unique_values == {6}:
                            output_grid[cell_r][cell_c] = 4
                        # Rule 4 (Minimum Value Cell in other components):
                        elif original_value == min_value:
                            output_grid[cell_r][cell_c] = 7
                        # Rule 5 (Other Cells in other components):
                        else: # original_value != min_value
                            output_grid[cell_r][cell_c] = min_value

    return output_grid
```
