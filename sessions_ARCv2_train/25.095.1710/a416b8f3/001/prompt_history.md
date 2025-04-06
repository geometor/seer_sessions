
## train_1

**input:**
```
3 0 0
2 3 0
2 1 8
0 1 0
```


**output:**
```
3 0 0 3 0 0
2 3 0 2 3 0
2 1 8 2 1 8
0 1 0 0 1 0
```


## train_2

**input:**
```
0 5 0
5 5 2
0 0 0
```


**output:**
```
0 5 0 0 5 0
5 5 2 5 5 2
0 0 0 0 0 0
```


## train_3

**input:**
```
5 2 3 0
2 5 3 0
5 2 8 8
0 0 6 0
```


**output:**
```
5 2 3 0 5 2 3 0
2 5 3 0 2 5 3 0
5 2 8 8 5 2 8 8
0 0 6 0 0 0 6 0
```

**Perception:**

The input and output are both grids of single-digit numbers. The number of rows remains the same between the input and output. The number of columns in the output grid is exactly double the number of columns in the input grid. Observing the relationship between input and output rows reveals a simple pattern: each row in the output is formed by taking the corresponding row from the input and concatenating it with itself.

**YAML Facts:**


```yaml
Task: ConcatenateRows
Objects:
  - InputGrid:
      Type: 2D array of integers
      Properties:
        - Rows: variable number
        - Columns: variable number
        - Cells: contain single digits (0-9)
  - OutputGrid:
      Type: 2D array of integers
      Properties:
        - Rows: same as InputGrid
        - Columns: double the columns of InputGrid
        - Cells: contain single digits (0-9)
  - Row:
      Type: 1D array of integers
      Properties:
        - Elements: sequence of integers from a grid row
Relationships:
  - Each OutputGrid Row corresponds to exactly one InputGrid Row at the same row index.
Action:
  - Name: Concatenate Row with Itself
  - Input: A single Row from the InputGrid
  - Output: A new Row formed by appending the Input Row to itself.
Transformation:
  - For each Row in the InputGrid:
      - Perform the "Concatenate Row with Itself" action.
      - Place the resulting concatenated Row into the corresponding row index of the OutputGrid.
```


**Natural Language Program:**

1.  For each row in the input grid:
2.  Create a new row by taking the current input row.
3.  Append a copy of the current input row to the end of the new row.
4.  Place this new, concatenated row into the corresponding row position in the output grid.
