## Perception

The input is always a 3x3 grid. The output is always a 6x3 grid.
Observing the relationship between the input and output grids across all examples, it becomes clear that the output grid is constructed by taking the original input grid and appending a vertically flipped version of the input grid directly below it.

- The top half (first 3 rows) of the output grid is identical to the input grid.
- The bottom half (last 3 rows) of the output grid is the input grid flipped upside down. Specifically, the last row of the output matches the first row of the input, the second-to-last row of the output matches the second row of the input, and the fourth row of the output matches the third row of the input.

## Facts


```yaml
task_context:
  - description: The task requires transforming a smaller input grid into a larger output grid by reflecting and appending.
  - input_grid_properties:
      - shape: Fixed 3x3 in all examples.
  - output_grid_properties:
      - shape: Fixed 6x3 in all examples (twice the height of the input).
      - relationship_to_input:
          - The top half of the output grid is identical to the input grid.
          - The bottom half of the output grid is a vertical reflection (flipped top-to-bottom) of the input grid.

transformation_steps:
  - step: 1
    action: Copy the input grid. This forms the top part of the output.
  - step: 2
    action: Create a vertically flipped version of the input grid.
    details: The order of the rows is reversed (row 0 becomes the last row, row 1 the second-to-last, etc.).
  - step: 3
    action: Concatenate the original input grid and the flipped grid vertically.
    details: The original grid is placed above the flipped grid.
  - step: 4
    action: The resulting concatenated grid is the final output.
```


## Natural Language Program

1.  Identify the input grid.
2.  Create a new grid by vertically flipping the input grid (reverse the order of the rows).
3.  Construct the output grid by stacking the original input grid on top of the flipped grid. The height of the output grid will be twice the height of the input grid, while the width remains the same.