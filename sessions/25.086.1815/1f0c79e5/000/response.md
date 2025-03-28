**Perception of Task Elements:**

1.  **Input Structure:** The input is a square grid (9x9 in examples) mostly filled with the background color white (0). It contains a small, localized cluster of non-white pixels.
2.  **Input Objects:** This cluster consists of pixels of two distinct colors. One color is always red (2). The other color varies across examples (magenta (6), green (3), orange (7), yellow (4)).
3.  **Output Structure:** The output is a grid of the same size as the input, also mostly white (0). It features a prominent diagonal band pattern.
4.  **Output Pattern:** The pattern is a diagonal band, consistently 3 pixels wide, stretching across the grid.
5.  **Color Transformation:** The color used for the output band is the non-red color found in the input cluster. The red pixels from the input are effectively ignored or removed.
6.  **Pattern Orientation:** The diagonal band can have two orientations:
    *   Top-Left to Bottom-Right (TL-BR)
    *   Bottom-Left to Top-Right (BL-TR)
7.  **Orientation Determinant:** The orientation seems to depend on the vertical position of the input cluster. Specifically, if the highest pixel (minimum row index) of the input cluster is in the top few rows (rows 0, 1, or 2), the orientation is TL-BR. Otherwise, the orientation is BL-TR.
8.  **Band Placement:** The 3-pixel wide band appears consistently placed relative to the grid's main diagonal or anti-diagonal, depending on the orientation.
    *   For TL-BR, the band includes the main diagonal (`row == col`) and the two diagonals immediately above it (`row == col - 1`, `row == col - 2`).
    *   For BL-TR, the band includes the main anti-diagonal (`row + col == height - 1`) and the two anti-diagonals immediately "below" it towards the bottom-left (`row + col == height - 2`, `row + col == height - 3`).

**YAML Facts:**


```yaml
task_elements:
  - item: grids
    properties:
      - type: input and output
      - background_color: white (0)
      - size: H x W (9x9 in examples)
  - item: input_object
    properties:
      - type: cluster of connected non-white pixels
      - location: localized within the input grid
      - composition: contains pixels of exactly two colors
      - colors:
          - red (2)
          - another color C (variable: magenta, green, orange, yellow)
  - item: output_pattern
    properties:
      - type: diagonal band
      - color: C (the non-red color from the input_object)
      - width: 3 pixels
      - orientation: determined by input_object's vertical position
      - placement: extends across the entire grid
relationships:
  - type: color_mapping
    description: The output pattern's color is the non-red color present in the input object.
  - type: orientation_rule
    description: >
      If the minimum row index of any pixel in the input_object is less than or equal to 2,
      the output pattern orientation is Top-Left to Bottom-Right (TL-BR).
      Otherwise, the orientation is Bottom-Left to Top-Right (BL-TR).
  - type: pattern_definition
    description: >
      The output pattern is a 3-pixel wide diagonal band.
      If TL-BR, pixels (r, c) are colored if -2 <= r - c <= 0.
      If BL-TR, pixels (r, c) are colored if (H-1) - 2 <= r + c <= H-1, where H is the grid height.
actions:
  - action: identify_input_object
    description: Locate the connected group of non-white pixels.
  - action: extract_colors
    description: Identify the two colors present (red and color C).
  - action: find_min_row
    description: Determine the minimum row index of the input object.
  - action: determine_orientation
    description: Apply the orientation_rule based on min_row.
  - action: generate_output_grid
    description: Create a new grid of the same dimensions as the input, filled with white.
  - action: draw_diagonal_band
    description: Fill pixels in the output grid according to the determined orientation, color C, and pattern_definition.

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid filled entirely with the background color (white, 0). Record the height `H` of the grid.
2.  Scan the input grid to find all non-white pixels.
3.  Identify the two distinct non-white colors present in the input grid. One color will be red (2). Designate the other color as `pattern_color`.
4.  Find the minimum row index (`min_row`) among all non-white pixels found in step 2.
5.  Determine the band orientation:
    *   If `min_row <= 2`, set the orientation to `TL-BR`.
    *   Otherwise (`min_row > 2`), set the orientation to `BL-TR`.
6.  Define the band width `Wd = 3`.
7.  Iterate through each pixel position `(r, c)` in the output grid (where `r` is the row index from 0 to `H-1`, and `c` is the column index).
8.  Apply the coloring rule based on the orientation:
    *   If the orientation is `TL-BR`: Check if the condition `-(Wd-1) <= r - c <= 0` (i.e., `-2 <= r - c <= 0`) is true. If it is, set the color of the output grid pixel `(r, c)` to `pattern_color`.
    *   If the orientation is `BL-TR`: Check if the condition `(H-1) - (Wd-1) <= r + c <= H-1` (i.e., `H-3 <= r + c <= H-1`) is true. If it is, set the color of the output grid pixel `(r, c)` to `pattern_color`.
9.  Return the completed output grid.