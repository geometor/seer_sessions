## Perception

1.  **Input/Output Structure:** Each input grid contains a structure composed of colored pixels, primarily located towards the bottom half of the grid. The output grid is identical to the input grid, except for the addition of new pixels of a specific color in the upper part of the grid. The original structure remains unchanged.
2.  **Key Element - Emitter:** In each input, there's a distinct horizontal segment (which can be just one pixel wide) of a single color (blue, green, or yellow in the examples) positioned directly above pixels of a *different* color. This segment appears to be the key element triggering the transformation. Let's call this the "emitter" segment.
3.  **Emitter Properties:** The emitter segment has a specific color, a width, and a central position (row `y_c`, column `x_c`).
4.  **Transformation Logic:** The transformation involves adding new pixels to the grid. The color of these new pixels is the same as the emitter segment's color. The positions of these new pixels are determined relative to the center of the emitter segment `(y_c, x_c)`.
5.  **Pattern Dependency:** The specific pattern (relative coordinates) of the added pixels depends on both the *color* and the *width* of the emitter segment.
    *   Example 1: Blue (1), Width 3 -> Offsets `(-2, -2), (-2, +2)` relative to center.
    *   Example 2: Green (3), Width 1 -> Offsets `(-3, -2), (-3, +2), (-2, -1), (-2, +1)` relative to center.
    *   Example 3: Yellow (4), Width 3 -> Offsets `(-3, -3), (-3, +3), (-2, -2), (-2, +2)` relative to center.
    *   Example 4: Yellow (4), Width 1 -> Offsets `(-2, -1), (-2, +1)` relative to center.
6.  **Output Grid:** The output grid retains all original pixels from the input grid and adds the newly generated pixels, potentially overwriting background (white) pixels.

## Facts


```yaml
task_description: Add new pixels based on properties of a specific horizontal segment ("emitter") found in the input.

element_definitions:
  - id: grid
    description: A 2D array of pixels with colors 0-9.
  - id: background
    description: Pixels with color 0 (white).
  - id: structure
    description: Contiguous block(s) of non-background pixels in the lower part of the grid.
  - id: emitter_segment
    description: >
      A horizontal, contiguous segment of pixels of a single color (C)
      where each pixel in the segment is located directly above a pixel
      of a different non-background color.
    properties:
      - color (C): The color of the emitter pixels.
      - position: Coordinates of the pixels forming the segment.
      - row (y_c): The row index of the segment.
      - center_col (x_c): The column index of the horizontal center of the segment.
      - width (W): The number of pixels in the segment.
  - id: generated_pixels
    description: >
      New pixels added to the output grid. Their color matches the emitter_segment color.
      Their positions are calculated relative to the emitter_segment's center (y_c, x_c).
    properties:
      - color: Same as emitter_segment color C.
      - relative_offsets: A set of (dy, dx) pairs specifying positions relative to (y_c, x_c).

relationships_and_rules:
  - rule: Find the emitter segment.
    details: >
      Scan the grid. Identify a horizontal segment of color C at row y,
      such that for each pixel (y, x) in the segment, the pixel (y+1, x) exists
      and has a non-background color different from C.
      Calculate its properties: color C, center (y_c, x_c), width W.
      (Assume y_c = y, and x_c is the average column index).
      Based on examples, there is only one such segment per input.
  - rule: Determine relative offsets based on emitter properties.
    details: >
      The set of relative offsets {(dy, dx)} depends on the emitter's color (C) and width (W).
      Observed patterns:
        - If C=1 (blue) and W=3: offsets = {(-2, -2), (-2, +2)}
        - If C=3 (green) and W=1: offsets = {(-3, -2), (-3, +2), (-2, -1), (-2, +1)}
        - If C=4 (yellow) and W=3: offsets = {(-3, -3), (-3, +3), (-2, -2), (-2, +2)}
        - If C=4 (yellow) and W=1: offsets = {(-2, -1), (-2, +1)}
  - rule: Generate output grid.
    details: >
      Start with a copy of the input grid.
      For each relative offset (dy, dx) determined by the emitter's properties:
        Calculate target coordinates: (y_target, x_target) = (y_c + dy, x_c + dx).
        If (y_target, x_target) is within the grid boundaries,
        set the pixel at (y_target, x_target) to the emitter's color C.

example_trace (train_1):
  - input_grid: 5x5 grid.
  - emitter_segment: Found at row 4, columns 1-3. Color=1 (blue). Width=3. Center=(4, 2). Pixels below (row 3) are magenta (6).
  - offsets_rule: C=1, W=3 => offsets = {(-2, -2), (-2, +2)}.
  - generated_pixels:
      - Offset (-2, -2): Target = (4-2, 2-2) = (2, 0). Color = 1 (blue).
      - Offset (-2, +2): Target = (4-2, 2+2) = (2, 4). Color = 1 (blue).
  - output_grid: Input grid + blue pixels at (2, 0) and (2, 4). Matches example output.

```


## Natural Language Program

1.  **Identify the Emitter Segment:**
    *   Scan the input grid row by row, from top to bottom.
    *   For each non-background pixel `(r, c)` with color `C`, check if the pixel directly below it, `(r+1, c)`, exists and has a non-background color different from `C`.
    *   If such a pixel is found, identify the full horizontal contiguous segment of color `C` at row `r` that includes `(r, c)`. This is the "emitter segment".
    *   Determine the emitter segment's color (`emitter_color`), its row index (`emitter_y`), its starting column (`emitter_x_min`), and its ending column (`emitter_x_max`).
2.  **Calculate Emitter Properties:**
    *   Calculate the width of the emitter segment: `emitter_width = emitter_x_max - emitter_x_min + 1`.
    *   Calculate the center column index of the emitter segment: `emitter_center_x = (emitter_x_min + emitter_x_max) / 2` (integer division or floor might be appropriate if width is even, though examples only show odd widths). Use `emitter_center_x = floor((emitter_x_min + emitter_x_max) / 2)`. Let the center coordinates be `(emitter_y, emitter_center_x)`.
3.  **Determine the Offset Pattern:**
    *   Based on the `emitter_color` and `emitter_width`, select the corresponding set of relative coordinate offsets `{(dy, dx)}`:
        *   If `emitter_color` is 1 (blue) and `emitter_width` is 3: use offsets `{(-2, -2), (-2, +2)}`.
        *   If `emitter_color` is 3 (green) and `emitter_width` is 1: use offsets `{(-3, -2), (-3, +2), (-2, -1), (-2, +1)}`.
        *   If `emitter_color` is 4 (yellow) and `emitter_width` is 3: use offsets `{(-3, -3), (-3, +3), (-2, -2), (-2, +2)}`.
        *   If `emitter_color` is 4 (yellow) and `emitter_width` is 1: use offsets `{(-2, -1), (-2, +1)}`.
        *   (Assume these are the only necessary combinations based on training data).
4.  **Create the Output Grid:**
    *   Initialize the output grid as a copy of the input grid.
    *   For each offset `(dy, dx)` in the selected set:
        *   Calculate the target coordinates: `target_y = emitter_y + dy`, `target_x = emitter_center_x + dx`.
        *   Check if the `target_y` and `target_x` are within the bounds of the grid dimensions.
        *   If they are within bounds, set the pixel at `(target_y, target_x)` in the output grid to the `emitter_color`.
5.  **Return the Output Grid.**