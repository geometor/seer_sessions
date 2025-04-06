
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

**Perception:**

The input and output are both structured as 3x3 grids containing single-digit integers. Observing the relationship between the input and output grids in both examples, it appears that the output grid is a transformation of the input grid. Specifically, the elements seem to be repositioned. Comparing the positions of the numbers, the transformation consistently matches a 180-degree rotation of the input grid. For instance, the element at the top-left corner of the input moves to the bottom-right corner of the output, the element at the top-right moves to the bottom-left, the center element stays in the center, and so on.

**Facts:**


```yaml
Task: Grid Transformation

Input:
  Type: Grid
  Dimensions: 3x3
  Elements: Single-digit integers

Output:
  Type: Grid
  Dimensions: 3x3
  Elements: Single-digit integers (same set as input)

Transformation:
  Action: Rotate
  Angle: 180 degrees
  Target: Input Grid

Relationship:
  - The output grid is the result of rotating the input grid by 180 degrees.
  - Each element at position (row, col) in the input grid moves to position (2-row, 2-col) in the output grid (using 0-based indexing).
```


**Natural Language Program:**

1.  Accept the input 3x3 grid.
2.  Rotate the input grid by 180 degrees.
3.  The resulting grid is the output.
