
## train_1

**input:**
```
5 0 0
0 5 0
5 0 0
```


**output:**
```
2 2 2
4 4 4
2 2 2
```


## train_2

**input:**
```
0 0 5
0 0 5
0 0 5
```


**output:**
```
3 3 3
3 3 3
3 3 3
```


## train_3

**input:**
```
0 5 0
0 0 5
0 5 0
```


**output:**
```
4 4 4
3 3 3
4 4 4
```


## train_4

**input:**
```
0 0 5
0 5 0
5 0 0
```


**output:**
```
3 3 3
4 4 4
2 2 2
```

**Perception of Task Elements:**

1.  **Input/Output Structure:** The task takes a 3x3 grid of integers as input and produces a 3x3 grid of integers as output.
2.  **Input Content:** Each row in the input grid contains exactly one non-zero integer, which is always 5. The other two integers in the row are 0.
3.  **Output Content:** Each row in the output grid consists of three identical integers. The value of this integer varies between rows.
4.  **Transformation:** The transformation appears to operate independently on each row of the input grid to produce the corresponding row in the output grid.
5.  **Key Relationship:** The value used to fill the output row seems to be determined solely by the *column index* (position) of the number 5 within the corresponding input row.
6.  **Mapping Rule:**
    *   If the 5 is in the first column (index 0) of the input row, the output row is filled with 2s.
    *   If the 5 is in the second column (index 1) of the input row, the output row is filled with 4s.
    *   If the 5 is in the third column (index 2) of the input row, the output row is filled with 3s.

**YAML Documentation of Facts:**


```yaml
task_description: Maps the position of a unique non-zero element in each input row to a specific uniform value for the corresponding output row.

input_grid:
  type: object
  properties:
    format: 3x3 grid of integers
    cell_values: [0, 5]
    row_constraint: Each row contains exactly one '5' and two '0's.

output_grid:
  type: object
  properties:
    format: 3x3 grid of integers
    cell_values: [2, 3, 4]
    row_constraint: Each row contains three identical integers.

transformation:
  scope: row-wise
  rule: The value filling an output row depends on the column index of the '5' in the corresponding input row.
  mapping:
    input_row_pattern: [5, 0, 0] # '5' at index 0
    output_row_value: 2
  mapping:
    input_row_pattern: [0, 5, 0] # '5' at index 1
    output_row_value: 4
  mapping:
    input_row_pattern: [0, 0, 5] # '5' at index 2
    output_row_value: 3

relationships:
  - The output grid dimensions match the input grid dimensions.
  - Each output row is derived independently from its corresponding input row.
  - The column index of the '5' in an input row determines the uniform value of the corresponding output row.
```


**Natural Language Program:**

1.  Initialize an empty 3x3 output grid.
2.  Iterate through each row of the input grid, from row index 0 to 2.
3.  For the current input row:
    a.  Find the column index where the value is 5.
    b.  Determine the output value based on this index:
        i.  If the index is 0, the output value is 2.
        ii. If the index is 1, the output value is 4.
        iii.If the index is 2, the output value is 3.
    c.  Fill the corresponding row in the output grid with three instances of the determined output value.
4.  Return the completed output grid.
