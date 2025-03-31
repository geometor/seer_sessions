**Perception:**

1.  **Input Grid:** The input is always a 3x3 grid. It contains exactly one non-white pixel (colors 4, 5, 3, 8, 7 in the examples). All other pixels are white (color 0).
2.  **Output Grid:** The output is always a 9x9 grid. It contains a pattern made of the same non-white color found in the input grid, set against a white background.
3.  **Transformation:** The position of the single non-white pixel in the 3x3 input grid determines *which* specific 9x9 pattern is generated in the output. The color of that input pixel determines the color used to draw the output pattern. There seems to be a unique, fixed 9x9 pattern associated with each of the 9 possible positions in the 3x3 input grid.

**Facts YAML:**


```yaml
task_description: Map the location and color of a single pixel in a 3x3 grid to a specific 9x9 pattern colored with that pixel's color.

elements:
  - element: input_grid
    description: A 3x3 grid.
    properties:
      - contains exactly one non-white pixel.
      - all other pixels are white (0).
  - element: output_grid
    description: A 9x9 grid.
    properties:
      - contains a pattern composed of a single non-white color against a white background (0).

transformation:
  - step: 1
    action: Identify the non-white pixel in the input grid.
    outputs:
      - name: pixel_color
        description: The color value (1-9) of the non-white pixel.
      - name: pixel_position
        description: The (row, column) coordinates of the non-white pixel within the 3x3 input grid.
  - step: 2
    action: Select a predefined 9x9 pattern based on the identified pixel_position.
    notes: There is a unique 9x9 binary pattern (or template) associated with each of the 9 possible positions in the 3x3 grid.
    outputs:
      - name: selected_pattern
        description: The 9x9 binary pattern corresponding to the input pixel's position.
  - step: 3
    action: Generate the output grid.
    inputs:
      - selected_pattern
      - pixel_color
    process: Create a 9x9 grid where cells corresponding to '1' (or foreground) in the selected_pattern are filled with pixel_color, and cells corresponding to '0' (or background) are filled with white (0).

relationships:
  - The position of the non-white pixel in the input grid determines the structure/shape of the pattern in the output grid.
  - The color of the non-white pixel in the input grid determines the color of the pattern in the output grid.
  - Each input grid maps to exactly one output grid.
```


**Natural Language Program:**

1.  Scan the 3x3 input grid to find the single pixel that is not white (color 0).
2.  Record the color of this pixel and its row and column coordinates (position).
3.  Determine which of the 9 possible predefined 9x9 patterns corresponds to the position found in step 2.
4.  Create a new 9x9 grid.
5.  Fill the new 9x9 grid according to the selected pattern: where the pattern indicates the foreground, use the color recorded in step 2; where the pattern indicates the background, use white (color 0).
6.  The resulting 9x9 grid is the output.