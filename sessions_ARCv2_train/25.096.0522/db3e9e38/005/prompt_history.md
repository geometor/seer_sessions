
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

Previous Code:
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
7 8 7 8 7 8 7 8
7 8 7 8 7 8 7 8
7 8 7 8 7 8 7 8
7 8 7 8 7 8 7 8
7 8 7 8 7 8 7 8
8 7 8 7 8 7 8 7
7 8 7 8 7 8 7 8
```
Match: False
Pixels Off: 34
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 121.42857142857143

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
8 7 8 7 8 7 8
8 7 8 7 8 7 8
8 7 8 7 8 7 8
7 8 7 8 7 8 7
```
Match: False
Pixels Off: 19
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 108.57142857142857
**General Assessment and Strategy**

The previous code (`code_00.py`) incorrectly assumed that the propagation should start from *all* cells containing '7' in the input and spread indefinitely via BFS. The results show that this leads to the entire grid being filled with alternating 7s and 8s, which does not match the expected outputs.

The expected outputs exhibit a bounded, diamond-like pattern originating from a single point. Comparing the input and output grids suggests the following revised hypothesis:

1.  **Single Seed:** The propagation originates from the *topmost* '7' found in the input grid.
2.  **Distance-Based Propagation:** The value assigned to a cell (7 or 8) depends on its Manhattan distance from the seed cell. Specifically, if the distance `d` is even, the value is 7; if `d` is odd, the value is 8.
3.  **Propagation Limit:** The propagation is limited. The pattern does not fill the entire grid. The extent of the propagation appears to be determined by the Manhattan distance between the topmost '7' (seed) and the *bottommost* '7' in the input grid. Let this maximum distance be `max_dist`. Only cells within `max_dist` (inclusive) from the seed are assigned a value (7 or 8); others remain 0.

**Strategy:**

1.  Implement functions to find the topmost and bottommost '7' coordinates.
2.  Calculate the Manhattan distance between these two points (`max_dist`).
3.  Iterate through each cell of the output grid.
4.  Calculate the Manhattan distance from the seed cell to the current cell (`dist`).
5.  If `dist <= max_dist`, assign 7 or 8 based on the parity of `dist`. Otherwise, assign 0.
6.  Use `tool_code` to verify coordinates, distances, and counts for the examples.

**Metrics Gathering**


*code_execution:*
```python
import numpy as np

def analyze_grid(grid_str):
    grid = np.array([[int(x) for x in row.split()] for row in grid_str.strip().split('\n')])
    rows, cols = grid.shape
    
    coords_7 = np.argwhere(grid == 7)
    num_7 = len(coords_7)
    
    topmost_7 = tuple(coords_7[0]) if num_7 > 0 else None
    bottommost_7 = tuple(coords_7[-1]) if num_7 > 0 else None
    
    max_dist = -1
    if topmost_7 and bottommost_7:
        max_dist = abs(topmost_7[0] - bottommost_7[0]) + abs(topmost_7[1] - bottommost_7[1])
        
    num_non_zero = np.count_nonzero(grid)
    
    return {
        "dimensions": (rows, cols),
        "num_7": num_7,
        "topmost_7": topmost_7,
        "bottommost_7": bottommost_7,
        "max_dist_7s": max_dist,
        "num_non_zero": num_non_zero
    }

# Example 1 Input
input_1_str = """
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
"""

# Example 1 Output
output_1_str = """
7 8 7 8 7 8 7 0
7 8 7 8 7 8 0 0
7 8 7 8 7 0 0 0
0 8 7 8 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
"""

# Example 2 Input
input_2_str = """
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
"""

# Example 2 Output
output_2_str = """
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
"""

metrics = {}
metrics['train_1_input'] = analyze_grid(input_1_str)
metrics['train_1_output'] = analyze_grid(output_1_str) # Analyze output based on non-zero count
metrics['train_1_output']['num_non_zero'] = np.count_nonzero(np.array([[int(x) for x in row.split()] for row in output_1_str.strip().split('\n')]))

metrics['train_2_input'] = analyze_grid(input_2_str)
metrics['train_2_output'] = analyze_grid(output_2_str) # Analyze output based on non-zero count
metrics['train_2_output']['num_non_zero'] = np.count_nonzero(np.array([[int(x) for x in row.split()] for row in output_2_str.strip().split('\n')]))


print(metrics)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{'train_1_input': {'dimensions': (7, 8), 'num_7': 5, 'topmost_7': (np.int64(0), np.int64(2)), 'bottommost_7': (np.int64(4), np.int64(2)), 'max_dist_7s': np.int64(4), 'num_non_zero': 5}, 'train_1_output': {'dimensions': (7, 8), 'num_7': 12, 'topmost_7': (np.int64(0), np.int64(0)), 'bottommost_7': (np.int64(4), np.int64(2)), 'max_dist_7s': np.int64(6), 'num_non_zero': 22}, 'train_2_input': {'dimensions': (5, 7), 'num_7': 4, 'topmost_7': (np.int64(0), np.int64(3)), 'bottommost_7': (np.int64(3), np.int64(3)), 'max_dist_7s': np.int64(3), 'num_non_zero': 4}, 'train_2_output': {'dimensions': (5, 7), 'num_7': 8, 'topmost_7': (np.int64(0), np.int64(1)), 'bottommost_7': (np.int64(3), np.int64(3)), 'max_dist_7s': np.int64(5), 'num_non_zero': 16}}

```
**YAML Facts**


```yaml
Task: Grid value propagation based on Manhattan distance from a seed, limited by distance between extremal seeds.

Objects:
  - Input_Grid:
      Type: 2D integer array
      Contains: Background value (0), Seed marker value (7)
      Structure: Primarily background values with one or more occurrences of the seed marker value, typically forming a vertical line.
  - Output_Grid:
      Type: 2D integer array
      Dimensions: Same as Input_Grid
      Contains: Background value (0), Propagation values (7, 8)
      Structure: A pattern of alternating propagation values forming a diamond shape centered on the Seed_Cell location, replacing original values up to a certain distance limit.
  - Seed_Cell:
      Identification: The cell in the Input_Grid containing the Seed marker value (7) with the minimum row index (topmost). If multiple 7s exist in the minimum row, the one with the minimum column index is chosen (though examples only show one per row).
      Properties: Row index (seed_row), Column index (seed_col), Value (7).
  - Limit_Cell:
      Identification: The cell in the Input_Grid containing the Seed marker value (7) with the maximum row index (bottommost). If multiple 7s exist in the maximum row, the one with the maximum column index is chosen (though examples only show one per row).
      Properties: Row index (limit_row), Column index (limit_col), Value (7).
  - Max_Distance:
      Calculation: The Manhattan distance between the Seed_Cell and the Limit_Cell. `max_dist = abs(seed_row - limit_row) + abs(seed_col - limit_col)`.
  - Propagation_Pattern:
      Values: Determined by Manhattan distance (`dist`) from the Seed_Cell. Value is 7 if `dist` is even, 8 if `dist` is odd.
      Mechanism: Applied to all cells `(r, c)` in the Output_Grid where the Manhattan distance `dist = abs(r - seed_row) + abs(c - seed_col)` is less than or equal to `Max_Distance`.

Relationships:
  - Origin: The center of the Propagation_Pattern in the Output_Grid is the Seed_Cell identified in the Input_Grid.
  - Limit: The extent of the Propagation_Pattern is determined by the Max_Distance calculated from the Input_Grid.
  - Value Assignment: The value (7 or 8) at a cell within the pattern depends on the parity of its Manhattan distance from the Seed_Cell.
  - Overwrite: The Propagation_Pattern overwrites the initial background value (0) of the Output_Grid cells it covers. Cells outside the Max_Distance remain 0.

Action:
  - Find_Extremal_Seeds: Locate the coordinates `(seed_row, seed_col)` of the topmost Seed marker value (7) and `(limit_row, limit_col)` of the bottommost Seed marker value (7) in the Input_Grid.
  - Handle_No_Seed: If no Seed marker value (7) is found, return an Output_Grid of the same size filled with the background value (0).
  - Calculate_Max_Distance: Compute the Manhattan distance `max_dist` between `(seed_row, seed_col)` and `(limit_row, limit_col)`.
  - Initialize_Output: Create an Output_Grid of the same size as the Input_Grid, filled with the background value (0).
  - Populate_Pattern: Iterate through each cell `(r, c)` of the Output_Grid:
      - Calculate the Manhattan distance `dist` from `(seed_row, seed_col)` to `(r, c)`.
      - If `dist <= max_dist`:
          - Assign 7 to `Output_Grid[r][c]` if `dist` is even.
          - Assign 8 to `Output_Grid[r][c]` if `dist` is odd.
```


**Natural Language Program**

1.  Initialize `seed_coords` and `limit_coords` to null or an indicator that they haven't been found.
2.  Scan the `input_grid` row by row, then column by column.
    a.  If a cell `(r, c)` contains the value 7:
        i.   If `seed_coords` is null, set `seed_coords = (r, c)`.
        ii.  Update `limit_coords = (r, c)` (this will naturally find the last/bottommost one after scanning completes).
3.  Get the dimensions (rows, cols) of the `input_grid`.
4.  Create a new grid, `output_grid`, with the same dimensions, initialized to all zeros.
5.  If `seed_coords` is still null (no 7 was found in the input), return the initialized `output_grid`.
6.  Extract `seed_row, seed_col` from `seed_coords` and `limit_row, limit_col` from `limit_coords`.
7.  Calculate the maximum allowed Manhattan distance: `max_dist = abs(seed_row - limit_row) + abs(seed_col - limit_col)`.
8.  Iterate through each cell `(r, c)` of the `output_grid` from `r = 0` to `rows - 1` and `c = 0` to `cols - 1`.
9.  For each cell `(r, c)`, calculate its Manhattan distance from the seed: `dist = abs(r - seed_row) + abs(c - seed_col)`.
10. If `dist <= max_dist`:
    a.  If `dist % 2 == 0` (distance is even), set `output_grid[r][c] = 7`.
    b.  If `dist % 2 != 0` (distance is odd), set `output_grid[r][c] = 8`.
11. Return the completed `output_grid`.
