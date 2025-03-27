## Perception

The task involves a simple color substitution within a grid. Each example shows an input grid containing pixels of various colors (orange, blue, azure) and an output grid where only the orange pixels have been changed. The positions and colors of all other pixels (blue and azure) remain identical between the input and output grids. The consistent change across all examples is the replacement of the color orange (value 7) with the color gray (value 5).

## Facts


```yaml
task_type: color_replacement
input_elements:
  - element_type: grid
    description: A 2D array of pixels with different colors.
    colors_present: [orange(7), blue(1), azure(8)]
output_elements:
  - element_type: grid
    description: A 2D array of pixels derived from the input grid.
    colors_present: [gray(5), blue(1), azure(8)]
transformation:
  - type: pixel_color_change
    input_color: orange(7)
    output_color: gray(5)
    scope: applies to all pixels with the input color
    condition: none
    unchanged_colors: [blue(1), azure(8)]
relationships:
  - type: spatial_invariance
    description: The dimensions of the grid remain unchanged.
  - type: color_invariance
    description: Pixels that are not orange retain their original color and position.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through each pixel (cell) of the input grid.
3.  If a pixel's color is orange (value 7), change the color of the corresponding pixel in the output grid to gray (value 5).
4.  If a pixel's color is not orange, keep its original color in the corresponding position in the output grid.
5.  Return the modified output grid.