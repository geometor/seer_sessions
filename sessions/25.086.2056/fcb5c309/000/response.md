Okay, let's analyze the task examples.

**Perception of Task Elements:**

1.  **Inputs:** The input grids contain pixels of various colors (white 0, blue 1, red 2, green 3, yellow 4). Each input seems to have:
    *   A white background (0).
    *   One or more large, contiguous shapes of a single color (e.g., blue 'L's in Ex 1, red 'L's in Ex 2, green 'U' shapes in Ex 3).
    *   Several scattered pixels (or very small shapes) of another distinct color (e.g., green in Ex 1, yellow in Ex 2, red in Ex 3).
2.  **Outputs:** The output grids are smaller than the inputs (6x7 or 7x7). They depict a numerical digit shape.
    *   The digit shape is formed using the color of the scattered pixels from the input.
    *   The background of the output grid is white (0).
    *   The specific digit drawn corresponds to the *numerical value* of the scattered pixels' color (e.g., scattered green (3) -> digit '3'; scattered yellow (4) -> digit '4'; scattered red (2) -> digit '2').
3.  **Transformation:** The core transformation involves identifying the color of the 'scattered' pixels and using that color's numerical value to select and draw a specific digit pattern using that same color. The large shapes in the input seem to serve only to distinguish the 'scattered' pixels – the scattered color is the one *not* forming the largest object(s).

**YAML Facts:**


```yaml
task_context:
  input_grid:
    description: A 2D grid containing pixels of different colors (0-9).
    elements:
      - type: background
        color: white (0)
      - type: large_shapes
        description: One or more contiguous objects of the same color, typically the largest non-background objects in the grid. Their specific shape (L, U, etc.) varies but isn't directly used in the output.
        properties:
          - color: Varies (blue, red, green in examples)
          - size: Relatively large compared to other non-background elements.
      - type: scattered_pixels
        description: Pixels (or very small objects) of a distinct color, not part of the largest contiguous object(s).
        properties:
          - color: Varies (green, yellow, red in examples). This color's numerical value is significant.
          - size: Small, typically individual pixels or small groups.
          - distribution: Spread across the grid, not forming large structures.
  output_grid:
    description: A smaller 2D grid representing a single digit.
    properties:
      - size: Fixed based on the digit (e.g., 6x7 for '3', 7x7 for '2' and '4').
    elements:
      - type: digit_shape
        description: A pattern of pixels forming a numerical digit.
        properties:
          - color: Same as the 'scattered_pixels' color from the input.
          - value: The numerical digit represented corresponds to the color value of the 'scattered_pixels'.
      - type: background
        color: white (0)

transformation_logic:
  - step: Identify non-background pixels and group them into contiguous objects based on color.
  - step: Calculate the size (pixel count) of each object.
  - step: Find the maximum size among all objects.
  - step: Identify the color of the pixels that *do not* belong to any object(s) having the maximum size. This is the 'scatter_color'.
  - step: Determine the numerical value ('digit_value') of the 'scatter_color'.
  - step: Select a predefined pixel pattern corresponding to the 'digit_value'.
  - step: Create the output grid using the 'scatter_color' for the digit pattern pixels and white (0) for the background pixels.

predefined_digit_patterns: # Using 'C' for scatter_color, '_' for white(0)
  '2': # 7x7
    - C C C C C C C
    - C _ C _ C _ C
    - C _ _ _ _ _ C
    - C _ _ _ _ _ C
    - C _ C _ _ _ C
    - C _ _ _ _ C C
    - C C C C C C C
  '3': # 6x7
    - C C C C C C C
    - C _ _ C _ _ C
    - C _ _ _ _ _ C
    - C C _ C _ _ C
    - C _ _ _ _ _ C
    - C C C C C C C
  '4': # 7x7
    - C C C C C C C
    - C _ _ _ _ _ C
    - C C _ _ _ _ C
    - C _ _ _ _ _ C
    - C _ _ _ C _ C
    - C _ _ _ _ _ C
    - C C C C C C C
  # Note: Patterns for other digits (0, 1, 5-9) might be needed if they appear as scatter colors.
```


**Natural Language Program:**

1.  Analyze the input grid to identify all contiguous objects composed of non-white pixels. Consider pixels connected horizontally or vertically to be part of the same object.
2.  For each object, determine its color and size (number of pixels).
3.  Find the size of the largest object(s). Let this maximum size be `max_size`.
4.  Identify the color (let's call it `scatter_color`) of any non-white pixels that are *not* part of *any* object whose size equals `max_size`. (Assume this process uniquely identifies one `scatter_color`).
5.  Determine the numerical value of `scatter_color`. Let this be `digit_value`.
6.  Retrieve the predefined pixel grid pattern corresponding to `digit_value`.
7.  Construct the output grid based on this pattern: replace the placeholder for the digit color with `scatter_color` and the placeholder for the background with white (0).
8.  Return the constructed output grid.