## Perception of Elements

The input grids consist of a white (0) background divided by green (3) horizontal and vertical lines. These lines partition the grid into several rectangular compartments. The output grids retain the green lines in their original positions but fill some of the white compartments with specific colors based on their location relative to the dividing lines.

## YAML Fact Document


```yaml
elements:
  - object: grid
    description: A 2D array of pixels representing colors.
    properties:
      - width: varies
      - height: varies
      - background_color: white (0)
  - object: line
    description: Continuous sequences of green (3) pixels, either horizontal or vertical.
    properties:
      - color: green (3)
      - orientation: horizontal or vertical
    relationships:
      - divides the grid into compartments
      - remain unchanged between input and output
  - object: compartment
    description: Rectangular areas of the grid bounded by green lines or grid edges. Initially filled with white (0) pixels.
    properties:
      - color: initially white (0)
      - location: relative position within the grid (e.g., top-left, top-right, bottom-left, bottom-right, central)
    actions:
      - fill: Some compartments are filled with a new color in the output.
relationships:
  - The color used to fill a white compartment depends on its location relative to the outermost green lines.
colors_used:
  - white (0): Background, some compartments remain white.
  - green (3): Dividing lines.
  - red (2): Fills the top-left corner compartment.
  - yellow (4): Fills the top-right corner compartment.
  - blue (1): Fills the bottom-left corner compartment.
  - azure (8): Fills the bottom-right corner compartment.
  - orange (7): Fills the central compartments located between the topmost and bottommost horizontal lines and between the leftmost and rightmost vertical lines.
```


## Natural Language Program

1.  Identify all horizontal and vertical lines composed of green (3) pixels in the input grid.
2.  Determine the row index of the topmost horizontal green line (`first_h_line`) and the bottommost horizontal green line (`last_h_line`).
3.  Determine the column index of the leftmost vertical green line (`first_v_line`) and the rightmost vertical green line (`last_v_line`).
4.  Create a copy of the input grid to serve as the output grid.
5.  Iterate through each pixel (`pixel`) of the input grid at position (`row`, `col`).
6.  If the `pixel` color is white (0):
    *   Check its position relative to the identified green lines:
        *   If `row < first_h_line` and `col < first_v_line`, set the corresponding pixel in the output grid to red (2).
        *   If `row < first_h_line` and `col > last_v_line`, set the corresponding pixel in the output grid to yellow (4).
        *   If `row > last_h_line` and `col < first_v_line`, set the corresponding pixel in the output grid to blue (1).
        *   If `row > last_h_line` and `col > last_v_line`, set the corresponding pixel in the output grid to azure (8).
        *   If `row > first_h_line` and `row < last_h_line` and `col > first_v_line` and `col < last_v_line`, set the corresponding pixel in the output grid to orange (7).
7.  Pixels that are green (3) in the input remain green (3) in the output. White pixels not meeting any of the conditions in step 6 remain white (0) in the output.
8.  Return the modified output grid.