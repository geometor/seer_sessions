**Perception:**

Each input grid contains a horizontal line of magenta pixels (color 6) that spans the width of the grid. Above this magenta line, there is a single 2x2 square of a specific color (red, orange, or azure in the examples). Below the magenta line, there is another single 2x2 square of a different color (green, yellow, or maroon in the examples). The background of the grid is white (color 0).

The output grid is always a 2x2 square. The color of this output square is identical to the color of the 2x2 square located *above* the magenta line in the corresponding input grid. The square below the magenta line seems to be irrelevant to the output.

**Facts:**


```yaml
Examples: 3
Grid_Properties:
  - Input_Dimensions: Varying (9x6, 9x6, 8x8)
  - Output_Dimensions: Fixed (2x2)
  - Colors_Present_Input: [white(0), blue(1), red(2), green(3), yellow(4), gray(5), magenta(6), orange(7), azure(8), maroon(9)] - Specific subset used in each example.
  - Colors_Present_Output: Subset of non-white, non-magenta input colors.

Objects:
  - Type: Horizontal_Line
    Attributes:
      - Color: magenta (6)
      - Location: Spans the width of the grid, dividing it into upper and lower sections.
      - Role: Separator / Reference line
  - Type: Square
    Attributes:
      - Size: 2x2
      - Quantity: Two per input grid (one above magenta line, one below)
      - Color: Varies (non-white, non-magenta)
      - Location: One positioned entirely above the magenta line, one entirely below.
  - Type: Background
    Attributes:
      - Color: white (0)

Relationships:
  - The magenta line separates the grid into two distinct regions: upper and lower.
  - One colored square exists in the upper region.
  - One colored square exists in the lower region.
  - The output grid is a copy of the square located in the upper region of the input grid.

Actions:
  - Identify: Locate the horizontal magenta line.
  - Identify: Locate the 2x2 colored square positioned above the magenta line.
  - Extract: Copy the 2x2 square from the upper region.
  - Generate: Create the output grid using the extracted square.
```


**Natural Language Program:**

1.  Scan the input grid to find the horizontal line composed entirely of magenta (6) pixels.
2.  Identify the 2x2 square object located in the region of the grid *above* the magenta line.
3.  Create a new 2x2 grid.
4.  Fill the new 2x2 grid with the color of the square identified in step 2. This new grid is the output.