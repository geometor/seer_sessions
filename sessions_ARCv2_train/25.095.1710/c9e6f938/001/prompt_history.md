
## train_1

**input:**
```
0 0 0
0 7 7
0 0 0
```


**output:**
```
0 0 0 0 0 0
0 7 7 7 7 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 7 0
0 0 7
0 7 7
```


**output:**
```
0 7 0 0 7 0
0 0 7 7 0 0
0 7 7 7 7 0
```


## train_3

**input:**
```
0 0 0
7 0 0
0 0 0
```


**output:**
```
0 0 0 0 0 0
7 0 0 0 0 7
0 0 0 0 0 0
```

**Perception:**

The input is a 2D grid of numbers (specifically 3x3 in the examples provided). The output is also a 2D grid of numbers, but wider than the input (3x6 in the examples). Comparing the input and output grids reveals a consistent spatial transformation. The left half of the output grid is identical to the input grid. The right half of the output grid appears to be a mirror image (horizontal flip) of the input grid.

**Facts:**


```yaml
objects:
  - name: input_grid
    type: 2D grid
    properties:
      - rows: 3
      - columns: 3
      - cells: contain integer values (0 or 7 in examples)
  - name: output_grid
    type: 2D grid
    properties:
      - rows: 3 (same as input)
      - columns: 6 (twice the input columns)
      - cells: contain integer values
actions:
  - name: horizontal_flip
    input: input_grid
    output: a new grid which is the horizontal mirror image of the input_grid
  - name: concatenate_horizontally
    input: [grid1, grid2]
    output: a new grid formed by placing grid2 to the right of grid1
relationships:
  - type: transformation
    description: The output_grid is generated from the input_grid.
  - type: composition
    description: The output_grid is composed of two parts horizontally.
    parts:
      - part: left_half
        source: input_grid (identical copy)
      - part: right_half
        source: result of applying horizontal_flip to input_grid
  - type: generation_process
    steps:
      - step: 1
        action: horizontal_flip
        target: input_grid
        result: flipped_grid
      - step: 2
        action: concatenate_horizontally
        arguments: [input_grid, flipped_grid]
        result: output_grid

```


**Natural Language Program:**

1.  Take the input grid.
2.  Create a horizontally flipped version of the input grid (mirror image across the vertical axis).
3.  Concatenate the original input grid and the horizontally flipped grid side-by-side, with the original grid on the left and the flipped grid on the right.
4.  The resulting concatenated grid is the output grid.
