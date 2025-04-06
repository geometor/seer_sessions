
## train_1

**input:**
```
0 2 3 0 0
3 3 2 3 0
2 0 3 0 3
0 0 3 2 3
0 2 0 0 2
```


**output:**
```
0 2 3 0 0
3 3 0 3 0
2 0 3 0 3
0 0 3 2 3
0 2 0 0 2
```


## train_2

**input:**
```
0 4 5 0 0
5 5 4 4 5
4 4 4 5 5
4 5 4 5 4
4 4 4 5 5
```


**output:**
```
0 4 5 0 0
5 5 4 4 5
4 4 4 5 5
4 0 4 5 4
4 4 4 5 5
```


## train_3

**input:**
```
8 8 8 2 2
8 2 8 8 2
8 8 8 2 2
8 2 8 8 2
8 8 2 8 2
```


**output:**
```
8 8 8 2 2
8 0 8 8 2
8 8 8 2 2
8 0 8 8 2
8 8 2 8 2
```


## train_4

**input:**
```
0 3 3 3 8
3 8 3 3 8
3 8 3 3 8
3 8 3 3 8
3 3 3 3 3
```


**output:**
```
0 3 3 3 8
3 0 3 3 8
3 0 3 3 8
3 0 3 3 8
3 3 3 3 3
```

*   **Perception of the elements:**
    *   The inputs and outputs are 5x5 grids containing single-digit integers.
    *   The transformation modifies specific cells within the grid, changing their value to 0.
    *   The changes only occur in columns 1, 2, and 3 (0-indexed), never in the first or last column.
    *   The modification of a cell seems dependent on the values of its immediate horizontal neighbors (left and right).
    *   In all examples, a cell's value is changed to 0 if, and only if, its left neighbor and right neighbor have the exact same non-zero value.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: grid
        properties:
          - type: 2D array
          - dimensions: 5x5
          - content: single-digit integers (0-9)
      - object: cell
        properties:
          - value: integer (0-9)
          - position: row_index, column_index
        relationships:
          - type: horizontal_adjacency
            to: cell
            properties:
              - direction: left (column_index - 1)
              - direction: right (column_index + 1)
    actions:
      - name: modify_cell_value
        target: cell
        condition:
          - property: target cell's left neighbor's value
            equals: target cell's right neighbor's value
          - property: target cell's left neighbor's value
            is_not: 0
        effect:
          - set target cell's value to 0
    constraints:
      - The modification check only applies to cells in columns 1 through 3 (inclusive, 0-indexed). Cells in columns 0 and 4 are never modified.
      - The input grid is the starting state, and the output grid is the state after applying the modification rule to all eligible cells simultaneously (or iteratively without affecting subsequent checks in the same pass).
    ```


*   **Natural Language Program:**
    1.  Iterate through each cell in the input grid, focusing on cells located in columns 1, 2, and 3 (from the second column to the second-to-last column).
    2.  For each selected cell at position (row, column):
        a.  Identify the value of the cell immediately to its left, `left_neighbor_value` (at position (row, column-1)).
        b.  Identify the value of the cell immediately to its right, `right_neighbor_value` (at position (row, column+1)).
        c.  Check if `left_neighbor_value` is equal to `right_neighbor_value`.
        d.  Check if `left_neighbor_value` (and therefore `right_neighbor_value`) is not equal to 0.
        e.  If both conditions (c and d) are true, change the value of the current cell (at position (row, column)) to 0 in the output grid.
    3.  If the conditions are not met, or if the cell is in the first or last column, copy the cell's original value from the input grid to the output grid.
    4.  The final output grid contains the results of these checks and modifications for all cells.
