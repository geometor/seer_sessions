
## train_1

**input:**
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```


**output:**
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```


## train_2

**input:**
```
1 1 1
1 0 1
1 1 1
```


**output:**
```
0 1 0
1 0 1
0 1 0
```


## train_3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```


**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

**Perception of Task Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids (matrices) of integers.
2.  **Input Content:** Each input grid contains a single cell with the value '0'. All other cells contain a uniform positive integer (e.g., 2, 1, or 3), which acts as a "background" value.
3.  **Output Content:** The output grid has the same dimensions as the input grid. It contains cells with the value '0' and cells with the original background value. The '0' from the input grid always corresponds to a '0' in the same position in the output grid. Additional cells in the output grid are also changed to '0'.
4.  **Transformation Pattern:** The transformation seems to depend on the position of the '0' in the input grid. The cells that become '0' in the output form a pattern related to their distance from the original '0'. Specifically, the pattern resembles cells whose Manhattan distance (sum of absolute differences in row and column coordinates) from the original '0' is an even number.

**YAML Facts:**


```yaml
Task: Grid Transformation based on Manhattan Distance Parity

Objects:
  - InputGrid:
      Type: 2D List/Array of Integers
      Properties:
        - rows: Integer (number of rows)
        - columns: Integer (number of columns)
        - cells: List of Lists of Integers
        - background_value: Integer (the non-zero value filling most of the grid)
        - zero_position: Tuple (row_index, column_index) of the '0' cell
  - OutputGrid:
      Type: 2D List/Array of Integers
      Properties:
        - rows: Integer (same as InputGrid)
        - columns: Integer (same as InputGrid)
        - cells: List of Lists of Integers
  - Cell:
      Type: Element within a Grid
      Properties:
        - value: Integer
        - position: Tuple (row_index, column_index)

Relationships:
  - OutputGrid dimensions are identical to InputGrid dimensions.
  - A Cell's value in the OutputGrid depends on its position relative to the InputGrid's zero_position.

Actions:
  - Identify the background_value in the InputGrid.
  - Locate the zero_position in the InputGrid.
  - For each Cell position (r, c) in the target OutputGrid dimensions:
      - Calculate the Manhattan distance between (r, c) and the zero_position.
      - Determine if the Manhattan distance is even or odd.
      - Set the OutputGrid Cell value at (r, c):
          - to '0' if the Manhattan distance is even.
          - to the background_value if the Manhattan distance is odd.

Derived Properties:
  - Manhattan Distance:
      Definition: For two positions (r1, c1) and (r2, c2), the distance is |r1 - r2| + |c1 - c2|.
      Usage: Calculated between each potential output cell position and the input zero_position.
  - Parity:
      Definition: Whether an integer is even or odd.
      Usage: Applied to the calculated Manhattan distance.
```


**Natural Language Program:**

1.  Initialize the output grid with the same dimensions as the input grid.
2.  Identify the unique non-zero integer value in the input grid; this is the `background_value`.
3.  Find the row and column index (`zero_row`, `zero_col`) of the cell containing '0' in the input grid.
4.  Iterate through each cell position (`r`, `c`) of the grid (from row 0 to max_row, and column 0 to max_col).
5.  For the current cell position (`r`, `c`), calculate the Manhattan distance to the zero cell: `distance = abs(r - zero_row) + abs(c - zero_col)`.
6.  Check if the calculated `distance` is even (i.e., `distance % 2 == 0`).
7.  If the `distance` is even, set the value of the cell at position (`r`, `c`) in the output grid to '0'.
8.  If the `distance` is odd, set the value of the cell at position (`r`, `c`) in the output grid to the `background_value`.
9.  Return the completed output grid.
```python
import math

"""
Transforms an input grid based on Manhattan distance parity from a central '0'.

1. Identifies the background value (the non-zero integer) in the input grid.
2. Locates the position (row, column) of the '0' cell in the input grid.
3. Creates an output grid of the same dimensions as the input grid.
4. Iterates through each cell position (r, c) in the grid.
5. Calculates the Manhattan distance between the current cell (r, c) and the '0' cell's position.
6. If the Manhattan distance is even, the corresponding cell in the output grid is set to '0'.
7. If the Manhattan distance is odd, the corresponding cell in the output grid is set to the identified background value.
8. Returns the completed output grid.
"""

def find_zero_position(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the row and column index of the first '0' found in the grid."""
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 0:
                return r, c
    return None # Should not happen based on problem description

def find_background_value(grid: list[list[int]], zero_pos: tuple[int, int]) -> int:
    """Finds the non-zero background value in the grid."""
    # Check a corner cell first, assuming it's not the zero cell
    if zero_pos != (0, 0) and grid[0][0] != 0:
        return grid[0][0]
    # If the top-left is zero, iterate to find the first non-zero
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                return value
    return -1 # Should not happen based on problem description

def calculate_manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the Manhattan distance parity transformation to the input grid."""

    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Find the location of the '0'
    zero_pos = find_zero_position(input_grid)
    if zero_pos is None:
         # Handle cases where 0 might not be present, though constraints imply it is.
         # For now, maybe return a copy or raise error. Let's return a copy.
         print("Warning: No zero found in input grid.")
         return [row[:] for row in input_grid]
    zero_row, zero_col = zero_pos

    # Find the background value
    background_value = find_background_value(input_grid, zero_pos)

    # Initialize the output grid (can be done element by element)
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the Manhattan distance from the current cell to the '0' cell
            distance = calculate_manhattan_distance((r, c), (zero_row, zero_col))

            # Check if the distance is even or odd
            if distance % 2 == 0:
                # If even, set the output cell to 0
                output_grid[r][c] = 0
            else:
                # If odd, set the output cell to the background value
                output_grid[r][c] = background_value

    # Return the completed output grid
    return output_grid
```
