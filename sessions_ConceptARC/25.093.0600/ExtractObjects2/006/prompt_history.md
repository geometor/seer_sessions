
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
```python
"""
Identifies the largest connected component of identical non-zero numbers in an input grid.
Connectivity is defined by adjacent cells (up, down, left, right) sharing the same non-zero value.
Calculates the minimal bounding box enclosing this largest component.
Extracts the subgrid corresponding to this bounding box from the input grid.
The input grid is expected to be a NumPy array, and the output will be a standard Python list of lists.
"""

import numpy as np
import collections

def _find_connected_component(grid, start_r, start_c, visited):
    """
    Performs BFS to find all connected cells with the same non-zero value.

    Args:
        grid (np.array): The input grid.
        start_r (int): The starting row index.
        start_c (int): The starting column index.
        visited (np.array): Boolean grid to track visited cells.

    Returns:
        list of tuple: Coordinates (row, col) of cells in the component.
                       Returns empty list if start cell is 0 or visited.
    """
    rows, cols = grid.shape
    target_value = grid[start_r, start_c]

    # Ignore background (0) or already processed cells
    if target_value == 0 or visited[start_r, start_c]:
        return []

    component_coords = []
    queue = collections.deque([(start_r, start_c)])
    visited[start_r, start_c] = True # Mark starting cell as visited

    while queue:
        r, c = queue.popleft()
        component_coords.append((r, c))

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor has the target value and hasn't been visited
                if not visited[nr, nc] and grid[nr, nc] == target_value:
                    visited[nr, nc] = True # Mark neighbor as visited
                    queue.append((nr, nc)) # Add neighbor to the queue

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

    # Find min/max row and column from the component coordinates
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, max_r, min_c, max_c

def transform(input_grid_arg):
    """
    Finds the largest connected component of a single non-zero number in the
    input grid and returns the subgrid corresponding to its bounding box.

    Args:
        input_grid_arg: The input 2D grid (can be list of lists or numpy array).

    Returns:
        list of list of int: The extracted subgrid containing the largest
                             connected component, defined by its bounding box.
                             Returns an empty list if no non-zero components
                             are found or if input is empty.
    """
    # Ensure input is a NumPy array for efficient processing
    input_grid = np.array(input_grid_arg, dtype=int)

    # Handle empty input grid
    if input_grid.size == 0:
        return []

    rows, cols = input_grid.shape
    # Initialize a boolean grid to keep track of visited cells
    visited = np.full((rows, cols), False, dtype=bool)

    max_component_size = 0
    largest_component_coords = []

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If cell is non-zero and not yet visited, explore its component
            if input_grid[r, c] != 0 and not visited[r, c]:
                # Find the connected component starting from this cell
                component_coords = _find_connected_component(input_grid, r, c, visited)
                current_component_size = len(component_coords)

                # Check if this component is the largest found so far
                if current_component_size > max_component_size:
                    max_component_size = current_component_size
                    largest_component_coords = component_coords

    # If no non-zero components were found, return an empty list
    if not largest_component_coords:
        return []

    # Calculate the bounding box of the largest component
    bounding_box = _get_bounding_box(largest_component_coords)
    min_r, max_r, min_c, max_c = bounding_box

    # Extract the subgrid corresponding to the bounding box using NumPy slicing
    output_np_array = input_grid[min_r : max_r + 1, min_c : max_c + 1]

    # Convert the resulting NumPy array to a standard Python list of lists
    output_grid = output_np_array.tolist()

    return output_grid
```
```python
"""
Identifies the unique integer value (including 0) in the input grid whose
occurrences have the highest density within their minimal bounding box.
Density is calculated as (number of occurrences) / (bounding box area).
Tie-breaking rules: highest density, then highest count, then smallest
bounding box area, then smallest integer value.
Extracts the subgrid corresponding to the bounding box of the selected value.
Filters the extracted subgrid, keeping only the cells that contained the
selected value in the original input and setting others to 0.
"""

import numpy as np
import collections # Although not strictly needed with numpy, kept for potential future use if logic changes

def _get_bounding_box(coords_indices):
    """
    Calculates the min/max row/col for a list/array of coordinates.

    Args:
        coords_indices (tuple of np.array): Output from np.where, containing arrays
                                          for row indices and column indices.

    Returns:
        tuple: (min_r, max_r, min_c, max_c) or None if coords_indices is empty.
    """
    if not coords_indices or len(coords_indices[0]) == 0:
        return None

    rows = coords_indices[0]
    cols = coords_indices[1]

    min_r = np.min(rows)
    max_r = np.max(rows)
    min_c = np.min(cols)
    max_c = np.max(cols)
    return min_r, max_r, min_c, max_c

def transform(input_grid_arg):
    """
    Finds the integer value with the highest density of occurrences within its
    bounding box, extracts that bounding box, and filters it to keep only
    the selected integer value.

    Args:
        input_grid_arg: The input 2D grid (list of lists or numpy array).

    Returns:
        list of list of int: The filtered subgrid based on the highest density value.
                             Returns an empty list if the input is empty or no suitable
                             value is found (e.g., only zeros and 0 isn't highest density).
    """
    # Ensure input is a NumPy array
    input_grid = np.array(input_grid_arg, dtype=int)

    # Handle empty input grid
    if input_grid.size == 0:
        return []

    rows, cols = input_grid.shape

    # Find unique values in the grid
    unique_values = np.unique(input_grid)

    # Initialize variables to track the best candidate
    best_value = None
    max_density = -1.0
    max_count = -1
    min_bbox_area = float('inf')
    best_bbox = None

    # Iterate through each unique value to find the one with the highest density
    for candidate_value in unique_values:
        # Find coordinates of all occurrences of the candidate value
        indices = np.where(input_grid == candidate_value)

        # Skip if the value doesn't exist (shouldn't happen with np.unique unless grid is empty)
        if len(indices[0]) == 0:
            continue

        # Calculate count
        current_count = len(indices[0])

        # Determine bounding box
        bbox = _get_bounding_box(indices)
        if bbox is None: # Should not happen if count > 0
             continue
        min_r, max_r, min_c, max_c = bbox

        # Calculate bounding box area
        current_bbox_area = (max_r - min_r + 1) * (max_c - min_c + 1)
        if current_bbox_area <= 0: # Avoid division by zero for single point/line cases
            current_density = float('inf') if current_count > 0 else 0 # Assign high density if area is minimal
        else:
            current_density = current_count / current_bbox_area

        # --- Apply selection criteria and tie-breaking ---
        is_better = False
        if current_density > max_density:
            is_better = True
        elif current_density == max_density:
            if current_count > max_count:
                is_better = True
            elif current_count == max_count:
                if current_bbox_area < min_bbox_area:
                    is_better = True
                elif current_bbox_area == min_bbox_area:
                    # Final tie-breaker: smaller integer value wins
                    if best_value is None or candidate_value < best_value:
                        is_better = True

        # Update best candidate if current one is better
        if is_better:
            max_density = current_density
            max_count = current_count
            min_bbox_area = current_bbox_area
            best_value = candidate_value
            best_bbox = bbox

    # If no suitable candidate was found (e.g., empty grid processed), return empty list
    if best_bbox is None:
        return []

    # Extract the subgrid corresponding to the best bounding box
    min_r, max_r, min_c, max_c = best_bbox
    extracted_subgrid = input_grid[min_r : max_r + 1, min_c : max_c + 1]

    # Filter the extracted subgrid: keep only the 'best_value', replace others with 0
    output_grid_np = np.where(extracted_subgrid == best_value, best_value, 0)

    # Convert the resulting NumPy array to a standard Python list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```
