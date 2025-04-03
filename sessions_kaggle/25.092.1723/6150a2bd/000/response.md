## Perception of Task Elements

The input and output are both represented as 3x3 grids containing single-digit integers. The transformation appears to be a spatial rearrangement of the elements within the grid. Comparing the positions of elements between the input and output suggests a specific type of rotation.

## Facts


```yaml
objects:
  - name: input_grid
    properties:
      type: grid
      dimensions: 3x3
      cell_content: integers
  - name: output_grid
    properties:
      type: grid
      dimensions: 3x3
      cell_content: integers
relationships:
  - type: transformation
    action: rotate_180_degrees
    input: input_grid
    output: output_grid
    description: The output grid is derived from the input grid by rotating it 180 degrees. Each element at position (row, col) in the input grid moves to position (2 - row, 2 - col) in the output grid (using 0-based indexing).
```


## Natural Language Program

1.  Read the input as a 3x3 grid of integers.
2.  Create a new 3x3 grid for the output, initially empty.
3.  Iterate through each cell of the input grid using its row index `r` and column index `c` (from 0 to 2).
4.  Place the integer value from the input grid cell at `(r, c)` into the output grid cell at position `(2 - r, 2 - c)`.
5.  The resulting grid is the output.