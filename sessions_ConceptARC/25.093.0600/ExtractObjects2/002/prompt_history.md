
## train_1

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 3 1 1 1 1 1 3 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0
0 0 3 0 3 0 0
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 3 0 0 0 3 0
0 0 3 0 3 0 0
0 0 0 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 0 9 9 9 9 9 0 0 0 0 0 0 0 0
4 0 4 9 4 0 4 9 4 0 4 0 4 0 4 0
0 4 0 9 0 4 0 9 0 4 0 4 0 4 0 4
0 0 0 9 0 0 0 9 0 0 0 0 0 0 0 0
6 0 6 9 9 9 9 9 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0
0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 9 9 9 9
9 0 0 0 9
9 0 0 0 9
9 0 0 0 9
9 9 9 9 9
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 4 0 0
0 4 0 4 0 4 0 4 0 4 0
0 0 4 0 0 0 4 0 0 0 4
4 0 0 6 6 6 0 0 4 0 0
0 4 0 4 0 6 0 4 0 4 0
0 0 4 0 0 6 4 0 0 0 4
4 0 0 6 6 6 0 0 0 0 0
0 4 0 4 0 4 0 0 0 4 0
0 0 4 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 4 0 0 0
```


**output:**
```
6 6 6
0 0 6
0 0 6
6 6 6
```

*   **Perception:** The task involves processing 2D grids of integers. The input grids contain background zeros and various non-zero integers forming different patterns and shapes. The output grid is always a subgrid of the input grid. The transformation seems to involve identifying a specific connected region of identical non-zero numbers within the input and extracting the rectangular bounding box surrounding that region.
*   **Logic:** The core logic appears to be:
    1.  Identify all connected components (regions where adjacent cells have the same non-zero value). Connectivity can be considered 4-way (up, down, left, right).
    2.  Determine the "most significant" component. Based on the examples, this seems to be the connected component containing the largest number of cells, irrespective of the actual number value.
    3.  Find the minimal bounding box (smallest rectangle) that encloses all cells of this largest component.
    4.  Extract the subgrid corresponding to this bounding box from the input grid.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    input_elements:
      - type: grid
        description: 2D grid of integers.
        properties:
          - contains_zeros: True (likely background)
          - contains_non_zeros: True (form patterns/objects)
    output_elements:
      - type: grid
        description: A subgrid extracted from the input.
    transformation:
      action: extract_subgrid
      target_object:
        type: connected_component
        properties:
          - composed_of_single_non_zero_value: True
          - criteria_for_selection: largest_area (maximum number of cells)
      subgrid_definition:
        type: bounding_box
        description: Minimal rectangular area enclosing the target connected component.
    relationships:
      - output is a sub-section of the input grid.
      - the content of the output grid directly corresponds to the content of the input grid within the identified bounding box.
    ```


*   **Natural Language Program:**
    1.  Receive the input grid.
    2.  Initialize variables to track the largest connected component found so far (e.g., `max_component_size = 0`, `largest_component_cells = None`).
    3.  Create a `visited` grid of the same dimensions as the input, initialized to `False`.
    4.  Iterate through each cell (`r`, `c`) of the input grid.
    5.  If the current cell `(r, c)` contains a non-zero value and has not been `visited`:
        a.  Initiate a search (e.g., Breadth-First Search or Depth-First Search) starting from `(r, c)` to find all connected cells with the same non-zero value. Mark each visited cell as `True` in the `visited` grid.
        b.  Store the coordinates of all cells belonging to this newly found component.
        c.  Count the number of cells (`current_component_size`) in this component.
        d.  If `current_component_size` is greater than `max_component_size`:
            i.  Update `max_component_size` to `current_component_size`.
            ii. Store the list of cell coordinates for this component in `largest_component_cells`.
    6.  After iterating through all cells, determine the minimum and maximum row (`min_r`, `max_r`) and column (`min_c`, `max_c`) indices from the coordinates stored in `largest_component_cells`. This defines the bounding box.
    7.  Create a new output grid by extracting the subgrid from the input grid ranging from `min_r` to `max_r` (inclusive) and `min_c` to `max_c` (inclusive).
    8.  Return the extracted output grid.
```python
"""
Finds the largest connected component of identical non-zero numbers in the input grid.
Then, extracts the minimal bounding box surrounding this component from the input grid.
Connectivity is defined as adjacent cells (up, down, left, right) having the same non-zero value.
"""

import collections

def _find_connected_component(grid, start_r, start_c, visited):
    """
    Performs a Breadth-First Search (BFS) to find all connected cells
    with the same non-zero value starting from (start_r, start_c).

    Args:
        grid (list of list of int): The input grid.
        start_r (int): The starting row index.
        start_c (int): The starting column index.
        visited (list of list of bool): Grid to track visited cells.

    Returns:
        list of tuple: A list of (row, col) coordinates for the cells
                       in the connected component. Returns empty list
                       if the starting cell is 0 or already visited.
    """
    rows = len(grid)
    cols = len(grid[0])
    target_value = grid[start_r][start_c]

    # Ignore background (0) or already processed cells
    if target_value == 0 or visited[start_r][start_c]:
        return []

    component_coords = []
    queue = collections.deque([(start_r, start_c)])
    visited[start_r][start_c] = True

    while queue:
        r, c = queue.popleft()
        component_coords.append((r, c))

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is part of the component and not visited
                if not visited[nr][nc] and grid[nr][nc] == target_value:
                    visited[nr][nc] = True
                    queue.append((nr, nc))

    return component_coords

def _get_bounding_box(coords):
    """
    Calculates the min/max row/col for a list of coordinates.

    Args:
        coords (list of tuple): List of (row, col) coordinates.

    Returns:
        tuple: (min_r, max_r, min_c, max_c) or None if coords is empty.
    """
    if not coords:
        return None

    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, max_r, min_c, max_c

def _extract_subgrid(grid, min_r, max_r, min_c, max_c):
    """
    Extracts a subgrid defined by the bounding box coordinates.

    Args:
        grid (list of list of int): The original grid.
        min_r (int): Minimum row index (inclusive).
        max_r (int): Maximum row index (inclusive).
        min_c (int): Minimum column index (inclusive).
        max_c (int): Maximum column index (inclusive).

    Returns:
        list of list of int: The extracted subgrid.
    """
    subgrid = []
    for r in range(min_r, max_r + 1):
        subgrid.append(grid[r][min_c : max_c + 1])
    return subgrid


def transform(input_grid):
    """
    Finds the largest connected component of a single non-zero number in the
    input grid and returns the subgrid corresponding to its bounding box.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The extracted subgrid containing the largest
                             connected component, defined by its bounding box.
                             Returns an empty list if no non-zero components
                             are found.
    """
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input

    rows = len(input_grid)
    cols = len(input_grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    max_component_size = 0
    largest_component_coords = []

    # Iterate through each cell to find components
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] != 0 and not visited[r][c]:
                # Find the connected component starting from this cell
                component_coords = _find_connected_component(input_grid, r, c, visited)
                current_component_size = len(component_coords)

                # Check if this component is the largest found so far
                if current_component_size > max_component_size:
                    max_component_size = current_component_size
                    largest_component_coords = component_coords

    # If no non-zero components were found, return empty grid
    if not largest_component_coords:
        return []

    # Calculate the bounding box of the largest component
    bounding_box = _get_bounding_box(largest_component_coords)
    min_r, max_r, min_c, max_c = bounding_box

    # Extract the subgrid corresponding to the bounding box
    output_grid = _extract_subgrid(input_grid, min_r, max_r, min_c, max_c)

    return output_grid
```
