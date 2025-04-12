
## train_1

**input:**
```
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 3 0 3 1 1
0 0 0 0 0 3 0 3 1 1
0 0 0 0 2 3 0 3 1 1
0 0 0 0 2 3 0 3 1 1
0 2 2 2 2 3 3 3 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 3 1 3 1 1
0 0 0 0 0 3 1 3 1 1
0 0 0 0 2 3 1 3 1 1
0 0 0 0 2 3 1 3 1 1
0 2 2 2 2 3 3 3 1 1
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 1
0 0 3 0 0 0 0 1 1 1
0 0 3 0 0 0 0 1 1 1
0 0 3 0 0 0 1 1 1 1
0 0 3 0 0 3 1 1 1 1
0 0 3 0 0 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 3 3 3 5 5 5 5
```


**output:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 1 1 1 1 1 1 1
0 0 3 1 1 3 1 1 1 1
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 3 3 3 5 5 5 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
9 9 1 1 0 0 0 0 9 9
0 9 9 1 0 0 0 9 9 0
0 0 9 9 0 0 0 9 0 0
0 0 0 9 0 0 9 9 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 4 0 0 0 0
2 0 0 4 0 4 0 0 0 0
2 0 2 4 0 4 0 0 0 0
2 2 2 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 9 9
0 9 9 0 0 0 0 9 9 0
0 0 9 9 0 0 0 9 0 0
0 0 0 9 0 0 9 9 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 4 0 0 0 0
2 0 0 4 1 4 0 0 0 0
2 1 2 4 1 4 0 0 0 0
2 2 2 4 4 4 0 0 0 0
```

*   **Perception:** The task involves transforming a 2D grid of numbers (colors). The core transformation observed in all examples is changing certain cells with value 0 to value 1. Cells with other non-zero values remain unchanged. The specific locations where the 0s change to 1s seem dependent on the values of their immediate orthogonal neighbors in the input grid. Examples 1 and 3 show a clear pattern where a 0 changes to a 1 if it is directly between two identical non-zero numbers either horizontally (left/right neighbors are the same and non-zero) or vertically (top/bottom neighbors are the same and non-zero). Example 2 also involves 0s changing to 1s, but the pattern doesn't consistently fit the rule observed in examples 1 and 3. Specifically, some 0s change without being flanked by identical non-zero neighbors, and one 0 that *is* flanked vertically by identical non-zero neighbors (1s) does *not* change. However, the rule identified in examples 1 and 3 is the most consistent pattern observed.

*   **Facts:**
    ```yaml
    task_type: grid_transformation
    grid_properties:
      dimensionality: 2
      cell_values: integers (0-9)
      size: 10x10 (consistent across examples)
    objects:
      - name: cell
        properties:
          - value: integer (color)
          - position: (row, column)
      - name: grid
        properties:
          - cells: collection of cell objects
    relationships:
      - type: adjacency
        between: cell, cell
        properties:
          - direction: orthogonal (North, South, East, West)
          - definition: cells sharing an edge
      - type: flanking
        definition: A cell is flanked horizontally if its West and East neighbors exist and have identical non-zero values. A cell is flanked vertically if its North and South neighbors exist and have identical non-zero values.
    transformation:
      action: change_cell_value
      target_object: cell
      input_condition: cell value is 0
      rule_condition: The cell is flanked either horizontally or vertically by identical non-zero values in the input grid.
      output_value: 1
      fallback_action: keep original cell value if conditions are not met
    uncertainties:
      - Example train_2 does not fully conform to the identified flanking rule. Some cells change without meeting the condition, and one cell meets the condition but does not change. This suggests either a refinement to the rule or a conditional application based on other grid properties specific to train_2 (like the presence of color 5) might be needed, but the core flanking rule works for train_1 and train_3.
    ```

*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each cell `C` at position (row, column) in the input grid.
    3.  Check if the value of cell `C` in the input grid is 0.
    4.  If the value is 0, then check its orthogonal neighbors:
        *   Check the West neighbor (row, column-1) and East neighbor (row, column+1). If both neighbors exist, are non-zero, and have the *same* value, then change the value of cell `C` at (row, column) in the output grid to 1.
        *   Else, check the North neighbor (row-1, column) and South neighbor (row+1, column). If both neighbors exist, are non-zero, and have the *same* value, then change the value of cell `C` at (row, column) in the output grid to 1.
    5.  If the value of cell `C` is not 0, or if it is 0 but neither the horizontal nor vertical flanking condition is met, keep its original value in the output grid.
    6.  Return the final output grid.
```python
"""
Transforms a 2D grid by changing the value of certain cells from 0 to 1 based on their orthogonal neighbors.
A cell's value is changed from 0 to 1 if it is directly flanked either horizontally or vertically by two identical, non-zero neighboring cells in the input grid. Otherwise, the cell's value remains unchanged.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return output_grid # Handle empty grid case
    cols = len(input_grid[0])
    if cols == 0:
        return output_grid # Handle empty row case

    # Iterate through each cell in the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell value in the input grid is 0
            if input_grid[r][c] == 0:
                # Check for horizontal flanking
                # Check if left neighbor exists (c > 0)
                has_left_neighbor = c > 0
                # Check if right neighbor exists (c < cols - 1)
                has_right_neighbor = c < cols - 1
                
                if has_left_neighbor and has_right_neighbor:
                    left_neighbor_val = input_grid[r][c-1]
                    right_neighbor_val = input_grid[r][c+1]
                    # Check if neighbors are identical and non-zero
                    if left_neighbor_val != 0 and left_neighbor_val == right_neighbor_val:
                        # Change the cell in the output grid to 1
                        output_grid[r][c] = 1
                        continue # Move to the next cell, no need to check vertical

                # Check for vertical flanking (only if horizontal condition was not met)
                # Check if top neighbor exists (r > 0)
                has_top_neighbor = r > 0
                # Check if bottom neighbor exists (r < rows - 1)
                has_bottom_neighbor = r < rows - 1

                if has_top_neighbor and has_bottom_neighbor:
                    top_neighbor_val = input_grid[r-1][c]
                    bottom_neighbor_val = input_grid[r+1][c]
                    # Check if neighbors are identical and non-zero
                    if top_neighbor_val != 0 and top_neighbor_val == bottom_neighbor_val:
                        # Change the cell in the output grid to 1
                        output_grid[r][c] = 1
                        
            # If the cell value is not 0, or if flanking conditions are not met,
            # the value in output_grid remains as copied from input_grid initially.

    # Return the final transformed grid
    return output_grid
```
