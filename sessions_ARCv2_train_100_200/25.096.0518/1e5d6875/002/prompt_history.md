
## train_1

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 2 7 7 7
7 5 7 7 2 2 7 7
7 5 5 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7
7 7 7 7 2 2 7 7
```


**output:**
```
7 7 7 7 7 7 7 7
7 7 4 7 2 7 7 7
7 5 4 3 2 2 7 7
7 5 5 3 3 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7
7 7 7 7 2 2 3 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 5 7 7 7 5 5 7
7 5 5 7 7 7 5 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 2 2 7 7 2 7 7
7 7 2 7 7 2 2 7
7 7 7 7 7 7 7 7
```


**output:**
```
7 7 4 7 7 7 7 7
7 5 4 4 7 5 5 7
7 5 5 7 4 4 5 7
7 7 7 7 7 4 7 7
7 7 3 3 7 7 7 7
7 2 2 3 7 2 7 7
7 7 2 7 3 2 2 7
7 7 7 7 3 3 7 7
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Input/Output:** Both inputs and outputs are 8x8 grids containing single digits.
2.  **Values:** The digits present are 2, 5, and 7 in the input. The output introduces digits 3 and 4, while retaining 2, 5, and 7.
3.  **Background:** The digit 7 appears to be a background or default value. Many 7s remain unchanged.
4.  **Active Elements:** Digits 2 and 5 seem to be the active elements influencing the transformation. They remain unchanged in the output.
5.  **Transformation:** The core transformation involves changing some of the background 7s into either 3s or 4s. This change appears localized around the positions of the 2s and 5s.
6.  **Neighborhood Influence:** The transformation of a 7 seems dependent on its neighboring cells (including diagonals).
    *   In `train_1`, 7s near 2s tend to become 3s (`output[2][3]`, `output[3][3]`, `output[3][4]`, `output[7][6]`).
    *   In `train_1`, 7s near 5s tend to become 4s (`output[1][2]`, `output[2][2]`).
    *   In `train_2`, 7s near 2s tend to become 3s (`output[4][2]`, `output[4][3]`, `output[7][4]`, `output[7][5]`).
    *   In `train_2`, 7s near 5s tend to become 4s (`output[1][2]`, `output[1][3]`, `output[2][4]`, `output[2][5]`, `output[3][5]`, `output[3][6]`).
7.  **Conflict Resolution:** When a 7 is near both 2s and 5s, a rule determines the outcome.
    *   In `train_1`, `input[2][3]` (7) has neighbors: one 5, two 2s. It becomes 3.
    *   In `train_1`, `input[3][3]` (7) has neighbors: one 5, two 2s. It becomes 3.
    *   In `train_1`, `input[2][2]` (7) has neighbors: three 5s, zero 2s. It becomes 4.
    *   This suggests a comparison: if the count of neighboring 2s is greater than or equal to the count of neighboring 5s, the 7 becomes a 3. Otherwise (if count of 5s is greater), it becomes a 4.

**YAML Fact Document:**


```yaml
task_description: "Transform a grid of digits based on the proximity of specific values (2 and 5) to a background value (7)."
elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - size: 8x8 (in examples)
      - values: [2, 3, 4, 5, 7]
  - object: cell
    properties:
      - value: integer (2, 3, 4, 5, or 7)
      - position: (row, column) coordinates
      - neighbors: set of 8 adjacent cells (including diagonals, handling boundaries)
  - value: 7
    role: background/default value, potentially transformable
  - value: 2
    role: active influencer, transforms nearby 7s primarily to 3s
  - value: 5
    role: active influencer, transforms nearby 7s primarily to 4s
  - value: 3
    role: output value, result of transforming a 7 influenced primarily by 2s
  - value: 4
    role: output value, result of transforming a 7 influenced primarily by 5s
actions:
  - name: iterate_cells
    description: Process each cell of the input grid.
  - name: check_value
    description: Determine the value of the current cell.
  - name: count_neighbors
    description: For a given cell, count how many of its 8 neighbors have the value 2 and how many have the value 5.
  - name: apply_transformation_rule
    description: Based on the cell's original value and the counts of its neighbors (2s and 5s), determine the output cell value.
relationships:
  - type: adjacency
    description: Cells are related to their immediate neighbors (N, NE, E, SE, S, SW, W, NW).
  - type: influence
    description: Values 2 and 5 in neighboring cells influence the transformation of a cell containing 7.
  - type: comparison
    description: The counts of neighboring 2s and 5s are compared to decide the transformation outcome (3 or 4) when both types of neighbors exist.
```


**Natural Language Program:**

1.  Create a new output grid of the same dimensions as the input grid.
2.  Iterate through each cell `(r, c)` of the input grid.
3.  Get the value `v` of the input cell `input[r][c]`.
4.  **If `v` is not equal to 7:**
    *   Copy the value `v` directly to the corresponding output cell: `output[r][c] = v`.
5.  **If `v` is equal to 7:**
    *   Examine the 8 neighboring cells (North, Northeast, East, Southeast, South, Southwest, West, Northwest) of `input[r][c]`, handling grid boundaries appropriately.
    *   Count the number of neighbors whose value is 2 (let this be `count_2`).
    *   Count the number of neighbors whose value is 5 (let this be `count_5`).
    *   **If `count_2 > 0` and `count_5 == 0`:**
        *   Set the output cell value: `output[r][c] = 3`.
    *   **Else if `count_5 > 0` and `count_2 == 0`:**
        *   Set the output cell value: `output[r][c] = 4`.
    *   **Else if `count_2 > 0` and `count_5 > 0`:**
        *   **If `count_2 >= count_5`:**
            *   Set the output cell value: `output[r][c] = 3`.
        *   **Else (`count_5 > count_2`):**
            *   Set the output cell value: `output[r][c] = 4`.
    *   **Else (if `count_2 == 0` and `count_5 == 0`):**
        *   Keep the original value: `output[r][c] = 7`.
6.  Return the completed output grid.
```python
import copy

"""
Transforms a grid of digits based on the proximity of specific values (2 and 5) to a background value (7).

Iterates through each cell of the input grid. If a cell contains the value 7, it counts the number of its 8 neighbors (including diagonals) that contain the value 2 and the number of neighbors that contain the value 5.

Transformation rules for a cell containing 7:
- If it has neighbors with value 2 but no neighbors with value 5, it becomes 3.
- If it has neighbors with value 5 but no neighbors with value 2, it becomes 4.
- If it has neighbors with both values 2 and 5:
    - If the count of neighbors with value 2 is greater than or equal to the count of neighbors with value 5, it becomes 3.
    - Otherwise (count of 5s is greater), it becomes 4.
- If it has no neighbors with value 2 or 5, it remains 7.
Cells not containing 7 remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the 2D transformed output grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input
    # This handles keeping non-7 values and 7s with no relevant neighbors
    output_grid = copy.deepcopy(input_grid)

    # Define the 8 neighbor directions (row_offset, col_offset)
    neighbor_directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is a 7
            if input_grid[r][c] == 7:
                # Initialize counts for neighbors with values 2 and 5
                count_2 = 0
                count_5 = 0

                # Examine the 8 neighbors
                for dr, dc in neighbor_directions:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_value = input_grid[nr][nc]
                        # Increment counts based on neighbor value
                        if neighbor_value == 2:
                            count_2 += 1
                        elif neighbor_value == 5:
                            count_5 += 1

                # Apply transformation rules based on neighbor counts
                if count_2 > 0 and count_5 == 0:
                    output_grid[r][c] = 3
                elif count_5 > 0 and count_2 == 0:
                    output_grid[r][c] = 4
                elif count_2 > 0 and count_5 > 0:
                    if count_2 >= count_5:
                        output_grid[r][c] = 3
                    else:
                        output_grid[r][c] = 4
                # If count_2 == 0 and count_5 == 0, the value remains 7 (already set by deepcopy)

    return output_grid
```
