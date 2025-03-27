**Perception**

1.  **Background Color:** All examples consistently use azure (8) as the background color, filling most of the grid.
2.  **Input Object:** Each input grid contains exactly one pixel that is *not* the background color. This single pixel acts as the key element determining the transformation. The color of this pixel varies (yellow, maroon, magenta).
3.  **Output Object:** The output grid is the same size as the input grid and retains the azure (8) background. A solid rectangle, colored the same as the unique input pixel, is drawn in one of the four corners of the output grid.
4.  **Transformation Logic:** The position of the single unique pixel in the input grid determines both the *location* (which corner) and the *size* (height and width) of the rectangle in the output grid.
5.  **Quadrant Calculation:** The position (R, C) of the unique input pixel effectively divides the grid into four quadrants relative to that pixel. The dimensions of these quadrants are:
    *   Top-Left: (R+1) x (C+1)
    *   Top-Right: (R+1) x (Grid Width - C)
    *   Bottom-Left: (Grid Height - R) x (C+1)
    *   Bottom-Right: (Grid Height - R) x (Grid Width - C)
6.  **Smallest Quadrant Rule:** The transformation identifies the quadrant with the *smallest area* among these four. The output rectangle's color, corner location, and dimensions correspond to this smallest quadrant.

**Facts**


```yaml
task_context:
  description: Transforms a grid based on the position of a single unique pixel.
  grid_properties:
    background_color: 8 # azure
    content: Contains a single pixel of a non-background color.

input_elements:
  - object: unique_pixel
    properties:
      color: Any color except the background_color (e.g., 4, 9, 6).
      location: Defined by its row (R) and column (C).
      count: Exactly one per input grid.

output_elements:
  - object: corner_rectangle
    properties:
      color: Same as the unique_pixel color from the input.
      shape: Solid rectangle.
      location: Positioned in one of the four corners (top-left, top-right, bottom-left, bottom-right) of the output grid.
      size: Height and width determined by the calculation based on the unique_pixel's location.

transformation:
  rule: Find the smallest area quadrant defined by the unique pixel's location and fill the corresponding corner of the output grid with a rectangle of that quadrant's dimensions and the unique pixel's color.
  details:
    - Identify the unique_pixel (color P_Color, row R, column C) and grid dimensions (Height H, Width W).
    - Calculate areas of four potential rectangles (quadrants):
        - area_TL: (R + 1) * (C + 1)
        - area_TR: (R + 1) * (W - C)
        - area_BL: (H - R) * (C + 1)
        - area_BR: (H - R) * (W - C)
    - Find the minimum area among area_TL, area_TR, area_BL, area_BR.
    - Determine the corner and dimensions (Rect_H, Rect_W) corresponding to the minimum area.
    - Create an output grid of size H x W, filled with the background_color.
    - Fill the determined corner region with a rectangle of size Rect_H x Rect_W using P_Color.
```


**Natural Language Program**

1.  Initialize the output grid to be the same dimensions as the input grid and fill it entirely with the background color, azure (8).
2.  Scan the input grid to find the single pixel that is not azure (8). Record its color (`source_color`) and its location (row `R`, column `C`).
3.  Get the height (`H`) and width (`W`) of the grid.
4.  Calculate the dimensions and areas of the four rectangular regions (quadrants) defined by the pixel at (`R`, `C`):
    *   `top_left_dims` = (`R` + 1, `C` + 1), `area_TL` = (`R` + 1) * (`C` + 1)
    *   `top_right_dims` = (`R` + 1, `W` - `C`), `area_TR` = (`R` + 1) * (`W` - `C`)
    *   `bottom_left_dims` = (`H` - `R`, `C` + 1), `area_BL` = (`H` - `R`) * (`C` + 1)
    *   `bottom_right_dims` = (`H` - `R`, `W` - `C`), `area_BR` = (`H` - `R`) * (`W` - `C`)
5.  Identify which of the four areas (`area_TL`, `area_TR`, `area_BL`, `area_BR`) is the smallest.
6.  Based on the smallest area, determine the target corner and the dimensions (`target_height`, `target_width`) for the output rectangle:
    *   If `area_TL` is smallest: Target corner is top-left, (`target_height`, `target_width`) = `top_left_dims`.
    *   If `area_TR` is smallest: Target corner is top-right, (`target_height`, `target_width`) = `top_right_dims`.
    *   If `area_BL` is smallest: Target corner is bottom-left, (`target_height`, `target_width`) = `bottom_left_dims`.
    *   If `area_BR` is smallest: Target corner is bottom-right, (`target_height`, `target_width`) = `bottom_right_dims`.
    *   (Note: Handle potential ties, although not present in examples, consistently choosing one, e.g., TL > TR > BL > BR priority).
7.  Fill the pixels in the target corner of the output grid with the `source_color`. The region to fill starts at row 0 for top corners or row `H - target_height` for bottom corners, and column 0 for left corners or column `W - target_width` for right corners, extending for `target_height` rows and `target_width` columns.