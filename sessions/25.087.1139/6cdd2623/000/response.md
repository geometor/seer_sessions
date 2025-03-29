**Perception:**

1.  **Input/Output Structure:** Both input and output are 2D grids of pixels with integer values representing colors. The output grid always has the same dimensions as the input grid.
2.  **Background:** The background color in both input and output is white (0).
3.  **Input Content:** Inputs contain scattered single pixels of various colors (blue, red, green, yellow, gray, azure) on a white background.
4.  **Output Content:** Outputs consist primarily of the white background, but with one or more complete horizontal or vertical lines drawn in a specific color.
5.  **Transformation Logic:** The transformation identifies pairs of pixels of the *same color* located on opposite edges of the input grid.
    *   If a pair of same-colored pixels exists on the left edge (column 0) and right edge (last column) within the *same row*, a horizontal line of that color is drawn across that entire row in the output grid.
    *   If a pair of same-colored pixels exists on the top edge (row 0) and bottom edge (last row) within the *same column*, a vertical line of that color is drawn down that entire column in the output grid.
6.  **Color Preservation:** The color of the line(s) drawn in the output matches the color of the identified edge pixel pairs in the input.
7.  **Irrelevant Pixels:** All other pixels in the input grid that are not part of these identified edge pairs are ignored and replaced by the white background color in the output.
8.  **Multiple Lines:** It's possible for multiple lines (horizontal and/or vertical) to be present in the output if multiple qualifying edge pairs are found in the input.

**Facts:**


```yaml
task_description: Identify pairs of same-colored pixels on opposite edges of the input grid and draw corresponding full lines (horizontal or vertical) on an initially white output grid of the same dimensions.

elements:
  - name: input_grid
    type: 2D array of integers (colors)
  - name: output_grid
    type: 2D array of integers (colors)
    properties:
      - same dimensions as input_grid
      - initialized to all white (0)
  - name: edge_pixel_pair
    type: two pixels
    properties:
      - same color (non-white)
      - located on opposite edges of the input grid
      - either in the same row (left/right edges) or same column (top/bottom edges)
  - name: line
    type: sequence of pixels
    properties:
      - horizontal or vertical
      - spans the entire width or height of the grid
      - color matches the corresponding edge_pixel_pair

relationships:
  - type: defines
    source: edge_pixel_pair (same row, left/right edges)
    target: horizontal line
    details: The row index of the pair determines the row of the horizontal line. The color of the pair determines the color of the line.
  - type: defines
    source: edge_pixel_pair (same column, top/bottom edges)
    target: vertical line
    details: The column index of the pair determines the column of the vertical line. The color of the pair determines the color of the line.
  - type: transformation
    input: input_grid
    output: output_grid
    steps:
      - Initialize output_grid with white pixels.
      - Identify all horizontal edge_pixel_pairs.
      - For each horizontal pair, draw the corresponding horizontal line on output_grid.
      - Identify all vertical edge_pixel_pairs.
      - For each vertical pair, draw the corresponding vertical line on output_grid.

examples:
  - example: train_1
    input_grid_dims: [13, 20]
    horizontal_pairs:
      - color: red (2), row: 3
      - color: red (2), row: 11
    vertical_pairs: []
    output_lines:
      - type: horizontal, color: red (2), row: 3
      - type: horizontal, color: red (2), row: 11
  - example: train_2
    input_grid_dims: [11, 22]
    horizontal_pairs:
      - color: green (3), row: 8
    vertical_pairs:
      - color: green (3), column: 11
    output_lines:
      - type: horizontal, color: green (3), row: 8
      - type: vertical, color: green (3), column: 11
  - example: train_3
    input_grid_dims: [15, 17]
    horizontal_pairs:
      - color: azure (8), row: 10
    vertical_pairs:
      - color: azure (8), column: 13
    output_lines:
      - type: horizontal, color: azure (8), row: 10
      - type: vertical, color: azure (8), column: 13

```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid, and fill it entirely with the background color (white, 0).
2.  Get the height (H) and width (W) of the input grid.
3.  Iterate through each row index `r` from 0 to H-1:
    *   Check if the pixel at the left edge `(r, 0)` and the pixel at the right edge `(r, W-1)` are the same non-white color.
    *   If they are the same color `C`, then draw a horizontal line in the output grid at row `r` using color `C`. This means setting all pixels `output_grid[r, c]` to `C` for `c` from 0 to W-1.
4.  Iterate through each column index `c` from 0 to W-1:
    *   Check if the pixel at the top edge `(0, c)` and the pixel at the bottom edge `(H-1, c)` are the same non-white color.
    *   If they are the same color `C`, then draw a vertical line in the output grid at column `c` using color `C`. This means setting all pixels `output_grid[r, c]` to `C` for `r` from 0 to H-1.
5.  Return the modified output grid.