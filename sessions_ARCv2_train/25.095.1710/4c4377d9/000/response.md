*   **Perception:** The task involves transforming a grid of numbers (input) into a larger grid of numbers (output). The input grids consistently have 3 rows and 4 columns. The output grids consistently have 6 rows and 4 columns, exactly double the height of the input. The numbers present in the output grid are the same as those in the input grid for each corresponding example. The structure of the output grid appears to be derived from stacking the rows of the input grid in a specific order. Specifically, the first half of the output grid (top 3 rows) consists of the input grid's rows in reverse order (bottom row first, top row last). The second half of the output grid (bottom 3 rows) consists of the input grid's rows in their original order (top row first, bottom row last).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    input:
      type: grid
      properties:
        data_type: integers
        rows: 3
        columns: 4
      objects:
        - rows: list of sequences (e.g., lists) of integers
    output:
      type: grid
      properties:
        data_type: integers
        rows: 6 # 2 * input rows
        columns: 4 # same as input columns
      objects:
        - rows: list of sequences (e.g., lists) of integers
    transformation:
      actions:
        - action: reverse_order
          target: input_rows
          result: reversed_input_rows
        - action: concatenate
          operands:
            - reversed_input_rows
            - original_input_rows
          axis: vertical (rows)
          result: output_rows
      relationship:
        - The first N rows of the output grid are the N rows of the input grid in reverse vertical order.
        - The next N rows of the output grid are the N rows of the input grid in the original vertical order.
        (where N is the number of rows in the input grid)
    ```


*   **Natural Language Program:**
    1.  Take the input grid.
    2.  Create a list of the rows from the input grid.
    3.  Create a new list containing the rows from the input grid in reverse order (last row becomes first, first row becomes last).
    4.  Concatenate the reversed list of rows with the original list of rows vertically.
    5.  The resulting combined list of rows forms the output grid.