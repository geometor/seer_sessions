*   **Perception**: The task involves transforming a small input grid into a larger output grid. The input grids contain only white (0) and gray (5) pixels. The output grids contain white (0), blue (1), and red (2) pixels. The output grid's dimensions are exactly double the input grid's dimensions in both height and width, suggesting a scaling operation where each input pixel corresponds to a 2x2 block in the output grid. Observing the color transformations, input white pixels map to 2x2 blocks of white pixels in the output. Input gray pixels map to a specific 2x2 pattern: `[[blue, red], [red, blue]]` (or `[[1, 2], [2, 1]]`) in the output.

*   **YAML Facts**:
    
```yaml
    task_description: Scale the input grid by a factor of 2 and replace pixels based on color.
    grid_properties:
      - input_grid:
          colors_present: [white(0), gray(5)]
          size: Variable (e.g., 3x3 in examples)
      - output_grid:
          colors_present: [white(0), blue(1), red(2)]
          size: Double the dimensions of the input grid (e.g., 6x6 for a 3x3 input)
          relationship: Each pixel in the input grid maps to a 2x2 block in the output grid.
    transformations:
      - type: scaling
        factor: 2x2
        details: Each input pixel at (row, col) corresponds to the output block at (2*row, 2*col) to (2*row+1, 2*col+1).
      - type: color_replacement
        rules:
          - input_color: white(0)
            output_pattern: |
              [[white(0), white(0)],
               [white(0), white(0)]]
          - input_color: gray(5)
            output_pattern: |
              [[blue(1), red(2)],
               [red(2), blue(1)]]
    ```


*   **Natural Language Program**:
    1.  Initialize an output grid with dimensions twice the height and twice the width of the input grid.
    2.  Iterate through each pixel of the input grid, using its row index `r` and column index `c`.
    3.  Determine the color of the input pixel at `(r, c)`.
    4.  Locate the corresponding 2x2 block in the output grid, which starts at row `2*r` and column `2*c`.
    5.  If the input pixel color is white (0), fill the 2x2 output block with white (0) pixels.
    6.  If the input pixel color is gray (5), fill the 2x2 output block with the pattern: top-left = blue(1), top-right = red(2), bottom-left = red(2), bottom-right = blue(1).
    7.  Return the completed output grid.