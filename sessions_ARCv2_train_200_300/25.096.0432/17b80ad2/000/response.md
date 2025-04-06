*   **Perception**: The task involves transforming a 2D grid of integers. The transformation appears to operate independently on each column. Within each column, non-zero numbers seem to "fall downwards", filling the zero cells below them until another non-zero number is encountered in the same column. The original non-zero numbers remain in their positions, but also propagate their value downwards into subsequent zero cells.

*   **YAML Facts**:
    
```yaml
    task: grid_transformation
    input_type: grid
      element_type: integer
      range: 0-9
      background_value: 0
    output_type: grid
      element_type: integer
      range: 0-9
    transformation: column_based_fill_down
    elements:
      - object: grid
        properties:
          - rows: integer
          - columns: integer
          - cells: list_of_lists
      - object: column
        properties:
          - index: integer
          - cells: list
      - object: cell
        properties:
          - row_index: integer
          - column_index: integer
          - value: integer (0-9)
    actions:
      - name: process_columns
        details: Iterate through each column of the input grid independently.
      - name: fill_down
        details: Within a column, iterate from top to bottom. Keep track of the most recent non-zero value encountered. Replace any zero cell with this tracked value. If a new non-zero value is encountered, update the tracked value.
    relationships:
      - The output grid has the same dimensions as the input grid.
      - The value of a cell in the output grid depends on the values of the cells in the same column at or above its row index in the input grid.
      - Zero cells in the output grid correspond to zero cells in the input grid that are above the first non-zero cell in their respective column.
      - Non-zero cells in the output grid either correspond to non-zero cells in the input grid or are zero cells in the input grid that have been filled by a non-zero value from above in the same column.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each column index `c` from 0 to the number of columns minus 1.
    3.  Initialize a variable `fill_value` to 0. This variable will store the last non-zero number encountered in the current column.
    4.  Iterate through each row index `r` from 0 to the number of rows minus 1 for the current column `c`.
    5.  Read the value of the cell at `(r, c)` in the *input* grid. Let this be `current_value`.
    6.  If `current_value` is not 0:
        *   Update `fill_value` to `current_value`.
    7.  Else (if `current_value` is 0):
        *   If `fill_value` is not 0:
            *   Set the value of the cell at `(r, c)` in the *output* grid to `fill_value`.
    8.  After processing all columns, return the modified output grid.