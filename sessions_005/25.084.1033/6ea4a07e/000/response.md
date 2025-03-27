Okay, let's break down this task.

## Perception

1.  **Grid Structure**: All examples use 3x3 grids for both input and output.
2.  **Color Palette**: Each input grid consists of two colors: white (0) acting as a background, and one other specific color (gray-5, azure-8, or green-3). Each output grid also consists of two colors: white (0) as the background, and a different specific color (yellow-4, red-2, or blue-1).
3.  **Spatial Transformation**: The core transformation appears to be an inversion based on color. Where the input grid has the non-background color, the output grid has the background color (white). Conversely, where the input grid has the background color (white), the output grid has a new non-background color. The positions themselves are not changed, only the colors within those positions based on this rule.
4.  **Color Mapping**: There's a consistent relationship between the specific non-background color used in the input and the specific non-background color used in the output:
    *   Input gray (5) maps to output yellow (4).
    *   Input azure (8) maps to output red (2).
    *   Input green (3) maps to output blue (1).

## Facts


```yaml
observations:
  - task_type: color_transformation_spatial_inversion
  - grid_properties:
      - input_output_size_equality: true
      - fixed_size: 3x3 (observed in examples)
  - color_properties:
      - background_color: 0 (white) # Consistent across all inputs and outputs
      - input_foreground_colors: [3, 5, 8] # green, gray, azure
      - output_foreground_colors: [1, 2, 4] # blue, red, yellow
  - transformation_rules:
      - rule_type: pixel_wise_conditional_color_swap
      - condition_1:
          input_pixel_color: background_color (0)
          output_pixel_color: specific_output_foreground_color
      - condition_2:
          input_pixel_color: input_foreground_color (non-zero)
          output_pixel_color: background_color (0)
  - color_mapping: # Maps input foreground color to the specific output foreground color used when input is background
      - input: 3 # green
        output: 1 # blue
      - input: 5 # gray
        output: 4 # yellow
      - input: 8 # azure
        output: 2 # red
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Identify the background color (which is always white, 0) and the unique non-background color (let's call it `input_fg_color`) present in the input grid.
3.  Determine the corresponding non-background color for the output grid (let's call it `output_fg_color`) based on the `input_fg_color` using the following mapping:
    *   If `input_fg_color` is green (3), then `output_fg_color` is blue (1).
    *   If `input_fg_color` is gray (5), then `output_fg_color` is yellow (4).
    *   If `input_fg_color` is azure (8), then `output_fg_color` is red (2).
4.  Iterate through each pixel of the input grid at position (row, column):
    *   If the color of the input pixel at (row, column) is the background color (white, 0), set the color of the output grid pixel at (row, column) to `output_fg_color`.
    *   If the color of the input pixel at (row, column) is `input_fg_color`, set the color of the output grid pixel at (row, column) to the background color (white, 0).
5.  Return the completed output grid.