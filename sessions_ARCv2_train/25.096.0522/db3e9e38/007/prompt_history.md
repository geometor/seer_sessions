
## train_1

**input:**
```
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
7 8 7 8 7 8 7 0
7 8 7 8 7 8 0 0
7 8 7 8 7 0 0 0
0 8 7 8 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

Okay, let's break down the transformation logic for this task.

**Perception of Elements:**

1.    **Input/Output Format:** Both input and output are 2D grids (matrices) of integers. The dimensions seem to remain consistent between input and output for each example.
2.  **Key Input Feature:** The input grids contain mostly zeros but have a distinct vertical line composed of the number 7.
3.  **Output Pattern:** The output grids also contain zeros, 7s, and a new number, 8. The 7s and 8s form a pattern that seems to originate from the location of the input line of 7s but expands outwards. The original line of 7s in the input is not directly preserved, except potentially the topmost '7'.
4.  **Propagation:** The pattern in the output looks like a wave or propagation spreading from a starting point. The values alternate between 7 and 8 as the pattern spreads.
5.  **Starting Point:** Comparing the two examples, the pattern seems to consistently start from the *topmost* '7' found in the input grid.
6.  **Alternating Values:** Cells adjacent (orthogonally) to a '7' in the output pattern become '8', and cells adjacent to an '8' become '7', provided they haven't been filled yet. This suggests a Breadth-First Search (BFS) or similar layer-by-layer expansion where the value depends on the value of the cell from which it's expanding.

**YAML Facts:**


```yaml
Task: Grid value propagation based on seed location

Objects:
  - Input_Grid:
      Type: 2D integer array
      Contains: Background value (0), Seed value (7)
      Structure: Primarily background values with one or more occurrences of the seed value, often forming a vertical line.
  - Output_Grid:
      Type: 2D integer array
      Dimensions: Same as Input_Grid
      Contains: Background value (0), Propagation values (7, 8)
      Structure: A pattern of alternating propagation values expanding from a specific point, replacing original values.
  - Seed_Cell:
      Identification: The topmost cell in the Input_Grid containing the Seed value (7).
      Properties: Row index, Column index, Value (7).
  - Propagation_Pattern:
      Values: Alternating sequence (7, 8, 7, 8, ...)
      Mechanism: Spreads outwards orthogonally (up, down, left, right) from the Seed_Cell.

Relationships:
  - Origin: The Propagation_Pattern in the Output_Grid originates from the Seed_Cell identified in the Input_Grid.
  - Overwrite: The Propagation_Pattern overwrites the initial content (0s or other 7s from the input) of the Output_Grid cells it covers.
  - Adjacency_Rule: Orthogonally adjacent cells in the Propagation_Pattern have alternating values (if one is 7, its newly filled neighbors are 8, and vice-versa).

Action:
  - Find_Seed: Locate the row and column of the topmost Seed value (7) in the Input_Grid.
  - Initialize_Output: Create an Output_Grid of the same size as the Input_Grid, filled with the background value (0).
  - Propagate:
      Starting_Condition: Place the Seed value (7) at the Seed_Cell location in the Output_Grid.
      Process: Perform a Breadth-First Search (BFS) starting from the Seed_Cell.
      Rule: For each cell visited, assign the alternating value (8 if current is 7, 7 if current is 8) to its unvisited orthogonal neighbors within the grid boundaries. Mark neighbors as visited and add them to the BFS queue.
      Termination: Continue until the BFS queue is empty.
```


**Natural Language Program:**

1.  Create a new grid, `output_grid`, with the same dimensions as the `input_grid`, and initialize all its cells to 0.
2.  Scan the `input_grid` row by row, then column by column, to find the coordinates `(seed_row, seed_col)` of the first cell encountered that contains the value 7.
3.  If no cell with the value 7 is found in the `input_grid`, return the initialized `output_grid`.
4.  If a seed cell `(seed_row, seed_col)` is found:
    a.  Initialize a queue data structure for Breadth-First Search (BFS).
    b.  Initialize a data structure (e.g., a set of coordinate tuples or a boolean grid) called `visited` to keep track of cells that have been assigned a value and added to the queue.
    c.  Set the value of `output_grid[seed_row][seed_col]` to 7.
    d.  Add the tuple `(seed_row, seed_col, 7)` representing (row, column, value) to the queue.
    e.  Add the coordinates `(seed_row, seed_col)` to `visited`.
    f.  While the queue is not empty:
        i.   Dequeue the next element `(current_row, current_col, current_value)`.
        ii.  Determine the `next_value` for neighbors: if `current_value` is 7, `next_value` is 8; otherwise, `next_value` is 7.
        iii. Consider the four orthogonal neighbors: `(current_row - 1, current_col)`, `(current_row + 1, current_col)`, `(current_row, current_col - 1)`, `(current_row, current_col + 1)`.
        iv.  For each neighbor `(neighbor_row, neighbor_col)`:
             1. Check if `(neighbor_row, neighbor_col)` is within the valid bounds of the grid.
             2. Check if `(neighbor_row, neighbor_col)` has *not* been marked as `visited`.
             3. If both checks pass:
                 *   Set `output_grid[neighbor_row][neighbor_col]` to `next_value`.
                 *   Mark `(neighbor_row, neighbor_col)` as `visited`.
                 *   Enqueue the tuple `(neighbor_row, neighbor_col, next_value)`.
5.  Return the completed `output_grid`.
```python
"""
Transforms an input grid by finding the topmost '7', treating it as a seed,
and performing a Breadth-First Search (BFS) propagation. During the BFS,
the values 7 and 8 alternate layer by layer, starting with 7 at the seed.
The propagation overwrites the grid cells with these alternating values.
"""

import collections

def find_seed(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the coordinates (row, col) of the topmost '7' in the grid."""
    rows = len(grid)
    if rows == 0:
        return None
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 7:
                return (r, c)
    return None # No seed found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Performs the BFS propagation transformation.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
         return [[] for _ in range(rows)] # Return grid of empty rows if cols is 0

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find the seed location (topmost '7')
    seed_coords = find_seed(input_grid)

    # If no seed is found, return the initialized grid
    if seed_coords is None:
        return output_grid

    seed_row, seed_col = seed_coords

    # Initialize BFS queue and visited set
    # The queue stores tuples of (row, col, value)
    queue = collections.deque()
    visited = set()

    # Start BFS from the seed cell
    start_value = 7
    output_grid[seed_row][seed_col] = start_value
    queue.append((seed_row, seed_col, start_value))
    visited.add((seed_row, seed_col))

    # Perform BFS propagation
    while queue:
        current_row, current_col, current_value = queue.popleft()

        # Determine the value for neighbors (alternating 7 and 8)
        next_value = 8 if current_value == 7 else 7

        # Define orthogonal neighbor directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Explore neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = current_row + dr, current_col + dc

            # Check if the neighbor is within grid bounds
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                # Check if the neighbor has not been visited
                if (neighbor_row, neighbor_col) not in visited:
                    # Update the output grid with the next value
                    output_grid[neighbor_row][neighbor_col] = next_value
                    # Mark the neighbor as visited
                    visited.add((neighbor_row, neighbor_col))
                    # Add the neighbor to the queue for further exploration
                    queue.append((neighbor_row, neighbor_col, next_value))

    return output_grid
```
```python
"""
Transforms an input grid by identifying all cells containing '7' as seeds.
These seed cells are marked as '7' in the output grid. A Breadth-First
Search (BFS) propagates outwards from all seeds simultaneously. Orthogonal
neighbors of '7' cells are marked '8', and neighbors of '8' cells are
marked '7'. The propagation only affects cells not yet visited, starting
from an initial grid of zeros.
"""

import collections

def find_all_seeds(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Finds the coordinates (row, col) of all '7's in the grid."""
    seeds = []
    rows = len(grid)
    if rows == 0:
        return seeds
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 7:
                seeds.append((r, c))
    return seeds

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Performs the BFS propagation transformation from all seed locations.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
         return [[] for _ in range(rows)] # Return grid of empty rows if cols is 0

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find all seed locations ('7's in the input)
    seed_locations = find_all_seeds(input_grid)

    # If no seeds are found, return the initialized grid
    if not seed_locations:
        return output_grid

    # Initialize BFS queue and visited set
    # The queue stores tuples of (row, col, value)
    queue = collections.deque()
    visited = set()

    # Initialize the BFS with all seed locations
    for r, c in seed_locations:
        start_value = 7
        if (r, c) not in visited: # Ensure seeds aren't added multiple times if input has duplicates? (Unlikely based on examples, but safe)
            output_grid[r][c] = start_value
            queue.append((r, c, start_value))
            visited.add((r, c))

    # Perform BFS propagation
    while queue:
        current_row, current_col, current_value = queue.popleft()

        # Determine the value for neighbors (alternating 7 and 8)
        next_value = 8 if current_value == 7 else 7

        # Define orthogonal neighbor directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Explore neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = current_row + dr, current_col + dc

            # Check if the neighbor is within grid bounds
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                # Check if the neighbor has not been visited
                if (neighbor_row, neighbor_col) not in visited:
                    # Update the output grid with the next value
                    output_grid[neighbor_row][neighbor_col] = next_value
                    # Mark the neighbor as visited
                    visited.add((neighbor_row, neighbor_col))
                    # Add the neighbor to the queue for further exploration
                    queue.append((neighbor_row, neighbor_col, next_value))

    return output_grid
```
```python
"""
Transforms an input grid based on a propagation pattern originating from the
topmost cell containing the value 7 (the seed). The pattern's extent is
determined by the Manhattan distance between the topmost and bottommost
cells containing 7 in the input. Within this distance limit, cells in the
output grid are assigned values 7 or 8 based on the parity of their
Manhattan distance from the seed cell (7 for even distance, 8 for odd).
Cells outside this distance limit remain 0.
"""

import numpy as np
from typing import Optional, Tuple, List

def find_extremal_seeds(grid: np.ndarray) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds the coordinates of the topmost (first encountered) and bottommost
    (last encountered) cells containing the value 7.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple containing two tuples: (topmost_coords, bottommost_coords),
        or None if no 7 is found.
    """
    rows, cols = grid.shape
    topmost_coords: Optional[Tuple[int, int]] = None
    bottommost_coords: Optional[Tuple[int, int]] = None

    # Find topmost seed (first 7 encountered in row-major order)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                topmost_coords = (r, c)
                break
        if topmost_coords is not None:
            break

    # If no 7 found at all
    if topmost_coords is None:
        return None

    # Find bottommost seed (last 7 encountered in row-major order)
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 7:
                bottommost_coords = (r, c)
                break
        if bottommost_coords is not None:
            break
            
    # Should theoretically always find bottommost if topmost was found,
    # but handle potential edge cases if grid structure is unusual.
    if bottommost_coords is None:
        bottommost_coords = topmost_coords # If only one seed, it's both top and bottom

    return topmost_coords, bottommost_coords

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the distance-limited, alternating value propagation.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize output_grid with zeros
    output_array = np.zeros_like(input_array)

    # Find the coordinates of the topmost and bottommost seeds
    extremal_seeds = find_extremal_seeds(input_array)

    # If no seeds were found, return the grid of zeros
    if extremal_seeds is None:
        return output_array.tolist()

    seed_coords, limit_coords = extremal_seeds
    seed_row, seed_col = seed_coords

    # Calculate the maximum propagation distance based on the extremal seeds
    max_dist = manhattan_distance(seed_coords, limit_coords)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the Manhattan distance from the current cell to the seed
            current_coords = (r, c)
            dist = manhattan_distance(seed_coords, current_coords)

            # Check if the cell is within the maximum allowed distance
            if dist <= max_dist:
                # Assign 7 for even distance, 8 for odd distance
                if dist % 2 == 0:
                    output_array[r, c] = 7
                else:
                    output_array[r, c] = 8
            # Cells outside max_dist remain 0 (already initialized)

    # Convert the result back to a list of lists
    return output_array.tolist()
```

Previous Code:
```python
"""
Transforms an input grid based on a propagation pattern originating from the
topmost cell containing the value 7 (the seed). The pattern's extent is
determined by the Manhattan distance between the topmost and bottommost
cells containing 7 in the input. Within this distance limit, cells in the
output grid are assigned values 7 or 8 based on the parity of their
Manhattan distance from the seed cell (7 for even distance, 8 for odd).
Cells outside this distance limit remain 0.
"""

import numpy as np
from typing import Optional, Tuple, List

def find_extremal_seeds(grid: np.ndarray) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds the coordinates of the topmost (first encountered) and bottommost
    (last encountered) cells containing the value 7.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple containing two tuples: (topmost_coords, bottommost_coords),
        or None if no 7 is found.
    """
    rows, cols = grid.shape
    topmost_coords: Optional[Tuple[int, int]] = None
    bottommost_coords: Optional[Tuple[int, int]] = None

    # Find topmost seed (first 7 encountered in row-major order)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                topmost_coords = (r, c)
                break
        if topmost_coords is not None:
            break

    # If no 7 found at all
    if topmost_coords is None:
        return None

    # Find bottommost seed (last 7 encountered in row-major order)
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 7:
                bottommost_coords = (r, c)
                break
        if bottommost_coords is not None:
            break
            
    # Should theoretically always find bottommost if topmost was found,
    # but handle potential edge cases if grid structure is unusual.
    if bottommost_coords is None:
        bottommost_coords = topmost_coords # If only one seed, it's both top and bottom

    return topmost_coords, bottommost_coords

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the distance-limited, alternating value propagation.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize output_grid with zeros
    output_array = np.zeros_like(input_array)

    # Find the coordinates of the topmost and bottommost seeds
    extremal_seeds = find_extremal_seeds(input_array)

    # If no seeds were found, return the grid of zeros
    if extremal_seeds is None:
        return output_array.tolist()

    seed_coords, limit_coords = extremal_seeds
    seed_row, seed_col = seed_coords

    # Calculate the maximum propagation distance based on the extremal seeds
    max_dist = manhattan_distance(seed_coords, limit_coords)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the Manhattan distance from the current cell to the seed
            current_coords = (r, c)
            dist = manhattan_distance(seed_coords, current_coords)

            # Check if the cell is within the maximum allowed distance
            if dist <= max_dist:
                # Assign 7 for even distance, 8 for odd distance
                if dist % 2 == 0:
                    output_array[r, c] = 7
                else:
                    output_array[r, c] = 8
            # Cells outside max_dist remain 0 (already initialized)

    # Convert the result back to a list of lists
    return output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
Expected Output:
```
7 8 7 8 7 8 7 0
7 8 7 8 7 8 0 0
7 8 7 8 7 0 0 0
0 8 7 8 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
Transformed Output:
```
7 8 7 8 7 8 7 0
8 7 8 7 8 7 0 0
7 8 7 8 7 0 0 0
0 7 8 7 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.14285714285714

## Example 2:
Input:
```
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```
Expected Output:
```
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```
Transformed Output:
```
8 7 8 7 8 7 8
0 8 7 8 7 8 0
0 0 8 7 8 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.28571428571428
**General Assessment and Strategy**

The initial attempt using Manhattan distance parity from the topmost seed (`code_00.py`) correctly identified the propagation center (topmost '7') and the general shape (limited by Manhattan distance to the bottommost '7'). However, it failed to correctly assign the alternating values (7 or 8). The discrepancies between the expected and transformed outputs, particularly the inversion of values in certain rows, suggest that the assignment rule (7 for even distance, 8 for odd) was incorrect.

The errors occurred in rows offset from the seed row, indicating the rule might involve more than just the total Manhattan distance. Comparing the column index (`c`) of filled cells to the seed's column index (`sc`) reveals a consistent pattern: cells where `abs(c - sc)` is even contain 7, and cells where `abs(c - sc)` is odd contain 8, *within* the calculated Manhattan distance limit.

The strategy is to refine the natural language program and the underlying logic to incorporate this new rule: the value depends on the parity of the horizontal distance (`abs(c - sc)`) from the seed column, constrained by the overall Manhattan distance limit derived from the topmost and bottommost '7's in the input.

**Metrics**


*code_execution:*
```python
import numpy as np

def calculate_metrics(input_str, output_str, transformed_str):
    """Calculates metrics by comparing output and transformed grids."""
    input_grid = np.array([list(map(int, row.split())) for row in input_str.strip().split('\n')], dtype=int)
    output_grid = np.array([list(map(int, row.split())) for row in output_str.strip().split('\n')], dtype=int)
    transformed_grid = np.array([list(map(int, row.split())) for row in transformed_str.strip().split('\n')], dtype=int)

    metrics = {}
    metrics['Input Shape'] = input_grid.shape
    metrics['Output Shape'] = output_grid.shape
    metrics['Transformed Shape'] = transformed_grid.shape

    metrics['Shapes Match'] = (output_grid.shape == transformed_grid.shape)

    if metrics['Shapes Match']:
        diff = output_grid != transformed_grid
        metrics['Pixels Off'] = int(np.sum(diff))
        metrics['Total Pixels'] = output_grid.size
        metrics['Accuracy (%)'] = (1 - metrics['Pixels Off'] / metrics['Total Pixels']) * 100
        metrics['Non-zero Pixels Off'] = int(np.sum(diff[output_grid != 0])) # How many non-zero target pixels were wrong?
        metrics['Zero Pixels Off'] = int(np.sum(diff[output_grid == 0])) # How many zero target pixels were wrong (i.e., transformed had a non-zero value)?

        output_colors = set(np.unique(output_grid))
        transformed_colors = set(np.unique(transformed_grid))
        metrics['Output Colors'] = sorted(list(output_colors))
        metrics['Transformed Colors'] = sorted(list(transformed_colors))
        metrics['Color Palette Match'] = (output_colors == transformed_colors)

        output_counts = {k: int(np.sum(output_grid == k)) for k in output_colors}
        transformed_counts = {k: int(np.sum(transformed_grid == k)) for k in transformed_colors}
        metrics['Output Color Counts'] = output_counts
        metrics['Transformed Color Counts'] = transformed_counts
        metrics['Color Count Match'] = (output_counts == transformed_counts)

    else:
        metrics['Pixels Off'] = -1 # Undefined
        metrics['Total Pixels'] = output_grid.size
        metrics['Accuracy (%)'] = 0
        metrics['Non-zero Pixels Off'] = -1
        metrics['Zero Pixels Off'] = -1
        metrics['Output Colors'] = sorted(list(np.unique(output_grid)))
        metrics['Transformed Colors'] = sorted(list(np.unique(transformed_grid)))
        metrics['Color Palette Match'] = False
        metrics['Output Color Counts'] = {k: int(np.sum(output_grid == k)) for k in np.unique(output_grid)}
        metrics['Transformed Color Counts'] = {k: int(np.sum(transformed_grid == k)) for k in np.unique(transformed_grid)}
        metrics['Color Count Match'] = False

    return metrics

# --- Example 1 Data ---
input_1 = """
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
"""
output_1 = """
7 8 7 8 7 8 7 0
7 8 7 8 7 8 0 0
7 8 7 8 7 0 0 0
0 8 7 8 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
"""
transformed_1 = """
7 8 7 8 7 8 7 0
8 7 8 7 8 7 0 0
7 8 7 8 7 0 0 0
0 7 8 7 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
"""

# --- Example 2 Data ---
input_2 = """
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
"""
output_2 = """
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
"""
transformed_2 = """
8 7 8 7 8 7 8
0 8 7 8 7 8 0
0 0 8 7 8 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
"""

metrics_1 = calculate_metrics(input_1, output_1, transformed_1)
metrics_2 = calculate_metrics(input_2, output_2, transformed_2)

print("--- Example 1 Metrics ---")
print(metrics_1)
print("\n--- Example 2 Metrics ---")
print(metrics_2)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Metrics ---
{'Input Shape': (7, 8), 'Output Shape': (7, 8), 'Transformed Shape': (7, 8), 'Shapes Match': True, 'Pixels Off': 9, 'Total Pixels': 56, 'Accuracy (%)': 83.92857142857143, 'Non-zero Pixels Off': 9, 'Zero Pixels Off': 0, 'Output Colors': [np.int64(0), np.int64(7), np.int64(8)], 'Transformed Colors': [np.int64(0), np.int64(7), np.int64(8)], 'Color Palette Match': True, 'Output Color Counts': {np.int64(0): 34, np.int64(8): 10, np.int64(7): 12}, 'Transformed Color Counts': {np.int64(0): 34, np.int64(8): 9, np.int64(7): 13}, 'Color Count Match': False}

--- Example 2 Metrics ---
{'Input Shape': (5, 7), 'Output Shape': (5, 7), 'Transformed Shape': (5, 7), 'Shapes Match': True, 'Pixels Off': 6, 'Total Pixels': 35, 'Accuracy (%)': 82.85714285714285, 'Non-zero Pixels Off': 6, 'Zero Pixels Off': 0, 'Output Colors': [np.int64(0), np.int64(7), np.int64(8)], 'Transformed Colors': [np.int64(0), np.int64(7), np.int64(8)], 'Color Palette Match': True, 'Output Color Counts': {np.int64(0): 19, np.int64(8): 8, np.int64(7): 8}, 'Transformed Color Counts': {np.int64(0): 19, np.int64(8): 10, np.int64(7): 6}, 'Color Count Match': False}

```
**YAML Facts**


```yaml
Task: Grid value propagation based on seed location and column parity within distance limit

Objects:
  - Input_Grid:
      Type: 2D integer array
      Contains: Background value (0), Seed marker (7)
      Structure: Primarily background values with one or more occurrences of the seed marker, typically forming a vertical line.
  - Output_Grid:
      Type: 2D integer array
      Dimensions: Same as Input_Grid
      Contains: Background value (0), Propagation values (7, 8)
      Structure: A diamond-like pattern of alternating propagation values expanding from a specific point, replacing original values within a calculated boundary.
  - Seed_Cell:
      Identification: The topmost (first encountered in row-major scan) cell in the Input_Grid containing the Seed marker (7).
      Properties: Row index (seed_row), Column index (seed_col).
  - Limit_Cell:
      Identification: The bottommost (last encountered in row-major scan) cell in the Input_Grid containing the Seed marker (7).
      Properties: Row index (limit_row), Column index (limit_col).
      Note: If only one '7' exists, Limit_Cell is the same as Seed_Cell.
  - Propagation_Boundary:
      Type: Manhattan Distance
      Calculation: `max_dist = abs(seed_row - limit_row) + abs(seed_col - limit_col)`
  - Propagation_Pattern:
      Values: 7 or 8
      Rule: Determined by the column parity relative to the Seed_Cell's column index.
      Condition: Applies only to cells within the Propagation_Boundary.

Relationships:
  - Origin: The Propagation_Pattern in the Output_Grid originates conceptually from the Seed_Cell.
  - Boundary_Definition: The extent of the Propagation_Pattern is limited by the Manhattan distance (`max_dist`) between the Seed_Cell and the Limit_Cell.
  - Value_Assignment: For a cell `(r, c)` within the Propagation_Boundary (i.e., `manhattan_distance((r, c), Seed_Cell) <= max_dist`), its value in the Output_Grid is 7 if `abs(c - seed_col)` is even, and 8 if `abs(c - seed_col)` is odd.
  - Background: Cells outside the Propagation_Boundary retain the Background value (0).
  - Overwrite: The Propagation_Pattern overwrites the initial content (0s or input 7s) of the Output_Grid cells it covers.

Action:
  - Find_Extremal_Seeds: Scan the Input_Grid to find the coordinates of the Seed_Cell `(seed_row, seed_col)` and the Limit_Cell `(limit_row, limit_col)`. Handle the case where no '7' is found or only one '7' is found.
  - Calculate_Max_Distance: Compute the Manhattan distance `max_dist` between Seed_Cell and Limit_Cell.
  - Initialize_Output: Create an Output_Grid of the same size as the Input_Grid, filled with the background value (0).
  - Apply_Pattern: Iterate through each cell `(r, c)` of the grid:
      - Calculate current Manhattan distance: `dist = abs(r - seed_row) + abs(c - seed_col)`.
      - If `dist <= max_dist`:
          - Calculate column distance: `col_dist = abs(c - seed_col)`.
          - If `col_dist % 2 == 0`: set `Output_Grid[r][c] = 7`.
          - Else (`col_dist % 2 == 1`): set `Output_Grid[r][c] = 8`.
  - Return_Output: Provide the completed Output_Grid.
```


**Natural Language Program**

1.  Create a new grid, `output_grid`, with the same dimensions as the `input_grid`, and initialize all its cells to 0.
2.  Scan the `input_grid` to find the coordinates of all cells containing the value 7.
3.  If no cells contain 7, return the initialized `output_grid`.
4.  Identify the coordinates of the topmost '7' (first found during a row-by-row, column-by-column scan) as `(seed_row, seed_col)`.
5.  Identify the coordinates of the bottommost '7' (last found during a row-by-row, column-by-column scan) as `(limit_row, limit_col)`. If only one '7' was found, `(limit_row, limit_col)` is the same as `(seed_row, seed_col)`.
6.  Calculate the maximum propagation distance using the Manhattan distance between the topmost and bottommost '7's: `max_dist = abs(seed_row - limit_row) + abs(seed_col - limit_col)`.
7.  Iterate through every cell `(r, c)` in the grid, from row 0 to `num_rows - 1` and column 0 to `num_cols - 1`.
8.  For each cell `(r, c)`, calculate its Manhattan distance to the seed cell: `current_dist = abs(r - seed_row) + abs(c - seed_col)`.
9.  Check if the `current_dist` is less than or equal to `max_dist`.
10. If `current_dist <= max_dist`:
    a.  Calculate the absolute difference between the current cell's column `c` and the seed cell's column `seed_col`: `col_diff = abs(c - seed_col)`.
    b.  Check the parity of `col_diff`.
    c.  If `col_diff` is even (`col_diff % 2 == 0`), set `output_grid[r][c] = 7`.
    d.  If `col_diff` is odd (`col_diff % 2 == 1`), set `output_grid[r][c] = 8`.
11. If `current_dist > max_dist`, the cell `output_grid[r][c]` remains 0 (its initialized value).
12. After iterating through all cells, return the completed `output_grid`.
