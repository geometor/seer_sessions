## Perception

The input is a 5x5 grid containing mostly zeros (0). Each input grid contains exactly one cell with the value '1' and exactly one cell with the value '2'. The output grid is derived from the input grid based on the relative positions of the '1' and '2'. In some cases, the output grid is identical to the input grid. In other cases, the cell containing '2' in the input is changed to '1' in the output, and the cell containing '1' in the input is changed to '0' in the output. The transformation rule appears to depend on whether the '1' and '2' cells are diagonally adjacent.

## Facts


```yaml
objects:
  - name: grid
    type: 2D array (list of lists)
    properties:
      - dimensions: 5x5
      - cells: contain integer values (0, 1, or 2)
  - name: cell_1
    type: grid cell
    properties:
      - value: 1
      - position: (row_1, col_1)
  - name: cell_2
    type: grid cell
    properties:
      - value: 2
      - position: (row_2, col_2)
relationships:
  - type: spatial
    between: [cell_1, cell_2]
    property: adjacency
    details: Checked for diagonal adjacency specifically. Two cells (r1, c1) and (r2, c2) are diagonally adjacent if the absolute difference in their row indices is 1 AND the absolute difference in their column indices is 1 (i.e., abs(r1 - r2) == 1 and abs(c1 - c2) == 1).
actions:
  - name: transform_grid
    condition: cell_1 and cell_2 are diagonally adjacent
    steps:
      - Change the value of cell_2 from 2 to 1 in the output grid.
      - Change the value of cell_1 from 1 to 0 in the output grid.
      - Keep all other cell values the same as the input grid.
  - name: copy_grid
    condition: cell_1 and cell_2 are NOT diagonally adjacent
    steps:
      - Copy the input grid directly to the output grid without changes.
```


## Natural Language Program

1.  Identify the coordinates (row_1, col_1) of the cell containing the value '1' in the input grid.
2.  Identify the coordinates (row_2, col_2) of the cell containing the value '2' in the input grid.
3.  Check if the cell containing '1' is diagonally adjacent to the cell containing '2'. This condition is true if the absolute difference between their row indices is 1 *and* the absolute difference between their column indices is 1 (i.e., `abs(row_1 - row_2) == 1` and `abs(col_1 - col_2) == 1`).
4.  **If** the cells are diagonally adjacent:
    *   Create the output grid by copying the input grid.
    *   Change the value at (row_2, col_2) in the output grid to '1'.
    *   Change the value at (row_1, col_1) in the output grid to '0'.
5.  **Else (if** the cells are not diagonally adjacent):
    *   The output grid is an identical copy of the input grid.