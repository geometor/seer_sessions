*   **Perception:** The input grids contain a few isolated, single, non-white pixels scattered across a white background. The output grids show that each of these non-white pixels has been replaced by a 3x3 square. The center of each square retains the original color of the input pixel, while the 8 surrounding pixels of the square adopt a new color. This new border color seems dependent on the original center color.

*   **YAML Facts:**
    
```yaml
    facts:
      - element: Input Grid
        description: A 2D grid primarily composed of white pixels (0), with a few scattered single non-white pixels.
        properties:
          - dimensions: Variable (e.g., 16x16, 6x6, 12x12)
          - background_color: white (0)
          - foreground_elements:
              type: Single Pixels
              colors: Varies (e.g., green(3), red(2), azure(8))
              distribution: Sparse, isolated
      - element: Output Grid
        description: A 2D grid of the same dimensions as the input, where input non-white pixels are expanded into 3x3 squares.
        properties:
          - dimensions: Same as input
          - background_color: white (0)
          - foreground_elements:
              type: 3x3 Squares
              structure: Center pixel retains original input color, border pixels have a new color.
              color_mapping:
                - center: green (3) -> border: magenta (6)
                - center: red (2) -> border: blue (1)
                - center: azure (8) -> border: yellow (4)
      - transformation:
          action: Expansion and Color Mapping
          input_object: Each non-white pixel in the input grid.
          output_object: A 3x3 square in the output grid.
          process:
            - Locate each non-white pixel in the input grid.
            - Determine its color (center_color) and position.
            - Determine the corresponding border_color based on the center_color using the defined mapping.
            - Place a 3x3 square in the output grid, centered at the input pixel's position.
            - Set the center pixel of the square to center_color.
            - Set the 8 border pixels of the square to border_color.
          relationship: The position of the 3x3 square in the output corresponds to the position of the single non-white pixel in the input. The colors within the square are determined by the color of the original input pixel.
    ```


*   **Natural Language Program:**
    1.  Create a new output grid with the same dimensions as the input grid, initialized with white (0) pixels.
    2.  Iterate through each pixel of the input grid.
    3.  If a pixel is not white (0):
        a.  Identify its color (let's call it `center_color`) and its coordinates (row, col).
        b.  Determine the `border_color` based on the `center_color`:
            *   If `center_color` is green (3), set `border_color` to magenta (6).
            *   If `center_color` is red (2), set `border_color` to blue (1).
            *   If `center_color` is azure (8), set `border_color` to yellow (4).
            *   Otherwise (for any other color not seen in examples), keep the `border_color` undefined or handle as an edge case (e.g., default to white or the center color - based on examples, only these 3 mappings exist).
        c.  Draw a 3x3 square on the output grid centered at (row, col):
            i.   Set the pixel at (row, col) in the output grid to `center_color`.
            ii.  For each of the 8 neighboring pixels (including diagonals) around (row, col), if their coordinates are within the grid boundaries, set their color in the output grid to `border_color`.
    4.  Return the modified output grid.