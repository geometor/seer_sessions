**Perception of Task Elements:**

The task involves transforming a 2D grid of numbers. The input grids contain the numbers 0 and 8. The output grids have the same dimensions as the input grids and contain the numbers 0 and 2. The number 0 appears to represent the background or empty space, which remains unchanged in position. The number 8 seems to represent an object or a set of objects. In the output, these objects appear to have moved and changed their value to 2. Comparing the input and output grids across the examples reveals a consistent pattern: every cell containing an 8 in the input corresponds to a cell containing a 2 in the output, located exactly one row below the original position.

**YAML Facts:**


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2
  cell_values:
    input: [0, 8]
    output: [0, 2]
  size_relation: input and output grids have identical dimensions
objects:
  - id: background
    input_value: 0
    output_value: 0
    transformation: remains unchanged
  - id: primary_object
    input_value: 8
    output_value: 2
    transformation: spatial shift and value change
transformation_rules:
  - action: identify_cells
    value: 8
    target: input_grid
  - action: shift_position
    direction: down
    magnitude: 1 row
    input_value: 8
    output_value: 2
  - action: preserve_value
    value: 0
    target: input_grid
relationships:
  - type: spatial_mapping
    description: Each cell with value 8 at (row, col) in the input maps to a cell with value 2 at (row + 1, col) in the output.
  - type: value_mapping
    description: Input value 8 maps to output value 2. Input value 0 maps to output value 0.
constraints:
  - Cells shifted beyond the bottom boundary of the grid are discarded (implicitly, as they don't appear in the output examples).
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the background value (0).
2.  Iterate through each cell of the input grid, noting its row index (`r`) and column index (`c`).
3.  If the value of the input cell at (`r`, `c`) is 8:
    a.  Calculate the target row index in the output grid as `r + 1`.
    b.  If the target row index `r + 1` is within the vertical bounds of the grid:
        i.  Set the value of the output grid cell at (`r + 1`, `c`) to 2.
4.  Return the completed output grid.