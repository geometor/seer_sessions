## Perception

The task involves transforming a 1-dimensional grid (represented as a single row).
Each input grid contains a single contiguous block of a non-white color, surrounded by white pixels (color 0).
The transformation consists of shifting this colored block two positions to the right within the grid.
The size and color of the block remain unchanged.
The background remains white.
All example grids have a width of 18.

## Facts


```yaml
task_type: object_transformation
grid_dimensions:
  input: [1, 18] # Observed in examples
  output: [1, 18] # Same as input
background_color: 0 # white
objects:
  - object_type: contiguous_block
    properties:
      color: non-white (e.g., 2 (red), 6 (magenta))
      shape: horizontal_line
      count: 1 # Only one such block per input grid
transformation:
  action: shift
  direction: right
  distance: 2 # Pixels
relationship:
  - The colored block is embedded within a white background.
  - The position of the block changes, but its color and size are preserved.
  - The output grid maintains the original dimensions and background color.
```


## Natural Language Program

1.  Identify the single contiguous block of non-white pixels within the input grid.
2.  Determine the starting and ending coordinates of this block.
3.  Create a new output grid of the same dimensions as the input grid, initially filled with the background color (white, 0).
4.  Place the identified colored block into the output grid, shifted two positions to the right from its original starting position.