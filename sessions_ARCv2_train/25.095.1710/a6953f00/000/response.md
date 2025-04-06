## Perception

The input consists of a grid of single-digit numbers represented as strings with space-separated values on each line. The output is always a 2x2 grid, also represented as space-separated strings. The core task is to extract a specific 2x2 subgrid from the input grid.

Observing the examples:
1.  **train_1:** Input is 4x4. Output is the top-right 2x2 subgrid (`[[8, 2], [4, 7]]`).
2.  **train_2:** Input is 3x3. Output is the top-left 2x2 subgrid (`[[0, 7], [5, 6]]`).
3.  **train_3:** Input is 5x5. Output is the top-left 2x2 subgrid (`[[5, 8], [8, 0]]`).

A pattern emerges based on the dimensions of the input grid. Specifically, the parity (evenness or oddness) of the number of rows seems to determine which 2x2 subgrid is extracted. If the number of rows is even (train_1), the top-right 2x2 subgrid is taken. If the number of rows is odd (train_2, train_3), the top-left 2x2 subgrid is taken.

## Facts


```yaml
objects:
  - name: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (N rows, M columns)
  - name: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: fixed (2 rows, 2 columns)

actions:
  - name: determine_dimensions
    actor: system
    input: input_grid
    output: number_of_rows (N), number_of_columns (M)
  - name: check_parity
    actor: system
    input: number_of_rows (N)
    output: is_even (boolean)
  - name: extract_subgrid
    actor: system
    input: input_grid, position (top-left or top-right)
    output: output_grid

relationships:
  - type: derivation
    from: input_grid
    to: output_grid
  - type: conditional_extraction
    condition: parity of number_of_rows in input_grid
    outcome_if_even: extract top-right 2x2 subgrid
    outcome_if_odd: extract top-left 2x2 subgrid
```


## Natural Language Program

1.  Read the input string and parse it into a 2D grid of integers.
2.  Calculate the number of rows (N) and the number of columns (M) of the input grid.
3.  Determine if the number of rows (N) is even or odd.
4.  If N is even:
    *   Select the subgrid consisting of the elements at row indices 0 and 1, and column indices M-2 and M-1.
5.  If N is odd:
    *   Select the subgrid consisting of the elements at row indices 0 and 1, and column indices 0 and 1.
6.  Format the selected 2x2 subgrid into the required output string format (space-separated values per row, newline between rows).