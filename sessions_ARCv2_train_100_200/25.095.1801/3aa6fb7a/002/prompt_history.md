
## train_1

**input:**
```
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 8 0 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 8 8 0 0
```


**output:**
```
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 8 1 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 1 8 0 0
0 0 0 8 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 8 1 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task involves transforming a 2D grid of numbers.
    *   The input grids contain only 0s and 8s.
    *   The output grids contain 0s, 1s, and 8s.
    *   The dimensions of the input and output grids are identical for each example.
    *   The positions of the number 8 remain unchanged from input to output.
    *   Some cells containing 0 in the input are changed to 1 in the output.
    *   The change from 0 to 1 appears to depend on the neighboring cells. Specifically, it seems related to the count of neighbors with the value 8.

*   **Facts:**
    
```yaml
    objects:
      - grid: A 2D array of integers.
      - cell: An individual element within the grid, defined by its row, column, and value.
      - neighbors: The set of 8 cells directly or diagonally adjacent to a given cell.
    properties:
      - cell.value: The integer value of a cell (0, 1, or 8).
      - cell.position: The (row, column) coordinates of a cell.
    actions:
      - transform_grid: Modifies the input grid to produce the output grid.
      - update_cell_value: Changes the value of a specific cell from 0 to 1 based on a condition.
    relationships:
      - rule: A cell's value in the output grid depends on its value and its neighbors' values in the input grid.
      - condition: A cell with value 0 in the input grid changes to 1 in the output grid if and only if it has exactly three neighbors with the value 8 in the input grid.
      - invariance: Cells with value 8 in the input grid retain their value and position in the output grid. Cells with value 0 that do not meet the condition also retain their value (0).
    ```


*   **Natural Language Program:**
    1.  Create a new grid (output grid) with the same dimensions as the input grid.
    2.  Iterate through each cell (identified by its row and column) of the input grid.
    3.  For the current cell, examine its value in the input grid.
    4.  If the input cell's value is 8, copy the value 8 to the corresponding cell in the output grid.
    5.  If the input cell's value is 0:
        a.  Count how many of its eight neighboring cells (horizontally, vertically, and diagonally adjacent) have the value 8 in the input grid.
        b.  If the count of neighbors with value 8 is exactly 3, set the value of the corresponding cell in the output grid to 1.
        c.  Otherwise (if the count is not 3), set the value of the corresponding cell in the output grid to 0.
    6.  Return the completed output grid.
```python
import copy

"""
Transforms an input grid based on the following rule:
Iterate through each cell of the input grid.
If the input cell's value is 8, keep it as 8 in the output grid.
If the input cell's value is 0, count its 8 neighbors (horizontally, vertically, and diagonally).
If the count of 8-neighbors is exactly 3, set the corresponding output cell's value to 1.
Otherwise (if the input cell is 0 and the neighbor count is not 3), keep the output cell's value as 0.
"""

def count_neighbors(grid: list[list[int]], r: int, c: int, target_value: int) -> int:
    """Counts the neighbors of cell (r, c) with the target_value."""
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    # Iterate through the 8 possible neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == target_value:
                    count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    A cell with value 0 becomes 1 if it has exactly three neighbors with value 8.
    Cells with value 8 remain unchanged.
    Other cells with value 0 remain 0.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell's value in the input grid is 0
            if input_grid[r][c] == 0:
                # Count neighbors with value 8 in the input grid
                neighbor_count_8 = count_neighbors(input_grid, r, c, 8)
                
                # Apply the rule: if count is exactly 3, change cell in output grid to 1
                if neighbor_count_8 == 3:
                    output_grid[r][c] = 1
            # If the input cell value is 8, it remains 8 (already handled by deepcopy)
            # If the input cell value is 0 and neighbor count is not 3, it remains 0 (already handled by deepcopy)

    return output_grid
```
