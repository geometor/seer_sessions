
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

The input and output are both 3x3 grids containing numerical digits. The transformation appears to rearrange the positions of the numbers within the grid. Comparing the input and output grids, the numbers themselves remain the same, but their locations change. The pattern suggests a spatial transformation, specifically a 180-degree rotation of the entire grid. The element originally at the top-left corner moves to the bottom-right, the element at the top-right moves to the bottom-left, the center element stays in place (though this isn't explicitly tested with a non-zero center element), and so on.

**YAML Facts:**


```yaml
task_elements:
  - object: grid
    properties:
      - type: 2D array
      - dimensions: 3x3
      - elements: numerical digits (0-9)
  - relationship: input_output
    description: The output grid is derived from the input grid through a transformation.
  - action: rotate
    actor: grid
    details:
      - type: 180 degrees
      - effect: Reverses the order of both rows and columns. The element at index (row, col) in the input moves to index (2-row, 2-col) in the output.
```


**Natural Language Program:**

1.  Take the 3x3 input grid.
2.  Rotate the grid by 180 degrees.
3.  The resulting grid is the output. This means the element at the top-left moves to the bottom-right, the element at the top-center moves to the bottom-center, the element at the top-right moves to the bottom-left, and similarly for the other rows.
