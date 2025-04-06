
## train_1

**input:**
```
5 5 2
1 0 0
0 0 0
```


**output:**
```
0 0 0
0 0 1
2 5 5
```


## train_2

**input:**
```
3 3 8
3 7 0
5 0 0
```


**output:**
```
0 0 5
0 7 3
8 3 3
```

Okay, let's analyze the provided examples.

**Perception of Task Elements:**

*   **Input:** The input consists of a 3x3 grid of single-digit integers.
*   **Output:** The output is also a 3x3 grid of single-digit integers.
*   **Transformation:** The numbers present in the input grid are rearranged to form the output grid. The specific rearrangement appears consistent across both examples. Comparing the positions, it looks like the grid is rotated 180 degrees. For instance, the element at the top-left corner (row 0, col 0) moves to the bottom-right corner (row 2, col 2), the element at the top-right (row 0, col 2) moves to the bottom-left (row 2, col 0), and the central element (row 1, col 1) stays in place.

**YAML Fact Documentation:**


```yaml
Task: Grid Transformation

Input:
  Type: Grid
  Dimensions: 3x3
  Elements:
    Type: Integer
    Range: 0-9 (based on examples)

Output:
  Type: Grid
  Dimensions: 3x3
  Elements:
    Type: Integer
    Relationship_to_Input: Same set of integers as input, rearranged.

Transformation:
  Action: Rotation
  Degrees: 180
  Center: Center of the grid
  Description: Each element at position (row, col) in the input grid moves to position (2 - row, 2 - col) in the output grid.
```


**Natural Language Program:**

1.  Read the input 3x3 grid.
2.  Create a new empty 3x3 grid for the output.
3.  For each element in the input grid at position (row, column):
    *   Place that element into the output grid at position (2 - row, 2 - column).
4.  Return the completed output grid.
