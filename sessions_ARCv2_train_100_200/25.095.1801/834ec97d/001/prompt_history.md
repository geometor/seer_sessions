
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
4 0 4 0 4
4 0 4 0 4
4 0 4 0 4
0 0 6 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 2 0
0 0 0
0 0 0
```


**output:**
```
0 4 0
0 2 0
0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided task examples.

**Perception of Task Elements:**

1.  **Input Data:** Each input is a grid (matrix) of numbers. The grid contains mostly zeros (0) and a single non-zero number at a specific location. The size of the grid varies between examples.
2.  **Output Data:** Each output is also a grid of the same dimensions as the corresponding input. The output grid contains the original non-zero number, but shifted down one row. Additionally, a pattern involving the number four (4) appears in the rows above the original position of the non-zero number.
3.  **Transformation:** The core transformation involves two main actions:
    *   **Relocation:** The single non-zero number from the input grid is moved one position down (row index increases by 1) while keeping the same column index.
    *   **Pattern Generation:** Rows in the output grid, starting from the top (row 0) down to the original row of the non-zero number, are filled with a repeating horizontal pattern. This pattern consists of the number 4 and 0. The exact structure of this pattern seems related to the column index of the original non-zero number and the grid's width.
4.  **Key Observations:**
    *   The value of the non-zero number (6, 2, 9) is preserved in the output, just its location changes.
    *   The pattern always uses the number 4.
    *   The pattern fills all rows *above* the *original* location of the non-zero number, inclusive of the original row itself (rows 0 to `r`, where `r` is the original row index).
    *   The horizontal pattern (`4 0 4 0 4` or `0 4 0`) depends on the parity (even/odd) of the column index (`c`) where the original non-zero number was found. If `c` is even, the pattern places '4's at even column indices. If `c` is odd, the pattern places '4's at odd column indices.

**YAML Facts:**


```yaml
task_elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: height H, width W
      - content: contains mostly zeros and one non-zero integer N
    location:
      row: r
      column: c

  - object: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: height H, width W (same as input)
      - content: derived from input_grid

  - object: non_zero_number
    identifier: N
    properties:
      - value: integer > 0 (e.g., 6, 2, 9)
      - initial_position: (r, c) in input_grid
      - final_position: (r+1, c) in output_grid

  - object: pattern_element
    identifier: P
    properties:
      - value: 4
      - structure: horizontal row pattern (e.g., [4, 0, 4, 0, 4] or [0, 4, 0])
      - dependency: structure depends on the parity of the initial column 'c' of N
      - location: fills rows 0 to 'r' (inclusive) in the output_grid

actions:
  - name: locate_N
    input: input_grid
    output: value N, position (r, c), dimensions (H, W)

  - name: determine_pattern_row
    input: width W, column c
    output: pattern_row P (list of length W)
    logic: P[j] = 4 if j % 2 == c % 2, else P[j] = 0, for j in 0..W-1

  - name: construct_output
    input: H, W, N, r, c, pattern_row P
    output: output_grid
    steps:
      - create HxW grid filled with zeros
      - for i from 0 to r: set output_grid[i] = P
      - set output_grid[r+1][c] = N

relationships:
  - The output grid dimensions are identical to the input grid dimensions.
  - The position of N in the output grid is directly below its position in the input grid.
  - The number of rows filled with the pattern P in the output grid is r + 1.
  - The structure of the pattern row P depends on the parity of the column index c.
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Determine the grid's dimensions: height `H` and width `W`.
3.  Scan the input grid to find the single non-zero number `N` and its location (row `r`, column `c`).
4.  Create a new output grid of the same dimensions (`H`x`W`) and initialize all its cells to 0.
5.  Construct the "pattern row" `P`, which is a list of length `W`:
    a.  Initialize `P` with all zeros.
    b.  Determine the parity of the column `c` (is `c` even or odd?).
    c.  Iterate through the column indices `j` from 0 to `W-1`.
    d.  If the parity of `j` matches the parity of `c`, set the element `P[j]` to 4.
6.  Fill the rows of the output grid with the pattern:
    a.  Iterate through the row indices `i` from 0 to `r` (inclusive).
    b.  For each row `i`, copy the contents of the pattern row `P` into the `i`-th row of the output grid.
7.  Place the original non-zero number `N` in the output grid:
    a.  Set the cell at position (row `r+1`, column `c`) in the output grid to the value `N`.
8.  Return the completed output grid.
