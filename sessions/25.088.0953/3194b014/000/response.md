*   **Perception:** Each input grid contains multiple shapes and colors scattered throughout. Among these, there is always one prominent, solid square shape composed of a single color (excluding the background color, white). The output grid is consistently a 3x3 solid grid, and its color matches the color of the largest solid square found in the corresponding input grid. The task seems to involve identifying this largest square object and using its color to generate the output.

*   **Facts:**
    
```yaml
    examples:
      - id: train_1
        input:
          grid_size: [20, 20]
          objects:
            - type: square
              color: yellow (4)
              size: 5x5
              location: approx_center_bottom
            - other_shapes: various smaller shapes and scattered pixels of magenta, orange, red, maroon, white
        output:
          grid_size: [3, 3]
          content: solid_fill
          color: yellow (4)
        relationship: Output color matches the color of the largest solid square in the input.

      - id: train_2
        input:
          grid_size: [20, 20]
          objects:
            - type: square
              color: green (3)
              size: 6x6
              location: approx_center_right
            - other_shapes: various smaller shapes and scattered pixels of azure, blue, gray, maroon, yellow, white
        output:
          grid_size: [3, 3]
          content: solid_fill
          color: green (3)
        relationship: Output color matches the color of the largest solid square in the input.

      - id: train_3
        input:
          grid_size: [20, 20]
          objects:
            - type: square
              color: azure (8)
              size: 7x7
              location: approx_top_left
            - other_shapes: various smaller shapes and scattered pixels of green, red, magenta, maroon, yellow, white
        output:
          grid_size: [3, 3]
          content: solid_fill
          color: azure (8)
        relationship: Output color matches the color of the largest solid square in the input.

    common_properties:
      - input_grid_size: 20x20
      - output_grid_size: 3x3
      - output_type: monochromatic_grid
      - background_color: white (0) is ignored in the search for the relevant object.
      - target_object: The largest solid (monochromatic) square object within the input grid.

    transformation:
      - Identify all contiguous regions of non-white pixels.
      - Filter these regions to find those that form perfect squares.
      - Determine the square with the largest side length (or area).
      - Create a new 3x3 grid.
      - Fill the new grid entirely with the color of the largest square found.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all contiguous blocks of pixels that have the same, non-white color.
    2.  For each identified block, check if its dimensions form a perfect square (height equals width).
    3.  Compare the sizes (side lengths or areas) of all identified squares.
    4.  Select the square with the largest size. If there are multiple squares of the same largest size, any one of them can be chosen (as implied by the examples, there seems to be a unique largest one).
    5.  Determine the color of this largest square.
    6.  Construct a 3x3 output grid.
    7.  Fill every pixel of the output grid with the color identified in step 5.