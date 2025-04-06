
## train_1

**input:**
```
3 5 1
4 5 8
2 4 9
```


**output:**
```
3 8 1
4 8 5
2 4 9
```


## train_2

**input:**
```
2 7 8 8 8
5 5 6 5 4
8 5 5 5 2
8 8 4 3 6
6 5 1 9 3
```


**output:**
```
2 7 5 5 5
8 8 6 8 4
5 8 8 8 2
5 5 4 3 6
6 8 1 9 3
```


## train_3

**input:**
```
6 5 3
5 7 5
8 8 2
```


**output:**
```
6 8 3
8 7 8
5 5 2
```

*   **Perception of Task Elements**:
    *   The input and output are grids (matrices) containing single-digit integers.
    *   The dimensions of the input grid match the dimensions of the output grid in each example.
    *   Comparing input and output grids reveals that most numbers remain in the same position.
    *   The core transformation involves specific numbers changing their values. In all examples, the numbers 5 and 8 are consistently interchanged. Where a 5 exists in the input, an 8 appears in the output, and where an 8 exists in the input, a 5 appears in the output. All other numbers remain unchanged.

*   **YAML Facts**:
    
```yaml
    task_elements:
      - object: Grid
        description: A 2D array of single-digit integers.
        properties:
          - rows: integer
          - columns: integer
      - object: Cell
        description: An individual element within the Grid.
        properties:
          - value: integer (0-9)
          - position: [row_index, column_index]
      - object: Number
        description: The integer value within a cell.
        properties:
          - identity: The specific integer (e.g., 5, 8).
    transformation:
      action: Swap Values
      description: Specific numeric values are systematically exchanged.
      target_values:
        - value_1: 5
        - value_2: 8
      rule: If a cell contains value_1, replace it with value_2. If a cell contains value_2, replace it with value_1.
      scope: Applies globally to all cells within the grid.
      unchanged_values: All integer values other than 5 and 8 remain unchanged in their respective positions.
    ```


*   **Natural Language Program**:
    1.  Iterate through each cell of the input grid.
    2.  For the current cell, read its integer value.
    3.  If the value is equal to 5, change the value of that cell to 8 in the output grid.
    4.  If the value is equal to 8, change the value of that cell to 5 in the output grid.
    5.  If the value is neither 5 nor 8, keep the original value in that cell in the output grid.
    6.  Continue this process until all cells have been processed. The resulting grid is the output.
