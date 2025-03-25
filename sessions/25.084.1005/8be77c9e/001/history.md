
## train_1

**input:**
```
0 0 0
1 0 1
1 1 0
```


**output:**
```
0 0 0
1 0 1
1 1 0
1 1 0
1 0 1
0 0 0
```


## train_2

**input:**
```
1 1 0
1 1 1
0 0 0
```


**output:**
```
1 1 0
1 1 1
0 0 0
0 0 0
1 1 1
1 1 0
```


## train_3

**input:**
```
0 0 0
0 0 1
0 0 1
```


**output:**
```
0 0 0
0 0 1
0 0 1
0 0 1
0 0 1
0 0 0
```

**Perception:**

The task involves transforming an input grid into an output grid. In all provided examples, the output grid has the same width as the input grid but is exactly twice the height. Observing the pixel patterns, the top half of the output grid is always identical to the input grid. The bottom half of the output grid is a vertical reflection (flipped upside down) of the input grid. The reflection appears to be mirrored across the horizontal line that would form the bottom edge of the input grid.

**Facts:**


```yaml
Input:
  - type: grid
    properties:
      - height: H
      - width: W
Output:
  - type: grid
    properties:
      - height: 2 * H
      - width: W
Transformation:
  - type: geometric
    action: reflect
    axis: horizontal
    location: across the bottom edge of the input grid
  - type: composition
    action: stack
    elements:
      - original_input_grid (top)
      - reflected_input_grid (bottom)
    orientation: vertical
Relationship:
  - The output grid consists of the original input grid placed directly above its own vertical reflection.
```


**Natural Language Program:**

1.  Identify the input grid.
2.  Create a vertically flipped (upside-down) version of the input grid.
3.  Construct the output grid by stacking the original input grid on top of the vertically flipped version. The resulting output grid will have the same width as the input and double the height.
