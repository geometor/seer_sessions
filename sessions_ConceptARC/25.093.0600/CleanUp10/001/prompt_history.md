
## train_1

**input:**
```
2 2 0 2 0 0
0 0 2 2 2 0
2 2 2 2 2 2
2 2 0 2 0 2
2 0 0 2 2 0
0 0 0 2 0 0
```


**output:**
```
0 0 0 2 0 0
0 0 0 2 0 0
2 2 2 2 2 2
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


## train_2

**input:**
```
0 0 2 0 2 0
0 2 0 0 2 0
0 0 2 2 2 2
2 2 0 0 2 2
2 2 2 2 2 2
0 2 0 0 2 0
```


**output:**
```
0 0 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
2 2 2 2 2 2
0 0 0 0 2 0
```

## Perception

The input and output are grids of the same dimensions (6x6 in the examples) containing numerical values (0 and 2). The transformation appears to identify specific structural features in the input grid (a row composed entirely of '2's and a column with the highest density of '2's) and uses these features to construct the output grid. The output grid seems to be a simplified representation highlighting these identified features against a background of '0's.

1.  **Identify Constant Feature:** There is always one row in the input grid that consists entirely of the digit '2'. This row is preserved exactly in the same position in the output grid.
2.  **Identify Dominant Feature:** There is one column in the input grid that contains the maximum number of '2's compared to other columns.
3.  **Construct Output:** The output grid is initially composed entirely of '0's. Then, the identified constant row (all '2's) from the input is copied over. Finally, the column corresponding to the identified dominant column index is filled entirely with '2's.

## Facts


```yaml
objects:
  - name: grid
    properties:
      - rows: integer (number of rows)
      - columns: integer (number of columns)
      - cells: list of lists containing numerical values (0 or 2)
  - name: row
    properties:
      - index: integer
      - values: list of numerical values
      - is_solid: boolean (true if all values are 2)
  - name: column
    properties:
      - index: integer
      - values: list of numerical values
      - count_of_twos: integer
      - is_dense: boolean (true if it has the maximum count_of_twos among all columns)

relationships:
  - type: containment
    from: grid
    to: row
  - type: containment
    from: grid
    to: column
  - type: correspondence
    description: Output grid has the same dimensions as the input grid.
  - type: preservation
    description: The solid row from the input grid appears identically in the output grid at the same row index.
  - type: projection
    description: The column index identified as dense in the input grid corresponds to a column filled entirely with 2s in the output grid.

actions:
  - name: find_solid_row
    input: input_grid
    output: index of the row where all cell values are 2
  - name: find_dense_column
    input: input_grid
    output: index of the column with the maximum count of cells with value 2
  - name: initialize_output_grid
    input: dimensions (rows, columns)
    output: grid filled with 0s
  - name: copy_row
    input: source_grid, target_grid, row_index
    action: Copies the row at row_index from source_grid to target_grid.
  - name: fill_column
    input: target_grid, column_index, value (2)
    action: Sets all cells in the specified column of target_grid to the given value.
```


## Natural Language Program

1.  Create a new output grid with the same dimensions as the input grid, initializing all its cells to 0.
2.  Scan the input grid row by row to locate the row that consists entirely of the value 2. Record the index of this row (`solid_row_index`).
3.  Scan the input grid column by column, counting the occurrences of the value 2 in each column. Identify the index of the column that has the highest count of 2s. Record this index (`dense_column_index`). If multiple columns have the same maximum count, select the one with the smallest column index.
4.  Copy the contents of the row at `solid_row_index` from the input grid to the row at `solid_row_index` in the output grid.
5.  Set all the cells in the column at `dense_column_index` in the output grid to the value 2.
6.  Return the modified output grid.
