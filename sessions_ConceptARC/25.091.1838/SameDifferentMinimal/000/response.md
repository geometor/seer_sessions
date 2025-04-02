**Perception:**
The task involves transforming the colors of pixels within a grid based on their original color. The input grids contain one or more hollow rectangular or square shapes made of various colors (green, blue, magenta, red, azure, orange) set against a white background. The output grids preserve the shapes and positions of these objects but change their colors according to a specific rule. The white background remains unchanged.

**YAML Facts:**


```yaml
task_type: color_transformation
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains_objects: true
  - type: object
    properties:
      - composition: contiguous pixels of the same non-white color
      - shape: hollow rectangles/squares
      - colors_observed_input: [green (3), blue (1), magenta (6), red (2), azure (8), orange (7)]
      - colors_observed_output: [yellow (4), gray (5)]
transformation:
  type: pixel_wise_color_replacement
  mapping:
    - input_color: white (0)
      output_color: white (0)
    - input_color: green (3)
      output_color: yellow (4)
    - input_color: blue (1)
      output_color: gray (5)
    - input_color: magenta (6)
      output_color: gray (5)
    - input_color: red (2)
      output_color: yellow (4)
    - input_color: azure (8)
      output_color: gray (5)
    - input_color: orange (7)
      output_color: gray (5)
  preserves:
    - grid_dimensions
    - object_shape
    - object_position
    - background_pixels
```


**Natural Language Program:**

1.  Iterate through each pixel of the input grid.
2.  Check the color of the current pixel.
3.  If the pixel color is white (0), keep its color as white (0) in the output grid at the same position.
4.  If the pixel color is red (2) or green (3), change its color to yellow (4) in the output grid at the same position.
5.  If the pixel color is blue (1), magenta (6), orange (7), or azure (8), change its color to gray (5) in the output grid at the same position.
6.  Construct the output grid using the transformed pixel colors.