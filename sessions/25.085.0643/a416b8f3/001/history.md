
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

## Perception

The task involves transforming an input grid into an output grid.
- The input grids have varying dimensions (4x3, 3x3, 4x4).
- The output grids consistently have the same height as their corresponding input grids but double the width.
- Visually comparing the input and output grids, the output grid appears to be composed of two identical copies of the input grid placed side-by-side horizontally.

## Facts


```yaml
task_name: mirror_horizontal
description: Duplicate the input grid horizontally to create the output grid.
elements:
  - object: input_grid
    type: grid
    properties:
      height: h
      width: w
  - object: output_grid
    type: grid
    properties:
      height: h
      width: 2 * w
relationship:
  - type: construction
    origin: input_grid
    target: output_grid
    details: The output grid is formed by concatenating the input grid with itself horizontally. The left half of the output grid is identical to the input grid, and the right half is also identical to the input grid.
action:
  - name: horizontal_concatenation
    input: input_grid
    output: output_grid
    details: Append a copy of the input_grid to the right side of the original input_grid.
```


## Natural Language Program

1.  Take the input grid.
2.  Create a new grid with the same height as the input grid and twice its width.
3.  Copy the input grid into the left half of the new grid (from column 0 to column width-1).
4.  Copy the input grid again into the right half of the new grid (from column width to column 2*width-1).
5.  The resulting grid is the output.
