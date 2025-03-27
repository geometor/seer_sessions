
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

**Perception**
The input is a grid of pixels. The output is also a grid of pixels. In each example, the output grid appears to be constructed by taking the input grid and placing an identical copy of it immediately to the right. The height of the output grid is the same as the input grid, while the width of the output grid is exactly double the width of the input grid. The left half of the output grid is identical to the input grid, and the right half of the output grid is also identical to the input grid.

**Facts**

```yaml
task_context:
  - description: Grid duplication.
    input_grid_properties:
      - height: H
      - width: W
      - pixels: P_in
    output_grid_properties:
      - height: H
      - width: 2 * W
      - pixels: P_out
transformation:
  - type: concatenation
    direction: horizontal
    source_1: input_grid
    source_2: input_grid
    result: output_grid
relationship:
  - description: The output grid is formed by placing the input grid next to a copy of itself.
    output_left_half: identical to input_grid
    output_right_half: identical to input_grid
```


**Natural Language Program**
1.  Get the input grid.
2.  Concatenate the input grid with itself horizontally. The first instance of the input grid forms the left half of the new grid, and the second instance forms the right half.
3.  The resulting concatenated grid is the output grid.
