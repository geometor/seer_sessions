*   **Perception:** The input is a grid of integers. The output is always a 2x2 grid of integers. The specific 2x2 subgrid selected from the input depends on the dimensions of the input grid, specifically the number of columns. The output always consists of elements from the first two rows of the input grid. The starting column index for the 2x2 subgrid depends on whether the total number of columns in the input grid is even or odd.

*   **Facts:**
    
```yaml
    task_description: Extract a 2x2 subgrid from the top-left or top-right corner of an input grid based on the parity of the input grid's width.
    elements:
      - object: input_grid
        properties:
          - type: 2D array of integers
          - rows: variable number (R)
          - columns: variable number (N)
      - object: output_grid
        properties:
          - type: 2D array of integers
          - rows: 2
          - columns: 2
          - source: subgrid extracted from input_grid
    actions:
      - action: determine_grid_dimensions
        input: input_grid
        output: number of rows (R), number of columns (N)
      - action: determine_start_column
        input: number of columns (N)
        logic: >
          If N is even, start_column = N - 2.
          If N is odd, start_column = 0.
        output: start_column_index
      - action: extract_subgrid
        input:
          - input_grid
          - start_column_index
        logic: >
          Select elements from input_grid at rows 0 and 1,
          and columns start_column_index and start_column_index + 1.
        output: 2x2 output_grid
      - action: format_output
        input: output_grid
        logic: Format the 2x2 grid with space-separated integers per row and newline characters between rows.
        output: formatted string representation
    relationships:
      - relationship: dependency
        subject: output_grid
        verb: is derived from
        object: input_grid
      - relationship: conditional_logic
        subject: start_column_index
        verb: depends on
        object: parity of the number of columns (N) in input_grid
      - relationship: positional_extraction
        subject: output_grid
        description: Always uses the first two rows (index 0 and 1) of the input_grid.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a 2D grid of integers.
    2.  Determine the number of columns (`N`) in the input grid.
    3.  Calculate the starting column index (`start_col`) for the output subgrid:
        *   If `N` is even, set `start_col = N - 2`.
        *   If `N` is odd, set `start_col = 0`.
    4.  Extract the 2x2 subgrid from the input grid by taking the elements at:
        *   Row 0, Column `start_col`
        *   Row 0, Column `start_col + 1`
        *   Row 1, Column `start_col`
        *   Row 1, Column `start_col + 1`
    5.  Format this 2x2 subgrid into the output string, with space-separated integers on each row and rows separated by newlines.