
## train_1

**input:**
```
2 9 2
4 4 4
9 9 9
```


**output:**
```
0 0 0
5 5 5
5 5 5
```


## train_2

**input:**
```
7 3 3
6 6 6
3 7 7
```


**output:**
```
0 0 0
5 5 5
0 0 0
```


## train_3

**input:**
```
2 2 4
2 2 4
1 1 1
```


**output:**
```
0 0 0
0 0 0
5 5 5
```


## train_4

**input:**
```
4 4 4
2 3 2
2 3 3
```


**output:**
```
5 5 5
0 0 0
0 0 0
```

*   **Perception of Elements:**
    *   The input and output are both 3x3 grids containing single digits.
    *   The transformation appears to operate independently on each row of the input grid to produce the corresponding row in the output grid.
    *   Each output row consists of three identical digits, either all 0s or all 5s.
    *   The determining factor for whether an output row is all 0s or all 5s seems to be related to the uniformity of the digits within the corresponding input row.

*   **YAML Facts:**
    
```yaml
    task_description: Transform a 3x3 input grid of digits into a 3x3 output grid based on row properties.
    elements:
      - object: input_grid
        properties:
          - type: grid
          - dimensions: 3x3
          - cell_content: single digits (0-9)
      - object: output_grid
        properties:
          - type: grid
          - dimensions: 3x3
          - cell_content: single digits (0 or 5)
      - object: row
        properties:
          - location: within input_grid or output_grid
          - length: 3 cells
          - content: sequence of digits
    relationships:
      - type: mapping
        source: input_grid row
        target: output_grid row (at the same index)
    actions:
      - action: analyze_row_uniformity
        input: input_grid row
        condition: Check if all digits in the row are identical.
        output: boolean (true if identical, false otherwise)
      - action: generate_output_row
        input: boolean result from analyze_row_uniformity
        rule: If true, output row is [5, 5, 5]. If false, output row is [0, 0, 0].
      - action: construct_output_grid
        input: generated output rows for each input row
        process: Assemble the generated rows into the final 3x3 output grid.
    ```


*   **Natural Language Program:**
    1.  Iterate through each row of the input grid, from top to bottom.
    2.  For the current input row, examine all three digits within it.
    3.  Check if all three digits in the current input row are identical.
    4.  If all three digits are identical, create the corresponding output row consisting of three '5' digits (`5 5 5`).
    5.  If the three digits are not all identical, create the corresponding output row consisting of three '0' digits (`0 0 0`).
    6.  Assemble these generated output rows to form the final output grid.
