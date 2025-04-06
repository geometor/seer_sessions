*   **Perception of Task Elements:**
    *   The input and output are 2D grids of integers.
    *   The transformation selectively keeps certain columns from the input grid while zeroing out others.
    *   The selection criteria appear to be based on the properties of the columns themselves, specifically the count of non-zero elements within each column.
    *   In cases where multiple columns share the maximum non-zero count, a tie-breaking rule seems to be applied (selecting the rightmost column).

*   **Facts (YAML):**
    
```yaml
    task_elements:
      - object: input_grid
        description: A 2D array of integers representing the initial state.
        properties:
          - dimensions (rows, columns)
          - cell_values (integers)
      - object: output_grid
        description: A 2D array of integers representing the final state.
        properties:
          - dimensions (same as input_grid)
          - cell_values (integers, mostly zeros)
      - object: column
        description: A vertical slice of the grid.
        properties:
          - index (position within the grid)
          - values (list of integers in the column)
          - non_zero_count (count of elements > 0)
      - object: cell
        description: An individual element within the grid.
        properties:
          - row_index
          - column_index
          - value (integer)

    transformation:
      action: analyze_columns
      description: Evaluate each column in the input_grid.
      input: input_grid
      process:
        - For each column, count the number of non-zero elements.
      output: A list of non-zero counts, one for each column index.

      action: find_target_column
      description: Determine which column(s) from the input should be preserved in the output.
      input: List of non-zero counts per column.
      process:
        - Find the maximum non-zero count among all columns.
        - Identify the indices of all columns that have this maximum count.
        - If multiple columns have the maximum count, select the one with the largest index (the rightmost one).
      output: The index of the single target column.

      action: construct_output
      description: Create the output grid based on the target column.
      input:
        - input_grid
        - target_column_index
      process:
        - Create a new grid with the same dimensions as the input_grid, filled with zeros.
        - Copy the elements from the target_column_index of the input_grid to the same column index in the new grid.
      output: output_grid

    relationships:
      - The output_grid structure is derived from the input_grid.
      - Only values from a specific column (the target_column) of the input_grid are present in the output_grid.
      - The selection of the target_column depends on maximizing the non_zero_count, with a rightmost tie-breaking rule.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a grid of zeros with the same dimensions as the input grid.
    2.  For each column in the input grid, count the number of non-zero elements it contains.
    3.  Determine the maximum non-zero count found across all columns.
    4.  Identify the index (or indices) of the column(s) that have this maximum non-zero count.
    5.  If there is only one such column, select its index. If there are multiple columns with the maximum count, select the index of the rightmost column among them (the one with the highest column index).
    6.  Copy all the values (including zeros) from the selected column in the input grid to the corresponding column in the output grid.
    7.  Return the final output grid.