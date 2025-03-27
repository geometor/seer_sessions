## Perception

The task involves transforming an input grid into an output grid. Based on the provided examples:

1.  **Input and Output Dimensions:** The dimensions (height and width) of the output grid are always identical to the dimensions of the input grid in all examples.
2.  **Content Preservation:** The individual pixel values (colors) present in the input grid are all present in the output grid, and no new colors are introduced.
3.  **Structural Change:** The arrangement of the pixels changes between input and output. Comparing the rows, the top row of the input consistently appears as the bottom row of the output. The second row from the top in the input becomes the second row from the bottom in the output, and this pattern continues. The bottom row of the input becomes the top row of the output.
4.  **Transformation Type:** This pattern strongly suggests a vertical reflection or flip along the horizontal midline of the grid. The order of rows is reversed. The content within each row (the order of pixels horizontally) remains unchanged.

## Facts


```yaml
task_type: grid_transformation
transformation: spatial_reflection
input_object:
  type: grid
  properties:
    - height: H
    - width: W
    - pixels: array of colors
output_object:
  type: grid
  properties:
    - height: H  # Same as input height
    - width: W   # Same as input width
    - pixels: array of colors
relationship:
  - type: vertical_reflection
    description: The output grid is the input grid flipped vertically.
  - type: row_mapping
    description: >
      Row `i` (0-indexed) of the input grid becomes row `H - 1 - i`
      of the output grid, where `H` is the height of the grid.
    details:
      - input_row_index: i
      - output_row_index: H - 1 - i
      - row_content: Unchanged horizontally
```


## Natural Language Program

1.  Receive the input grid.
2.  Determine the height (number of rows) of the input grid.
3.  Create a new grid (the output grid) with the same height and width as the input grid.
4.  Iterate through the rows of the input grid, from the first row (index 0) to the last row (index `height - 1`).
5.  For each input row at index `i`, copy its contents to the output grid at row index `height - 1 - i`.
6.  Return the newly created output grid.