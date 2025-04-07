## Perception

The input grids contain a dominant background color. Upon this background, there are several hollow rectangular frames, each made of a single distinct color. Additionally, there are scattered pixels of various colors ("noise") that are not part of the background or the rectangular frames.

The transformation involves two main steps:
1.  **Noise Removal:** All pixels that are neither the background color nor part of a hollow rectangular frame are removed (replaced with the background color).
2.  **Frame Modification:** Pixels are added inside each hollow rectangular frame. Specifically, along the horizontal line that vertically bisects the frame, pixels are colored with the frame's color in an alternating pattern, starting from the second column inside the frame's boundary.

## Facts


```yaml
Observations:
  - Input contains a background color, hollow rectangular frames, and noise pixels.
  - Output contains the background color and modified frames, with noise removed.

Background:
  - Property: The most frequent color in the input grid.
  - Role: Fills the space not occupied by frames or noise in the input, and replaces noise in the output.

Objects:
  - Type: Hollow Rectangular Frame
    - Properties:
      - Composed of a single, non-background color.
      - Forms the perimeter of a rectangle.
      - Has a bounding box (min_row, max_row, min_col, max_col).
      - Has a specific color.
    - Actions:
      - Identified in the input.
      - Preserved in the output.
      - Modified internally in the output.
  - Type: Noise Pixel
    - Properties:
      - Any color different from the background.
      - Not part of a contiguous hollow rectangular frame structure.
    - Actions:
      - Identified in the input.
      - Removed in the output (replaced by background color).

Transformations:
  - Noise Removal:
    - Condition: Pixel is not background color AND not part of any identified frame.
    - Action: Change pixel color to background color.
  - Frame Modification (Dot Insertion):
    - For each frame:
      - Target Row: The middle row of the frame's bounding box (`mid_row = (min_row + max_row) // 2`).
      - Target Columns: Columns strictly inside the frame's left and right boundaries (`min_col + 1` to `max_col - 1`).
      - Pattern: Color pixels at `(mid_row, col)` with the frame's color if the column index `col` is odd relative to the first *internal* column (`(col - (min_col + 1)) % 2 != 0`).

Relationships:
  - Frames are distinct objects on the background.
  - Noise pixels are separate from frames and background.
  - The modification pattern inside a frame depends on its bounding box dimensions and color.
```


## Natural Language Program

1.  Determine the background color by identifying the most frequent pixel color in the input grid.
2.  Identify all hollow rectangular frames in the input grid. For each frame, record its color and its bounding box coordinates (minimum row, maximum row, minimum column, maximum column). A frame is a connected perimeter of a single non-background color forming a rectangle.
3.  Create a new grid (the output grid) as a copy of the input grid.
4.  Iterate through each pixel `(r, c)` of the input grid. If the color of the pixel `input[r, c]` is not the background color AND the pixel `(r, c)` is not part of any identified rectangular frame's perimeter, change the corresponding pixel in the output grid `output[r, c]` to the background color.
5.  For each identified rectangular frame with color `C` and bounding box `min_r, max_r, min_c, max_c`:
    a. Calculate the middle row index: `mid_row = floor((min_r + max_r) / 2)`.
    b. Define the starting internal column index: `start_internal_col = min_c + 1`.
    c. Iterate through the columns `col` from `start_internal_col` to `max_c - 1`.
    d. If the column index `col` relative to the `start_internal_col` is odd (i.e., `(col - start_internal_col)` is odd, or equivalently `(col - start_internal_col) % 2 != 0`), set the pixel in the output grid at `output[mid_row, col]` to the frame's color `C`.
6.  Return the modified output grid.