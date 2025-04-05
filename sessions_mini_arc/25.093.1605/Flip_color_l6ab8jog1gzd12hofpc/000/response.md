## Perception

The task involves transforming an input grid of numbers (colors) into an output grid of the same dimensions. The transformation appears to be a global color swap operation. In each example, two distinct non-zero colors are present in the input grid. The transformation rule swaps every instance of the first non-zero color with the second non-zero color, and vice-versa, throughout the entire grid. The background color (represented by 0) remains unchanged.

## Facts


```yaml
task_elements:
  - object: Grid
    properties:
      - type: 2D array or matrix
      - content: cells with numerical values (colors)
      - dimensions: variable (5x5 in examples)
  - object: Cell
    properties:
      - position: (row, column) coordinates
      - value: integer representing a color
  - object: Color
    properties:
      - type: integer value
      - role:
          - background (typically 0)
          - foreground (non-zero values)
relationships:
  - type: identity
    between: [input Grid.dimensions, output Grid.dimensions]
    description: The output grid has the same dimensions as the input grid.
  - type: mapping
    between: [input Cell.value, output Cell.value]
    description: The value of a cell in the output grid depends on its value in the input grid based on a global swap rule.
actions:
  - action: identify_swap_colors
    input: input Grid
    output: [color_A, color_B]
    description: Find the two unique non-zero color values present in the input grid.
  - action: swap_colors
    input: [input Grid, color_A, color_B]
    output: output Grid
    description: Iterate through each cell of the input grid. If a cell's value is color_A, change it to color_B in the output. If it's color_B, change it to color_A. If it's 0 (or any other color not identified for swapping), keep its value unchanged.
```


## Natural Language Program

1.  **Analyze** the input grid to identify the set of unique non-zero color values present. Assume there will be exactly two such distinct non-zero colors; let them be `color_1` and `color_2`.
2.  **Create** a new output grid with the same dimensions as the input grid.
3.  **Iterate** through each cell `(row, col)` of the input grid:
    *   Read the `input_color` at `input_grid[row][col]`.
    *   If `input_color` is equal to `color_1`, set the corresponding cell in the output grid to `color_2`: `output_grid[row][col] = color_2`.
    *   Else if `input_color` is equal to `color_2`, set the corresponding cell in the output grid to `color_1`: `output_grid[row][col] = color_1`.
    *   Else (if `input_color` is 0 or any other value not identified in step 1), keep the color unchanged: `output_grid[row][col] = input_color`.
4.  **Return** the completed output grid.