
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
5 5 5 5 5
5 0 5 0 5
5 5 5 5 5
5 0 5 0 5
5 5 5 5 5
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 7 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
5 5 5 5 5
5 0 5 0 5
5 5 5 5 5
5 0 5 0 5
5 5 5 5 5
```


## train_3

**input:**
```
6 0 0 0 6
6 0 0 0 6
0 6 0 6 0
0 6 0 6 0
0 0 6 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 5 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
7 7 7 7 7
7 0 7 0 7
7 7 7 7 7
7 0 7 0 7
7 7 7 7 7
```


**output:**
```
5 0 0 0 5
5 0 0 0 5
0 5 0 5 0
0 5 0 5 0
0 0 5 0 0
```


## train_5

**input:**
```
3 0 0 0 3
3 0 0 0 3
0 3 0 3 0
0 3 0 3 0
0 0 3 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 5 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_6

**input:**
```
1 1 1 1 1
1 0 1 0 1
1 1 1 1 1
1 0 1 0 1
1 1 1 1 1
```


**output:**
```
5 0 0 0 5
5 0 0 0 5
0 5 0 5 0
0 5 0 5 0
0 0 5 0 0
```

*   **Perception of Task Elements:**
    *   The task involves transforming a 5x5 input grid of integers into a 5x5 output grid of integers.
    *   The transformation rule does not depend on the specific non-zero values in the input, only on their presence (non-zero) and their spatial arrangement (shape/pattern).
    *   There appear to be three distinct input conditions leading to three distinct output grids.
    *   The output grids consist solely of the values 0 and 5.
    *   The input grids contain various integer values, but the value 0 seems to represent an "empty" or "background" cell, while any non-zero value represents an "active" or "foreground" cell.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    grid_size: [5, 5]
    input_elements:
      - type: grid
        description: 5x5 grid containing integer values. 0 represents background, non-zero values represent foreground shapes.
    output_elements:
      - type: grid
        description: 5x5 grid containing integer values 0 and 5, representing predefined patterns.
    patterns:
      - name: single_center_point
        description: Input grid contains exactly one non-zero cell, located anywhere. (Seen in train_1, train_2 inputs, though centered there).
        triggers_output: pattern_A
      - name: pattern_C_shape
        description: Input grid's non-zero cells form a specific shape (seen in train_3, train_5 inputs).
        coordinates_non_zero: [[0,0], [0,4], [1,0], [1,4], [2,1], [2,3], [3,1], [3,3], [4,2]] # Example coordinates for this shape
        triggers_output: pattern_D
      - name: pattern_A_shape
        description: Input grid's non-zero cells form the shape of pattern_A (seen in train_4, train_6 inputs).
        coordinates_non_zero: [[0,0],[0,1],[0,2],[0,3],[0,4], [1,0],[1,2],[1,4], [2,0],[2,1],[2,2],[2,3],[2,4], [3,0],[3,2],[3,4], [4,0],[4,1],[4,2],[4,3],[4,4]] # Coordinates for this shape
        triggers_output: pattern_B
    output_patterns:
      - name: pattern_A
        grid:
          - [5, 5, 5, 5, 5]
          - [5, 0, 5, 0, 5]
          - [5, 5, 5, 5, 5]
          - [5, 0, 5, 0, 5]
          - [5, 5, 5, 5, 5]
        description: Output grid associated with the single_center_point input condition.
      - name: pattern_B
        grid:
          - [5, 0, 0, 0, 5]
          - [5, 0, 0, 0, 5]
          - [0, 5, 0, 5, 0]
          - [0, 5, 0, 5, 0]
          - [0, 0, 5, 0, 0]
        description: Output grid associated with the pattern_A_shape input condition.
      - name: pattern_D
        grid:
          - [0, 0, 0, 0, 0]
          - [0, 0, 0, 0, 0]
          - [0, 0, 5, 0, 0]
          - [0, 0, 0, 0, 0]
          - [0, 0, 0, 0, 0]
        description: Output grid associated with the pattern_C_shape input condition.
    relationships:
      - The spatial pattern formed by non-zero cells in the input determines which fixed output grid is produced.
      - The specific non-zero values in the input are irrelevant to the transformation logic, only their positions matter.
    ```


*   **Natural Language Program:**
    1.  Identify all cells in the input grid that contain a non-zero value. Record their coordinates.
    2.  Count the number of non-zero cells.
    3.  **Condition 1:** If the count of non-zero cells is exactly 1, produce the predefined output grid `pattern_A`.
    4.  **Condition 2:** If the count is greater than 1, compare the set of coordinates of the non-zero cells to the predefined coordinate set defining `pattern_C_shape`. If they match exactly, produce the predefined output grid `pattern_D`.
    5.  **Condition 3:** If the count is greater than 1 and the coordinates do not match `pattern_C_shape`, compare the set of coordinates of the non-zero cells to the predefined coordinate set defining `pattern_A_shape`. If they match exactly, produce the predefined output grid `pattern_B`.
    6.  (Implicitly, if none of the above conditions are met, the behavior is undefined by the examples, but likely results in an error or a default output - though all examples fit one of these conditions).
