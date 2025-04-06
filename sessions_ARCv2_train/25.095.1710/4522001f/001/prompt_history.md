
## train_1

**input:**
```
0 0 0
0 2 3
0 3 3
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
```


## train_2

**input:**
```
3 3 0
3 2 0
0 0 0
```


**output:**
```
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a small input grid (3x3) into a larger output grid (9x9). The grids contain integer values, seemingly representing categories or colors. The core operation appears to be an upscaling process where each cell in the input grid determines the content of a corresponding 3x3 subgrid in the output grid. There's a specific rule for mapping the input cell values to the output subgrid values: input value 0 maps to output value 0, while any non-zero input value (specifically 2 and 3 in the examples) maps to the output value 3.

## YAML Fact Document


```yaml
task_description: Grid transformation involving upscaling and value mapping.
elements:
  - object: input_grid
    properties:
      - type: grid
      - dimensions: 3x3
      - cell_values: integers (e.g., 0, 2, 3)
  - object: output_grid
    properties:
      - type: grid
      - dimensions: 9x9
      - cell_values: integers (e.g., 0, 3)
relations:
  - type: mapping
    description: Each cell in the input_grid maps to a 3x3 block in the output_grid.
    details: The input cell at (row, col) maps to the output block starting at (row * 3, col * 3).
actions:
  - action: upscale
    input: input_grid
    output: output_grid (structure)
    factor: 3 (in both dimensions)
  - action: value_transformation
    input: value from input_grid cell
    output: value for the corresponding 3x3 output_grid block
    rule:
      - condition: input value is 0
        result: output block filled with 0
      - condition: input value is non-zero (e.g., 2 or 3)
        result: output block filled with 3
```


## Natural Language Program

1.  Create a new output grid with dimensions three times larger than the input grid in both height and width (e.g., if input is 3x3, output is 9x9).
2.  Iterate through each cell `(r, c)` of the input grid.
3.  Determine the value `v` of the input cell `(r, c)`.
4.  Identify the corresponding 3x3 block in the output grid, which starts at row `r * 3` and column `c * 3`.
5.  If the input value `v` is 0, fill the entire 3x3 output block with the value 0.
6.  If the input value `v` is non-zero, fill the entire 3x3 output block with the value 3.
7.  Return the completed output grid.
