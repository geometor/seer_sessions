
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 4 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 8 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 0 0 0
0 0 0 3 3 4 4 0 0 0
0 0 0 8 8 6 6 0 0 0
0 0 0 8 8 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 2 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 7 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 2 0 0 0 0 0 0
0 0 7 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0 0 0 9 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
7 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 8 9 9 9 0 0 0
0 8 8 8 9 9 9 0 0 0
0 8 8 8 9 9 9 0 0 0
0 7 7 7 6 6 6 0 0 0
0 7 7 7 6 6 6 0 0 0
0 7 7 7 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task involves transforming an input grid containing a central gray rectangle and four distinctly colored single pixels located outside, near the corners of the rectangle, into an output grid. The output grid retains the dimensions of the input but replaces the gray rectangle's area with a pattern derived from the four corner pixels. Specifically, the area previously occupied by the gray rectangle is divided into four equal quadrants, and each quadrant is filled with the color of the corresponding nearby corner pixel. All original non-white pixels (the gray rectangle and the four corner pixels) are effectively removed or replaced, leaving only the newly colored quadrants on a white background.

**Facts:**


```yaml
task_description: Fill a rectangular area based on four corner color indicators.

elements:
  - type: grid
    properties:
      - dimensions: HxW (variable, <= 30x30)
      - background_color: white (0)

  - type: object
    name: gray_rectangle
    identifier: largest contiguous block of gray (5) pixels
    properties:
      - shape: rectangle
      - color: gray (5)
      - size: variable (always even dimensions H'xW')
      - location: centered or near-center
    relationships:
      - surrounded_by: four distinct color_pixels

  - type: object
    name: color_pixel
    identifier: single non-white (0), non-gray (5) pixels
    properties:
      - count: 4
      - colors: distinct (e.g., green, yellow, azure, magenta)
      - location: outside the gray_rectangle, one near each corner
    relationships:
      - correspond_to: corners of the gray_rectangle (top-left, top-right, bottom-left, bottom-right)

actions:
  - name: identify_gray_rectangle
    inputs: input_grid
    outputs: gray_rectangle_object (location, dimensions)

  - name: identify_corner_pixels
    inputs: input_grid, gray_rectangle_object
    outputs: four color_pixel objects (color, location) identified by relative position to the rectangle (TL, TR, BL, BR)
      - TL_pixel: row < rect_min_row, col < rect_min_col
      - TR_pixel: row < rect_min_row, col > rect_max_col
      - BL_pixel: row > rect_max_row, col < rect_min_col
      - BR_pixel: row > rect_max_row, col > rect_max_col

  - name: create_output_grid
    inputs: input_grid_dimensions
    outputs: empty_output_grid (filled with white 0)

  - name: divide_rectangle_area
    inputs: gray_rectangle_object
    outputs: four quadrant areas (top-left, top-right, bottom-left, bottom-right) within the rectangle's bounds. Each quadrant has dimensions (H'/2)x(W'/2).

  - name: fill_quadrants
    inputs: empty_output_grid, quadrant_areas, corner_pixels
    outputs: modified_output_grid
    process: Fill each quadrant area in the output grid with the color of the corresponding corner_pixel.
      - Top-left quadrant gets TL_pixel color.
      - Top-right quadrant gets TR_pixel color.
      - Bottom-left quadrant gets BL_pixel color.
      - Bottom-right quadrant gets BR_pixel color.

final_output: The modified_output_grid after filling all four quadrants.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but filled entirely with the background color (white, 0).
2.  Identify the largest contiguous rectangular object composed of gray (5) pixels in the input grid. Record its bounding box (minimum row, minimum column, maximum row, maximum column) and its dimensions (height H', width W').
3.  Find the four single-pixel objects in the input grid that are not white (0) and not gray (5).
4.  Assign each of these four pixels to a corner relative to the gray rectangle's bounding box:
    *   The pixel with row < minimum row and column < minimum column is the Top-Left (TL) corner pixel.
    *   The pixel with row < minimum row and column > maximum column is the Top-Right (TR) corner pixel.
    *   The pixel with row > maximum row and column < minimum column is the Bottom-Left (BL) corner pixel.
    *   The pixel with row > maximum row and column > maximum column is the Bottom-Right (BR) corner pixel.
    *   Record the color of each corner pixel.
5.  Calculate the midpoint row and column for dividing the gray rectangle's area: `mid_row = min_row + H'/2`, `mid_col = min_col + W'/2`.
6.  Fill the pixels in the output grid within the gray rectangle's original bounding box according to the following quadrant rules:
    *   For rows `r` from `min_row` to `mid_row - 1` and columns `c` from `min_col` to `mid_col - 1`, set the pixel `(r, c)` to the color of the TL corner pixel.
    *   For rows `r` from `min_row` to `mid_row - 1` and columns `c` from `mid_col` to `max_col`, set the pixel `(r, c)` to the color of the TR corner pixel.
    *   For rows `r` from `mid_row` to `max_row` and columns `c` from `min_col` to `mid_col - 1`, set the pixel `(r, c)` to the color of the BL corner pixel.
    *   For rows `r` from `mid_row` to `max_row` and columns `c` from `mid_col` to `max_col`, set the pixel `(r, c)` to the color of the BR corner pixel.
7.  Return the modified output grid.
