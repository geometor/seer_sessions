## Perception

The task involves transforming an input grid into an output grid of the same dimensions.
The key elements in the input grids are pixels with the color azure (8). These azure pixels always form one or more contiguous objects (single pixels or blocks). The rest of the grid is filled with white (0) pixels.
In the output grids, the azure objects are replaced by objects of the same shape but colored red (2). These red objects are positioned exactly one row below the original position of the azure objects in the input grid. Pixels that were originally white remain white. If moving an azure pixel down would place it outside the grid boundaries, that pixel is effectively removed (or rather, the corresponding output cell remains white).

## Facts


```yaml
task_context:
  - description: Grid transformation based on object movement and color change.
  - grid_dimensions: Input and output grids have the same height and width in each example.
  - background_color: White (0) is the predominant background color and remains unchanged unless replaced by a transformed object.

objects:
  - id: input_object
    description: Contiguous block(s) of azure (8) pixels in the input grid.
    properties:
      - color: azure (8)
      - shape: Varies (single pixel, 2x2 block, 1x3 block)
      - location: Specific coordinates within the input grid.
  - id: output_object
    description: Object derived from the input_object in the output grid.
    properties:
      - color: red (2)
      - shape: Same shape as the corresponding input_object.
      - location: Shifted one row down compared to the corresponding input_object.

transformations:
  - action: identify_objects
    input: input_grid
    target: pixels with color azure (8)
    output: Set of azure objects (groups of contiguous azure pixels).
  - action: translate_object
    input: azure object coordinates (row, col)
    parameter: vertical_shift = +1 row
    output: new coordinates (row + 1, col)
  - action: change_color
    input: translated azure pixels
    parameter: new_color = red (2)
    output: red pixels at the new coordinates.
  - action: generate_output
    steps:
      - Create a new grid with the same dimensions as the input, filled with white (0).
      - For each azure pixel at (row, col) in the input grid:
        - Calculate the target coordinates (new_row, new_col) = (row + 1, col).
        - If new_row is within the grid's height boundary:
          - Set the pixel at (new_row, new_col) in the new grid to red (2).
    output: output_grid

relationships:
  - type: positional
    description: Each red pixel in the output grid is located one row directly below the corresponding azure pixel in the input grid.
  - type: color_mapping
    description: Azure (8) in the input maps to red (2) in the output after translation.
  - type: shape_preservation
    description: The shape and relative arrangement of pixels within an object are preserved during the transformation.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color white (0).
2.  Iterate through each pixel of the input grid.
3.  If a pixel at coordinates (row, column) has the color azure (8):
    a.  Calculate the target coordinates for the output grid as (row + 1, column).
    b.  Check if the target row (`row + 1`) is within the bounds of the grid height.
    c.  If the target coordinates are valid (within the grid boundaries), set the pixel at these target coordinates in the output grid to the color red (2).
4.  Return the completed output grid.