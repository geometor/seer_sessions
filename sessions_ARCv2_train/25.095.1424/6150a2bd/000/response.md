## Perception

The input and output are both structured as 3x3 grids containing single-digit integers. The core transformation appears to be a spatial rearrangement of the elements within the grid. Specifically, the output grid seems to be a 180-degree rotation of the input grid.

## Facts


```yaml
task_elements:
  - object: input_grid
    type: 2D array (3x3)
    element_type: integer
    properties: contains numbers from the input string, arranged spatially
  - object: output_grid
    type: 2D array (3x3)
    element_type: integer
    properties: contains numbers derived from the input grid, arranged spatially
relationship:
  - type: spatial_transformation
    action: rotate_180_degrees
    source: input_grid
    destination: output_grid
    details: |
      The element at input_grid[row][col] is moved to output_grid[2-row][2-col].
      For example:
      - input_grid[0][0] moves to output_grid[2][2]
      - input_grid[0][1] moves to output_grid[2][1]
      - input_grid[1][1] moves to output_grid[1][1]
      - input_grid[2][2] moves to output_grid[0][0]
```


## Natural Language Program

1.  Read the input as a 3x3 grid of integers.
2.  Create a new empty 3x3 grid for the output.
3.  Iterate through each cell of the input grid using its row index (`r`) and column index (`c`).
4.  For each input cell `input[r][c]`, place its value into the output grid at the position `output[2-r][2-c]`.
5.  Return the completed output grid.