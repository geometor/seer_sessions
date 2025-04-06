## Perception

The input is a 4x4 grid of integers. The non-zero integers are concentrated within the central 2x2 subgrid (rows 1 and 2, columns 1 and 2, using 0-based indexing). The outer border of the input grid consists entirely of zeros.

The output is also a 4x4 grid of integers. The non-zero integers from the input's central 2x2 subgrid have been relocated to the four corners of the output grid. All other cells in the output grid are zeros.

The transformation involves extracting the four values from the central 2x2 subgrid of the input and mapping them to the corner positions of the output grid.

## Facts


```yaml
task_elements:
  - type: grid
    properties:
      size: 4x4
      dtype: integer
      role: input
  - type: grid
    properties:
      size: 4x4
      dtype: integer
      role: output
objects:
  - name: input_grid
    type: grid
    description: The source 4x4 grid containing numbers.
  - name: output_grid
    type: grid
    description: The target 4x4 grid, initially empty or zero-filled.
  - name: central_subgrid
    type: subgrid
    location: input_grid[1:3, 1:3] # rows 1-2, columns 1-2
    description: The 2x2 area within the input grid containing the non-zero values.
    elements:
      - name: top_left_value
        location: input_grid[1, 1]
      - name: top_right_value
        location: input_grid[1, 2]
      - name: bottom_left_value
        location: input_grid[2, 1]
      - name: bottom_right_value
        location: input_grid[2, 2]
  - name: output_corners
    type: set_of_cells
    location: output_grid corners
    description: The four corner cells of the output grid.
    elements:
      - name: top_left_corner
        location: output_grid[0, 0]
      - name: top_right_corner
        location: output_grid[0, 3]
      - name: bottom_left_corner
        location: output_grid[3, 0]
      - name: bottom_right_corner
        location: output_grid[3, 3]
actions:
  - name: initialize_output
    actor: system
    target: output_grid
    result: A 4x4 grid filled with zeros.
  - name: map_values_to_corners
    actor: system
    source: central_subgrid elements
    target: output_corners elements
    mapping:
      - from: top_left_value (input[1, 1])
        to: top_left_corner (output[0, 0])
      - from: top_right_value (input[1, 2])
        to: top_right_corner (output[0, 3])
      - from: bottom_left_value (input[2, 1])
        to: bottom_left_corner (output[3, 0])
      - from: bottom_right_value (input[2, 2])
        to: bottom_right_corner (output[3, 3])
relationships:
  - type: positional_mapping
    description: The value at a specific position in the input's central subgrid is moved to a specific corner position in the output grid.
```


## Natural Language Program

1.  Create a new 4x4 grid, initialized entirely with zeros. Call this the `output_grid`.
2.  Identify the value in the input grid at row 1, column 1. Place this value into the `output_grid` at row 0, column 0.
3.  Identify the value in the input grid at row 1, column 2. Place this value into the `output_grid` at row 0, column 3.
4.  Identify the value in the input grid at row 2, column 1. Place this value into the `output_grid` at row 3, column 0.
5.  Identify the value in the input grid at row 2, column 2. Place this value into the `output_grid` at row 3, column 3.
6.  Return the `output_grid`.