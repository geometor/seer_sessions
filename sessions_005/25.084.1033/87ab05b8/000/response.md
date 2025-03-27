*   **Perception:**
    *   All examples use 4x4 grids.
    *   The input grids contain various colored pixels scattered on a magenta (6) background.
    *   A single red pixel (2) is present in each input grid. The position of this red pixel varies.
    *   Other colors present in the inputs (maroon-9, blue-1, yellow-4, gray-5, white-0, azure-8) do not appear in the outputs.
    *   The output grids are also 4x4.
    *   The output grids consist mostly of the magenta background color (6).
    *   Each output grid features a 2x2 square of red pixels (2) located in the bottom half of the grid.
    *   The horizontal position of this 2x2 red square in the output seems dependent on the horizontal position of the single red pixel in the input.
    *   If the input red pixel is in the left half (columns 0 or 1), the output 2x2 red square is in the bottom-left corner (starting at row 2, column 0).
    *   If the input red pixel is in the right half (columns 2 or 3), the output 2x2 red square is in the bottom-right corner (starting at row 2, column 2).
    *   The top half (rows 0 and 1) of the output grid is always filled with the magenta background color (6).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      size: constant (4x4 in examples)
      background_color: magenta (6)
    input_elements:
      - object: target_pixel
        color: red (2)
        quantity: exactly one per grid
        location: variable
      - object: other_pixels
        color: various (maroon, blue, yellow, gray, white, azure)
        location: variable
        role: ignored in output
      - object: background
        color: magenta (6)
    output_elements:
      - object: background
        color: magenta (6)
        location: fills the grid initially, persists in the top half
      - object: output_square
        shape: 2x2 square
        color: red (2)
        location: bottom half of the grid (starting at row H/2)
        placement_rule: dependent on the input target_pixel's horizontal position
    relationships:
      - type: dependency
        element1: output_square.column_start
        element2: input.target_pixel.column_index
        rule: |
          Let W be the grid width.
          If target_pixel.column_index < W/2, then output_square.column_start = 0.
          If target_pixel.column_index >= W/2, then output_square.column_start = W/2.
      - type: fixed_placement
        element: output_square.row_start
        value: H/2 (where H is grid height)
    actions:
      - identify the single red (2) pixel in the input grid.
      - determine its column index.
      - create an output grid of the same dimensions, filled with magenta (6).
      - determine the starting column (0 or W/2) for the output square based on the input red pixel's column.
      - draw a 2x2 red (2) square in the output grid starting at row H/2 and the determined starting column.
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Locate the single pixel with the color red (2) within the input grid. Record its column index, `c_in`.
    3.  Create a new output grid with the same dimensions (H x W) as the input grid.
    4.  Fill the entire output grid with the background color magenta (6).
    5.  Determine the starting column (`c_out`) for the 2x2 red square in the output grid based on the input red pixel's column index (`c_in`):
        *   If `c_in` is less than `W / 2`, set `c_out` to 0.
        *   Otherwise (if `c_in` is greater than or equal to `W / 2`), set `c_out` to `W / 2`.
    6.  Determine the starting row (`r_out`) for the 2x2 red square, which is always `H / 2`.
    7.  Fill the 2x2 area in the output grid starting at position (`r_out`, `c_out`) with the color red (2). Specifically, set the pixels at (`r_out`, `c_out`), (`r_out`, `c_out + 1`), (`r_out + 1`, `c_out`), and (`r_out + 1`, `c_out + 1`) to red (2).
    8.  Return the modified output grid.