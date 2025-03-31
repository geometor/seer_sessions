*   **Perception**: The task involves scaling the input grid by a factor of 2 in both height and width. Each pixel in the input grid corresponds to a 2x2 block in the output grid. The transformation rule depends on the color of the input pixel. Non-white pixels are expanded into a solid 2x2 block of their original color. White pixels (color 0) are transformed into a specific 2x2 pattern: blue (color 1) pixels on the main diagonal (top-left and bottom-right) and white pixels on the anti-diagonal (top-right and bottom-left).

*   **YAML Facts**:
    
```yaml
    task_context: Grid transformation involving scaling and pixel replacement based on color.
    grid_properties:
      - input_grid: 2D array of integers (colors).
      - output_grid: 2D array of integers (colors).
      - size_relation: Output grid dimensions are twice the input grid dimensions (height*2, width*2).
    objects:
      - pixels: Individual cells in the grid identified by their row, column, and color value.
    transformations:
      - scaling: Each input pixel maps to a 2x2 block in the output grid.
      - rule_based_replacement: The content of the 2x2 output block depends on the input pixel's color.
    rules:
      - condition: Input pixel color is not white (0).
        action: Fill the corresponding 2x2 output block with the input pixel's color.
        example: Input red (2) pixel at (r, c) maps to a 2x2 block of red (2) at (2*r, 2*c).
      - condition: Input pixel color is white (0).
        action: Fill the corresponding 2x2 output block with a specific pattern.
        pattern:
          - top-left: blue (1)
          - top-right: white (0)
          - bottom-left: white (0)
          - bottom-right: blue (1)
        mapping_coords:
          - input (r, c) -> output (2*r, 2*c) = blue (1)
          - input (r, c) -> output (2*r, 2*c+1) = white (0)
          - input (r, c) -> output (2*r+1, 2*c) = white (0)
          - input (r, c) -> output (2*r+1, 2*c+1) = blue (1)
    relationships:
      - mapping: Each input pixel at coordinates (r, c) directly determines the content of the 2x2 output block starting at coordinates (2*r, 2*c).
    ```


*   **Natural Language Program**:
    1.  Determine the dimensions (height `H`, width `W`) of the input grid.
    2.  Create a new output grid with dimensions `2*H` height and `2*W` width, initially filled with a default color (e.g., white/0).
    3.  Iterate through each pixel of the input grid at row `r` (from 0 to `H-1`) and column `c` (from 0 to `W-1`). Let the color of the input pixel be `input_color`.
    4.  Identify the top-left corner coordinates `(out_r, out_c)` of the corresponding 2x2 block in the output grid, where `out_r = 2 * r` and `out_c = 2 * c`.
    5.  Check the `input_color`:
        a.  If `input_color` is not white (0):
            *   Set the color of the four pixels in the output grid at `(out_r, out_c)`, `(out_r, out_c+1)`, `(out_r+1, out_c)`, and `(out_r+1, out_c+1)` to `input_color`.
        b.  If `input_color` is white (0):
            *   Set the color of the output grid pixel at `(out_r, out_c)` to blue (1).
            *   Set the color of the output grid pixel at `(out_r, out_c+1)` to white (0).
            *   Set the color of the output grid pixel at `(out_r+1, out_c)` to white (0).
            *   Set the color of the output grid pixel at `(out_r+1, out_c+1)` to blue (1).
    6.  Return the completed output grid.