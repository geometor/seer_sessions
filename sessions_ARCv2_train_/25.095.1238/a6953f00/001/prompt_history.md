
## train_1

**input:**
```
7 5 8 2
8 0 4 7
1 6 4 7
8 9 6 9
```


**output:**
```
8 2
4 7
```


## train_2

**input:**
```
0 7 9
5 6 5
3 7 9
```


**output:**
```
0 7
5 6
```


## train_3

**input:**
```
5 8 8 9 2
8 0 5 6 5
7 7 2 2 9
5 5 1 7 4
3 3 8 7 7
```


**output:**
```
5 8
8 0
```

**Perception:**

The input is a square or rectangular grid of single-digit integers. The output is always a 2x2 grid of integers. The transformation involves selecting a specific 2x2 subgrid from the input grid. The location of the selected 2x2 subgrid appears to depend on the dimensions of the input grid. In two examples (3x3 and 5x5 inputs), the output is the top-left 2x2 subgrid. In the other example (4x4 input), the output is the top-right 2x2 subgrid. This suggests a conditional rule based on the input dimensions.

**Facts:**


```yaml
objects:
  - name: input_grid
    properties:
      - type: grid
      - element_type: integer
      - rows: variable (e.g., 3, 4, 5)
      - columns: variable (e.g., 3, 4, 5)
  - name: output_grid
    properties:
      - type: grid
      - element_type: integer
      - rows: 2
      - columns: 2
actions:
  - name: extract_subgrid
    parameters:
      - input_grid
      - top_row_index
      - left_col_index
      - height: 2
      - width: 2
    output: output_grid
relationships:
  - type: selection
    details: The output_grid is a 2x2 subgrid extracted from the input_grid.
  - type: conditional_location
    condition: input_grid dimensions are 4x4
    action: extract_subgrid with top_row_index=0, left_col_index=2 (top-right)
  - type: conditional_location
    condition: input_grid dimensions are not 4x4
    action: extract_subgrid with top_row_index=0, left_col_index=0 (top-left)

```


**Natural Language Program:**

1.  Examine the dimensions (number of rows and columns) of the input grid.
2.  If the input grid has 4 rows and 4 columns:
    a.  Select the 2x2 subgrid starting from row index 0 and column index 2 (the top-right 2x2 block).
3.  Otherwise (if the input grid does not have 4 rows and 4 columns):
    a.  Select the 2x2 subgrid starting from row index 0 and column index 0 (the top-left 2x2 block).
4.  Return the selected 2x2 subgrid as the output.
