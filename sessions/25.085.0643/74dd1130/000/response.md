## Perception

The input and output for each example are 3x3 grids containing various colors (represented by integers 0-9). The colors present in the input grid are the same as the colors present in the output grid, but their positions have changed. Comparing the input and output grids in each example, it appears that the output grid is a transformation of the input grid where rows have become columns and columns have become rows. This is consistent across all provided examples and is characteristic of a matrix transpose operation.

## Facts


```yaml
task_type: transformation
input_object:
  type: grid
  description: A 2D grid of pixels (colors).
  properties:
    height: 3
    width: 3
    colors: varies per example
output_object:
  type: grid
  description: A 2D grid of pixels (colors), resulting from the transformation.
  properties:
    height: 3
    width: 3
    colors: same set as input, rearranged
transformation:
  type: geometric
  operation: transpose
  description: The input grid is transposed to produce the output grid. The element at row `i`, column `j` in the input grid moves to row `j`, column `i` in the output grid.
```


## Natural Language Program

1.  Take the input grid.
2.  Create a new output grid with the same dimensions as the input grid, but swapped (width becomes height, height becomes width).
3.  For each pixel at position (row `r`, column `c`) in the input grid, place its value (color) into the output grid at position (row `c`, column `r`).
4.  Return the resulting output grid.