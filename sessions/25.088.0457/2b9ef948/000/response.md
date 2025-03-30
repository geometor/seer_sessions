**Perception**

1.  **Input/Output Grid Sizes:** The input and output grids consistently maintain the same dimensions across all examples.
2.  **Input Composition:** The input grids predominantly consist of a white (0) background. They contain distinct objects or patterns composed of yellow (4), gray (5), and one other unique color (orange (7) in train\_1, green (3) in train\_2, azure (8) in train\_3).
3.  **Output Composition:** The output grids are filled almost entirely with a single color, which corresponds to the unique non-white, non-yellow, non-gray color found in the respective input grid. Embedded within this background color are yellow (4) pixels.
4.  **Transformation Pattern:** The core transformation involves identifying two key elements from the input:
    *   The unique color that is *not* white (0), yellow (4), or gray (5). This color becomes the background fill for the output grid.
    *   The exact locations of all yellow (4) pixels. These locations are preserved in the output grid, maintaining their yellow color, while all other original pixel colors (white, gray, and the unique background color itself) are replaced by the new background color.
5.  **Object Irrelevance:** The specific shapes or arrangements of the gray (5) objects, or the non-yellow pixels within the yellow objects, do not seem to directly influence the final pattern, other than the unique color determining the output background. Only the presence and location of yellow pixels and the identity of the unique color matter.

**Facts (YAML)**


```yaml
task_description: Overwrite the input grid based on specific color rules, preserving only the locations of yellow pixels.
grid_properties:
  - input_output_size_relationship: Identical dimensions.
  - background_color_input: Predominantly white (0).
  - background_color_output: Determined by a unique color in the input.

color_rules:
  - target_color_for_preservation: yellow (4)
  - ignored_colors_for_output_pattern: white (0), gray (5)
  - background_determining_color: The single color present in the input grid that is NOT white (0), yellow (4), or gray (5).
    - example_1: orange (7)
    - example_2: green (3)
    - example_3: azure (8)

transformation_steps:
  - identify_background_color: Scan the input grid to find the unique color that isn't white (0), yellow (4), or gray (5).
  - initialize_output_grid: Create a new grid with the same dimensions as the input.
  - fill_background: Fill the entire output grid with the identified background color.
  - preserve_yellow_pixels: Iterate through the input grid. For every pixel that is yellow (4), overwrite the corresponding pixel in the output grid with yellow (4).

element_persistence:
  - yellow_pixels: Locations are preserved, color remains yellow (4).
  - other_pixels: Locations are overwritten by the new background color, unless the original pixel was yellow (4).
```


**Natural Language Program**

1.  Determine the dimensions (height and width) of the input grid.
2.  Scan the input grid to find the single, unique color value that is *not* white (0), yellow (4), or gray (5). Let this be the `output_background_color`.
3.  Create a new output grid with the same dimensions as the input grid.
4.  Fill the entire output grid with the `output_background_color`.
5.  Iterate through each cell (pixel) of the input grid at position (row, column).
6.  If the color of the input grid cell at (row, column) is yellow (4), then set the color of the output grid cell at the corresponding (row, column) to yellow (4).
7.  Return the completed output grid.