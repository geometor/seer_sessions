
## train_1

**input:**
```
3 2 1 4
5 5 5 5
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```


**output:**
```
3 2 1 4
5 5 5 5
3 3 3 3
2 2 2 2
1 1 1 1
4 4 4 4
3 3 3 3
2 2 2 2
1 1 1 1
4 4 4 4
```


## train_2

**input:**
```
2 1 4
5 5 5
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```


**output:**
```
2 1 4
5 5 5
2 2 2
1 1 1
4 4 4
2 2 2
1 1 1
4 4 4
```


## train_3

**input:**
```
8 3
5 5
0 0
0 0
0 0
0 0
```


**output:**
```
8 3
5 5
8 8
3 3
8 8
3 3
```

**Perception of the Task Elements**

1.  **Input/Output Structure:** The inputs and outputs are grids (matrices) of single-digit integers. The dimensions (number of rows and columns) of the output grid are identical to the input grid for each example.
2.  **Row Copying:** The first two rows of the input grid are consistently copied verbatim to the first two rows of the output grid.
3.  **Source Sequence Identification:** The first row of the input grid serves as a source sequence of values.
4.  **Row Filling Pattern:** Starting from the third row (index 2) of the output grid, each row is populated based on the source sequence derived from the first input row.
5.  **Cyclical Filling:** The values from the source sequence are used one by one, cyclically, to fill entire rows in the output grid. The first value from the source sequence fills the third output row entirely, the second value fills the fourth output row, and so on. If the end of the source sequence is reached, it wraps around to the beginning.
6.  **Value Replication:** The selected value from the source sequence for a given output row is replicated across all columns of that row.
7.  **Input Ignored Data:** The content of the input grid from the third row onwards does not influence the output and appears to be ignored.

**YAML Facts**


```yaml
task_elements:
  - object: input_grid
    properties:
      - type: grid
      - content: integers
      - rows: variable (e.g., 10, 8, 6)
      - columns: variable (e.g., 4, 3, 2)
  - object: output_grid
    properties:
      - type: grid
      - content: integers
      - rows: same as input_grid
      - columns: same as input_grid
  - object: source_sequence
    properties:
      - derived_from: first row of input_grid
      - content: sequence of integers
      - length: equal to columns of input_grid
  - relationship: row_correspondence
    description: First two rows of output_grid are identical copies of the first two rows of input_grid.
  - action: fill_rows
    source: source_sequence
    target: output_grid rows starting from index 2
    details:
      - rule: cyclical pattern
      - index_mapping: Output row `i` (for `i >= 2`) uses element `(i - 2) % length(source_sequence)` from source_sequence.
      - value_application: The selected element fills all columns of the target output row.
  - observation: Input grid data from row index 2 onwards is not used in the transformation.
```


**Natural Language Program**

1.  Initialize the output grid with the same dimensions as the input grid.
2.  Copy the first row of the input grid to the first row of the output grid.
3.  Copy the second row of the input grid to the second row of the output grid.
4.  Identify the sequence of numbers in the first row of the input grid; let this be the `source_sequence`. Let the number of elements in this sequence (which is the number of columns) be `num_cols`.
5.  For each subsequent row index `i` in the output grid, starting from index 2 up to the total number of rows minus 1:
    a.  Determine the index `j` within the `source_sequence` to use for this row: `j = (i - 2) % num_cols`.
    b.  Retrieve the value `v` from the `source_sequence` at index `j`.
    c.  Fill the entire output grid row at index `i` with the value `v`, repeating it `num_cols` times.
6.  The resulting grid is the final output.
