
## train_1

**input:**
```
1 0 1
1 7 1
1 1 1
```


**output:**
```
1 0 1
1 0 1
1 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0
0 2 2 0 5 5 0 0 0 0 0
0 2 2 0 5 5 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 8 0 0 0 0
0 0 0 0 6 0 0 8 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 3 0 0 6 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 6 0 0 0 0 0 0 0 0 0 0 0
0 3 0 6 6 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 7 8 0 7 0 0 0
0 0 0 0 0 0 0 7 0 8 8 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 8 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 8 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 3 0 0 6 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 8 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 8 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 5 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 0 0 0 0 9
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 0 0 0 0 9
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves processing a 2D grid of integers. The transformation rule appears to selectively change some non-zero integer values back to 0 based on their neighboring cells. Cells with the value 0 seem to remain unchanged. The non-zero values likely represent different types of objects or "colors". The core pattern is that a non-zero cell is "erased" (set to 0) if it is orthogonally adjacent to another cell containing a *different* non-zero value. Cells that are only adjacent to cells with the same non-zero value or zero value remain unchanged.

## Facts


```yaml
task_type: grid_transformation
grid_elements:
  - type: integer
    value_range: 0-9 (based on examples)
    role: background (0), object_color (non-zero)
objects:
  - id: cell
    properties:
      - value: integer
      - row_index: integer
      - column_index: integer
      - neighbors: list of adjacent cells (orthogonal)
relationships:
  - type: adjacency
    between: [cell, cell]
    definition: Two cells are adjacent if they share an edge (orthogonally: up, down, left, right).
actions:
  - name: evaluate_cell
    input: cell (from input grid)
    condition: cell.value != 0
    sub_actions:
      - name: check_neighbors
        input: cell, input_grid
        output: keep_flag (boolean)
        logic: |
          Iterate through orthogonal neighbors.
          If any neighbor exists and has a value `v` such that `v != 0` and `v != cell.value`,
          set `keep_flag = False` and stop checking neighbors.
          Otherwise, `keep_flag = True`.
      - name: update_output_cell
        input: cell, keep_flag
        target: corresponding cell in output grid
        logic: |
          If `keep_flag` is False, set output cell value to 0.
          Otherwise, set output cell value to input cell value.
  - name: copy_zero_cell
    input: cell (from input grid)
    condition: cell.value == 0
    target: corresponding cell in output grid
    logic: Set output cell value to 0.
transformation_goal: Create an output grid where non-zero cells from the input are set to 0 if they have any orthogonal neighbor with a different non-zero value.
```


## Natural Language Program

1.  Create a new grid (`output_grid`) with the same dimensions as the `input_grid`.
2.  Iterate through each cell of the `input_grid` using its row index `r` and column index `c`.
3.  Get the value of the current cell in the `input_grid`: `input_value = input_grid[r][c]`.
4.  If `input_value` is 0, set the corresponding cell in the `output_grid` to 0 (`output_grid[r][c] = 0`) and continue to the next cell.
5.  If `input_value` is not 0, assume initially that the value should be kept: set a flag `should_erase = False`.
6.  Define the coordinates of the orthogonal neighbors: `(r-1, c)`, `(r+1, c)`, `(r, c-1)`, `(r, c+1)`.
7.  For each neighbor coordinate `(nr, nc)`:
    a.  Check if the neighbor coordinate is within the bounds of the `input_grid`.
    b.  If it is within bounds, get the neighbor's value: `neighbor_value = input_grid[nr][nc]`.
    c.  Check if the `neighbor_value` is different from 0 AND different from the `input_value`.
    d.  If both conditions in step 7c are true, set `should_erase = True` and break out of the neighbor-checking loop (no need to check other neighbors for this cell).
8.  After checking all neighbors (or breaking early), if `should_erase` is `True`, set the corresponding cell in the `output_grid` to 0 (`output_grid[r][c] = 0`).
9.  If `should_erase` is `False`, copy the `input_value` to the corresponding cell in the `output_grid` (`output_grid[r][c] = input_value`).
10. After iterating through all cells, return the `output_grid`.
```python
import copy

"""
Creates an output grid where non-zero cells from the input are set to 0 
if they have any orthogonal neighbor (up, down, left, right) with a 
different non-zero value. Cells with value 0 remain 0. Non-zero cells 
that are only adjacent to cells with the same non-zero value or 0 remain 
unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on neighbor values.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid.
    # We will modify this grid by setting cells to 0 where needed.
    output_grid = copy.deepcopy(input_grid)

    # Define orthogonal neighbor offsets
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # Iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current cell in the input_grid
            input_value = input_grid[r][c]

            # Skip processing if the cell value is 0 (it's already correct in output)
            if input_value == 0:
                continue

            # Assume initially that the value should not be erased
            should_erase = False

            # Check orthogonal neighbors
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # Check if the neighbor coordinate is within the bounds of the input_grid
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Get the neighbor's value from the *original* input_grid
                    neighbor_value = input_grid[nr][nc]

                    # Check if the neighbor_value is different from 0 AND different from the input_value
                    if neighbor_value != 0 and neighbor_value != input_value:
                        # If such a neighbor exists, mark this cell for erasing
                        should_erase = True
                        # Break the inner loop (no need to check other neighbors)
                        break 
            
            # If the cell was marked for erasing, set its value to 0 in the output_grid
            if should_erase:
                output_grid[r][c] = 0
            # Otherwise, the value remains as it was copied initially.

    # Return the modified output_grid
    return output_grid
```
```python
import copy

"""
Creates an output grid where non-zero cells from the input are set to 0 
if they have any orthogonal neighbor (up, down, left, right) with a 
different non-zero value. Cells with value 0 remain 0. Non-zero cells 
that are only adjacent to cells with the same non-zero value or 0 remain 
unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on neighbor values.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        # Handle empty rows case
        return [[] for _ in range(rows)]

    # 1. Create a new grid (output_grid) with the same dimensions as the input_grid.
    # We initialize it as a deep copy, then modify it.
    output_grid = copy.deepcopy(input_grid)

    # Define orthogonal neighbor offsets
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # 2. Iterate through each cell of the input_grid using its row index r and column index c.
    for r in range(rows):
        for c in range(cols):
            # 3. Get the value of the current cell in the input_grid.
            input_value = input_grid[r][c]

            # 4. If input_value is 0, the corresponding cell in output_grid is already 0 (from copy), so skip.
            if input_value == 0:
                continue

            # 5. If input_value is not 0, assume initially that the value should be kept.
            should_erase = False

            # 6. Define the coordinates of the orthogonal neighbors (done via offsets).
            # 7. For each neighbor coordinate (nr, nc):
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # 7a. Check if the neighbor coordinate is within the bounds of the input_grid.
                if 0 <= nr < rows and 0 <= nc < cols:
                    # 7b. If it is within bounds, get the neighbor's value from the original input grid.
                    neighbor_value = input_grid[nr][nc]

                    # 7c. Check if the neighbor_value is different from 0 AND different from the input_value.
                    if neighbor_value != 0 and neighbor_value != input_value:
                        # 7d. If both conditions are true, set should_erase = True and break.
                        should_erase = True
                        break # No need to check other neighbors for this cell

            # 8. After checking all neighbors (or breaking early), if should_erase is True, set output cell to 0.
            if should_erase:
                output_grid[r][c] = 0
            # 9. If should_erase is False, the output cell retains the input_value (already set by deepcopy).

    # 10. After iterating through all cells, return the output_grid.
    return output_grid
```
```python
import copy

"""
Creates an output grid based on the input grid. Iterates through each cell 
in the input grid. If a cell has a non-zero value, it checks its orthogonal 
neighbors (up, down, left, right). If any neighbor has a non-zero value that 
is *smaller* than the current cell's value, then the current cell's value is 
set to 0 in the output grid. Otherwise (if all non-zero neighbors have values 
equal to or greater than the current cell, or if all neighbors are zero), 
the current cell's value is kept in the output grid. Cells with value 0 in 
the input grid remain 0 in the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on comparing cell values with their 
    smaller non-zero neighbors.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        # Handle empty rows case
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid.
    # We will modify this grid by setting cells to 0 where needed based on the rule.
    output_grid = copy.deepcopy(input_grid)

    # Define orthogonal neighbor offsets
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    # Iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current cell from the original input grid
            input_value = input_grid[r][c]

            # Skip processing if the cell value is 0 (it remains 0 in the output)
            if input_value == 0:
                continue

            # Flag to determine if the current cell should be erased
            should_erase = False

            # Check orthogonal neighbors
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # Check if the neighbor coordinate is within the bounds of the input_grid
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Get the neighbor's value from the *original* input_grid
                    neighbor_value = input_grid[nr][nc]

                    # Check the core condition: erase if a neighbor has a smaller non-zero value
                    if 0 < neighbor_value < input_value:
                        # If such a neighbor exists, mark this cell for erasing
                        should_erase = True
                        # Break the inner loop (no need to check other neighbors)
                        break 
            
            # If the cell was marked for erasing, set its value to 0 in the output_grid
            if should_erase:
                output_grid[r][c] = 0
            # Otherwise, the value remains as it was copied initially from input_grid.

    # Return the modified output_grid
    return output_grid
```
