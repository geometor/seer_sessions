
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input and output are both 1-dimensional grids (rows). Each input grid contains a single contiguous horizontal block of a non-white color, surrounded by white pixels. The transformation involves shifting this colored block exactly one position to the right. The length of the colored block remains unchanged. This shift effectively makes the leftmost pixel of the original block white and colors the pixel immediately to the right of the original block with the block's color.

**Facts:**


```yaml
task_type: object_transformation
grid_dimensionality: 1D # Based on examples
background_color: white (0)
objects:
  - type: contiguous_block
    count: 1
    properties:
      color: non-white (varies per example: red, azure, magenta)
      shape: horizontal line segment
      location: variable start position within the grid
      size: variable length
relationships:
  - type: spatial
    description: The non-white block is surrounded by white pixels.
actions:
  - name: identify_object
    input: input_grid
    target: the single contiguous block of non-white color
    output: object_color, start_index, end_index
  - name: shift_object_right
    input: input_grid, object_color, start_index, end_index
    description: |-
      Create a copy of the input grid.
      Set the pixel at the start_index to white (0).
      If the index (end_index + 1) is within the grid bounds,
      set the pixel at (end_index + 1) to the object_color.
    output: output_grid
```


**Natural Language Program:**

1.  Identify the single contiguous horizontal block of non-white pixels in the input grid. Determine its color, its starting column index (`start`), and its ending column index (`end`).
2.  Create a new grid identical to the input grid.
3.  In the new grid, change the color of the pixel at index `start` to white (0).
4.  Check if the index `end + 1` is a valid column index within the grid's width.
5.  If `end + 1` is a valid index, change the color of the pixel at index `end + 1` in the new grid to the identified block's color.
6.  The resulting grid is the output.
