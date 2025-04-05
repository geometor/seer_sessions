
## train_1

**input:**
```
0 0 0 0 0
0 8 0 4 0
0 0 5 0 0
4 0 0 0 0
0 0 0 0 9
```


**output:**
```
4 8 5 4 9
4 8 5 4 9
4 8 5 4 9
4 8 5 4 9
4 8 5 4 9
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 8 6 0 0
1 0 0 0 0
0 0 0 6 9
```


**output:**
```
1 8 6 6 9
1 8 6 6 9
1 8 6 6 9
1 8 6 6 9
1 8 6 6 9
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
2 2 2 2 2
```


## train_4

**input:**
```
3 0 0 0 0
0 3 0 0 0
0 0 0 5 0
0 0 3 0 0
0 0 0 0 3
```


**output:**
```
3 3 3 5 3
3 3 3 5 3
3 3 3 5 3
3 3 3 5 3
3 3 3 5 3
```

*   **Perception of Task Elements:**
    *   The input is a 5x5 grid of integers, predominantly zeros, with some non-zero single digits scattered throughout.
    *   The output is also a 5x5 grid of integers.
    *   A key characteristic of the output grid is that all its rows are identical.
    *   The transformation involves analyzing the columns of the input grid to determine the single, repeated row of the output grid.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_grid
        properties:
          - type: grid
          - dimensions: 5x5
          - content: integers (0-9)
          - structure: contains mostly zeros and some non-zero digits
      - object: output_grid
        properties:
          - type: grid
          - dimensions: 5x5
          - content: integers (derived from input)
          - structure: all rows are identical
      - object: target_row
        properties:
          - type: sequence
          - length: 5
          - content: integers derived from input columns
          - relationship: forms each row of the output_grid
    actions:
      - name: identify_column_value
        actor: system
        input: column index (j), input_grid
        output: non-zero integer value
        description: Scan column j of the input_grid and identify the non-zero integer present in that column. Assumes only one distinct non-zero value exists per column across examples shown.
      - name: construct_target_row
        actor: system
        input: input_grid
        output: target_row
        description: Iterate through each column index (0 to 4) of the input_grid, apply identify_column_value for each, and assemble the results into the target_row.
      - name: construct_output_grid
        actor: system
        input: target_row
        output: output_grid
        description: Create a 5x5 grid where each row is a copy of the target_row.
    relationships:
      - type: determination
        from: non-zero value in input_grid column j
        to: value at index j in target_row
      - type: replication
        from: target_row
        to: each row in output_grid
    ```


*   **Natural Language Program:**
    1.  Determine the target row (a sequence of 5 integers) that will form the basis of the output grid.
    2.  For each column index `j` (from 0 to 4):
        a.  Scan the column `j` of the input grid.
        b.  Find the non-zero integer value present within that column. (Ignore the zeros. Based on the examples, it's assumed that if non-zero values exist in a column, they are all the same digit, or there is only one non-zero digit).
        c.  Assign this non-zero value as the element at index `j` in the target row.
    3.  Construct the 5x5 output grid by repeating the determined target row 5 times.
