
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
7 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 7 4 7 0
0 0 0 0 0 7 4 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
4 7 4 0 0 0 0 0 0
7 7 4 0 0 0 0 0 0
0 0 0 0 0 4 4 7 0
0 0 0 0 0 7 4 4 0
0 0 0 0 0 4 7 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Perception of Elements

1.  **Data Structure**: The input and output are both 2D grids (or matrices) of integers. The grid size appears consistent (9x9 in the examples).
2.  **Cell Values**: The grids contain three distinct integer values: 0, 4, and 7.
3.  **Input Pattern**: The input grids consist primarily of 0s, representing a background. Within this background, there are one or more connected regions composed of the value 4.
4.  **Output Pattern**: The output grids retain the original structure of the 0s and 4s from the input. However, some 0s in the input have been changed to 7s in the output.
5.  **Transformation Locus**: The changes (0 -> 7) occur specifically at positions that were originally 0 in the input grid and are adjacent (including diagonals) to cells containing the value 4.
6.  **Invariance**: Cells that initially contain 4 remain 4. Cells that initially contain 0 and are *not* adjacent to any 4 remain 0.

## YAML Facts


```yaml
task_type: grid_transformation
grid_properties:
  size: 9x9 (based on examples)
  dimensionality: 2
cell_values:
  - value: 0
    role: background
  - value: 4
    role: foreground_object / trigger
  - value: 7
    role: modified_background / output_marker
objects:
  - type: grid_cell
    properties:
      - value: integer (0, 4, or 7)
      - position: (row, column)
  - type: region
    properties:
      - composed_of: value 4
      - connectivity: connected cells (sharing sides or corners)
relationships:
  - type: adjacency
    definition: Cells sharing a side or a corner (Moore neighborhood)
    applies_to: grid_cells
action:
  - type: conditional_value_change
    target: cells with value 0
    condition: target cell must be adjacent (Moore neighborhood) to at least one cell with value 4
    result: target cell value changes from 0 to 7
invariants:
  - Cells with value 4 do not change.
  - Cells with value 0 that do not meet the adjacency condition do not change.
```


## Natural Language Program

1.  Initialize an output grid identical to the input grid.
2.  Iterate through each cell `(r, c)` of the input grid.
3.  If the value of the input cell `input[r][c]` is 0:
    a.  Examine the 8 neighboring cells (including diagonals) around `(r, c)` in the input grid.
    b.  Check if any of these neighbors has the value 4.
    c.  If at least one neighbor has the value 4, set the corresponding cell in the output grid `output[r][c]` to 7.
    d.  If no neighbor has the value 4, the cell `output[r][c]` retains its value (which is 0, as copied in step 1).
4.  If the value of the input cell `input[r][c]` is 4, the cell `output[r][c]` retains its value (which is 4, as copied in step 1).
5.  Return the final output grid.
```python
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the following rule:
    If a cell in the input grid has a value of 0 and is adjacent (including diagonals) 
    to at least one cell with a value of 4, its value is changed to 7 in the output grid. 
    All other cells retain their original values.
    """
    # Get the dimensions of the grid
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize the output grid as a deep copy of the input grid
    # This handles the invariant cases (cells with 4 or 0s not adjacent to 4s)
    output_grid = copy.deepcopy(input_grid)

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the input grid is 0
            if input_grid[r][c] == 0:
                found_4_neighbor = False
                # Examine the 8 neighboring cells
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the input grid has the value 4
                        if input_grid[nr][nc] == 4:
                            found_4_neighbor = True
                            break  # Found a 4, no need to check other neighbors

                # If at least one neighbor has the value 4, update the output grid cell to 7
                if found_4_neighbor:
                    output_grid[r][c] = 7
            # If the input cell is not 0 (i.e., it's 4), it remains unchanged 
            # in the output grid because we initialized output_grid as a copy.

    # Return the final transformed grid
    return output_grid
```
