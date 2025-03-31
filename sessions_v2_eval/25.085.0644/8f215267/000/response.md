**Perception**

The task involves transforming input grids containing various colored shapes and pixels into output grids. Each input grid features a dominant background color, several hollow rectangles constructed from a single color different from the background, and some scattered pixels ("noise") of various colors.

The transformation rule appears to operate primarily on the hollow rectangles. The core logic involves:
1.  Identifying the background color.
2.  Identifying the hollow rectangular structures. Each rectangle is defined by a single-pixel thick border of a specific color, enclosing an area filled solely with the background color.
3.  Identifying and discarding any other non-background pixels (noise) that are not part of these hollow rectangles.
4.  Modifying the interior of each identified hollow rectangle. Specifically, pixels along the horizontal midline of the rectangle's *internal* area are selectively colored with the rectangle's border color.
5.  The selection criteria for coloring pixels on the midline depend on the parity (odd or even) of the background color's numerical value. If the background color value is odd, pixels at *odd* absolute column indices on the midline are colored. If the background color value is even, pixels at *even* absolute column indices on the midline are colored.
6.  The final output grid consists of the original background color, the intact hollow rectangle borders, and the newly colored pixels within the rectangles' midlines.

**Facts**


```yaml
elements:
  - object: grid
    attributes:
      - height: integer
      - width: integer
      - pixels: 2D array of color values

  - object: background
    attributes:
      - color: integer (most frequent color in the input grid)
      - parity: derived from color value (odd or even)

  - object: hollow_rectangle
    attributes:
      - color: integer (color of the border pixels)
      - border_pixels: list of coordinates [(row, col), ...]
      - bounding_box: (min_row, min_col, max_row, max_col)
      - internal_area: region inside the border, initially filled with background color
      - internal_midline_row: integer (row index of the horizontal middle of the internal_area)
      - internal_columns: range of column indices for the internal_area

  - object: noise_pixel
    attributes:
      - color: integer
      - position: (row, col)
    notes: Any pixel that is not part of the background or a hollow_rectangle border.

relationships:
  - type: spatial
    description: hollow_rectangles enclose an internal_area filled with the background color.
  - type: identification
    description: noise_pixels are identified by not belonging to the background or a hollow_rectangle.

actions:
  - action: identify_background
    inputs: input_grid
    outputs: background_color, background_parity
    description: Determine the most frequent color and its parity.

  - action: find_hollow_rectangles
    inputs: input_grid, background_color
    outputs: list of hollow_rectangle objects
    description: Locate connected components of non-background colors that form a single-pixel thick rectangular border around an area filled only with background_color.

  - action: filter_noise
    inputs: input_grid, background_color, list of hollow_rectangles
    outputs: None (implicitly removes noise during output construction)
    description: Identify pixels that are neither background nor part of a hollow_rectangle border.

  - action: apply_midline_pattern
    inputs: hollow_rectangle, background_parity
    outputs: list of coordinates and colors for new pixels
    description: >
      Calculate the internal_midline_row and internal_columns for the rectangle.
      Iterate through the absolute column indices corresponding to the internal_columns.
      For each pixel position (internal_midline_row, col_index), check if the parity of col_index matches the background_parity.
      If it matches, mark this position to be colored with the hollow_rectangle's color.

  - action: construct_output
    inputs: input_grid_dimensions, background_color, list of hollow_rectangles, list of new pattern pixels
    outputs: output_grid
    description: >
      Create a new grid filled with background_color.
      Draw the border_pixels of each hollow_rectangle onto the grid.
      Draw the new pattern pixels (from apply_midline_pattern) onto the grid.
```


**Natural Language Program**

1.  **Initialize Output:** Create a new grid with the same dimensions as the input grid.
2.  **Identify Background:** Determine the most frequent color in the input grid. This is the `background_color`. Fill the new output grid completely with this `background_color`. Determine the `background_parity` (odd or even) based on the numerical value of the `background_color`.
3.  **Find Hollow Rectangles:**
    *   Iterate through the input grid to find connected components (objects) made of pixels that are not the `background_color`.
    *   For each component, verify if it constitutes a "hollow rectangle":
        *   It must have a single, consistent color (`rectangle_color`).
        *   Its pixels must form a single-pixel-thick rectangular border.
        *   The area enclosed strictly within this border must consist *only* of pixels matching the `background_color` in the input grid.
    *   Keep a list of all valid hollow rectangles found, storing their `rectangle_color`, border pixel locations, and bounding boxes.
4.  **Draw Rectangle Borders:** For each identified hollow rectangle, draw its border pixels onto the output grid using its `rectangle_color`.
5.  **Apply Midline Pattern:** For each identified hollow rectangle:
    *   Determine the row index of the horizontal midline of its *internal* area (the area inside the border). If the internal height is odd, there's one midline row. (The examples only show odd internal heights).
    *   Identify the range of column indices belonging to the internal area.
    *   Iterate through the absolute column indices within this internal range.
    *   For each column index `col` on the midline row:
        *   Check if the parity of `col` (odd or even) matches the `background_parity`.
        *   If the parities match, change the color of the pixel at (midline_row, `col`) in the output grid to the `rectangle_color`.
6.  **Return Output:** The final modified output grid is the result.