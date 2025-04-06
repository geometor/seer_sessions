
## train_1

**input:**
```
0 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 4
0 0 4 0 0 0 4 0
0 0 0 4 0 4 0 0
0 0 0 0 4 0 0 0
2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 4 0 0 0 0
0 0 0 0 4 0
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
4 0 0 0 0 0
0 4 0 0 0 0
0 0 4 0 0 0
0 4 0 4 0 4
0 0 0 0 4 0
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0
0 4 0
0 0 0
0 0 0
2 2 2
0 0 0
```


**output:**
```
0 0 0
0 0 0
0 4 0
0 0 0
2 2 2
0 0 0
```


## train_4

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
0 0 0 0 0
2 2 2 2 2
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
4 0 0 0 4
0 4 0 4 0
0 0 4 0 0
2 2 2 2 2
```

Okay, analyzing the provided examples, here's my perception and breakdown of the task:

**Perception of Elements:**

The task involves transforming a 2D grid of integers based on a gravity-like simulation applied to specific elements.

1.  **Grid Structure:** Both input and output are rectangular grids (matrices) containing integers.
2.  **Cell Values:** The grids primarily contain 0s (representing empty space), 4s (representing movable objects), and a single horizontal line of 2s (representing a solid boundary or floor).
3.  **Boundary Line:** The row composed entirely of 2s acts as an impenetrable barrier. Its position and values remain constant between input and output.
4.  **Movable Objects:** The number 4 represents objects that are subject to "gravity".
5.  **Gravity Simulation:** The core transformation involves the 4s "falling" downwards within their respective columns.
6.  **Stopping Conditions:** A falling 4 stops when it reaches the row immediately above the boundary line (the row of 2s) or immediately above another 4 that has already settled in the same column.
7.  **Empty Space:** As a 4 falls, its original position becomes 0 (empty space).
8.  **Column Independence:** The falling process happens independently within each column. The movement of a 4 in one column does not directly influence the movement in another column, except by potentially creating a landing spot for a 4 originally above it in the *same* column.

**YAML Facts:**


```yaml
task_type: grid_transformation
components:
  - type: grid
    description: A 2D array representing the state.
    properties:
      - cells: Contains integer values (0, 2, 4).
  - type: element
    value: 4
    description: Represents a movable object subject to gravity.
    behavior: Falls downwards within its column.
  - type: element
    value: 0
    description: Represents empty space.
  - type: element
    value: 2
    description: Represents an impassable boundary element.
    properties:
      - arrangement: Forms a continuous horizontal row.
      - immutability: Position and value remain unchanged.
rules:
  - rule: boundary_identification
    description: Identify the row composed entirely of 2s. This row acts as the primary stopping point.
  - rule: gravity_simulation
    description: Process each column independently from bottom to top (above the boundary).
    steps:
      - Identify all 4s in the column above the boundary.
      - Clear the original positions of these 4s (set to 0).
      - Determine the lowest available landing spot for each identified 4, starting from the row just above the boundary or the highest settled 4 in that column.
      - Place the 4s sequentially into their final settled positions within the column.
constraints:
  - Movement is purely vertical (within columns).
  - Objects (4s) cannot pass through the boundary (2s) or other settled objects (4s).
  - The boundary row (2s) is static.
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify the row index of the horizontal line consisting entirely of the number 2 (the boundary row).
3.  Iterate through each column of the grid independently.
4.  For the current column, collect the row indices of all cells containing the number 4 that are located *above* the identified boundary row.
5.  In the output grid for the current column, set the original positions (identified in step 4) of these 4s to 0.
6.  Determine the target "floor" row index for the current column. This is the index of the boundary row identified in step 2.
7.  Iterate through the rows of the current column in the output grid, starting from the row just *above* the target floor row index and moving upwards towards row 0.
8.  Maintain a count of how many 4s have been collected (from step 4) for this column.
9.  If the count of collected 4s is greater than zero and the current cell being examined (in the upward iteration) is a potential landing spot (i.e., it's above the floor and currently 0, or it *is* the lowest available spot), place a 4 in this cell in the output grid and decrement the count of collected 4s. Continue placing 4s upwards in consecutive cells until all collected 4s for that column are placed. More accurately: Starting from the row immediately above the boundary row, fill cells upwards with the collected 4s for that column, up to the number of 4s collected.
10. Repeat steps 4-9 for all columns.
11. The modified output grid is the final result.
```python
import copy

"""
Simulates gravity on elements marked '4' within a grid.
The grid contains 0s (empty space), 4s (movable objects), and a single horizontal row of 2s (impassable boundary).
Objects (4s) fall downwards within their respective columns until they land on the row immediately above the boundary (2s) or immediately above another settled 4 in the same column.
The boundary row remains static. The process happens independently for each column.
"""

def find_boundary_row(grid: list[list[int]]) -> int:
    """Finds the index of the row consisting entirely of 2s."""
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    for r in range(num_rows):
        if all(grid[r][c] == 2 for c in range(num_cols)):
            return r
    return -1 # Should not happen based on problem description, but good practice

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies gravity to '4' elements in the grid, making them fall
    towards a boundary row of '2's.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid with '4's settled.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Find the boundary row (row of 2s)
    boundary_row_idx = find_boundary_row(output_grid)

    # If no boundary row is found, return the original grid (or handle as error)
    if boundary_row_idx == -1:
        # This case implies invalid input according to the examples
        print("Warning: Boundary row (all 2s) not found.")
        return output_grid 
        
    # Iterate through each column independently
    for c in range(num_cols):
        # Count the number of '4's in this column above the boundary
        fours_count = 0
        for r in range(boundary_row_idx): # Iterate rows above the boundary
            if output_grid[r][c] == 4:
                fours_count += 1
                # Clear the original position of the 4 in the output grid
                output_grid[r][c] = 0

        # Place the counted '4's starting from the row just above the boundary
        # and moving upwards
        landing_row = boundary_row_idx - 1
        for _ in range(fours_count):
            # Ensure we don't try to place a 4 outside the grid bounds (above row 0)
            # or overwrite the boundary itself (though the loop range prevents this)
            if landing_row >= 0:
                output_grid[landing_row][c] = 4
                landing_row -= 1 # Move the next landing spot one row up

    return output_grid
```
