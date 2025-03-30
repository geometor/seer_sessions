Okay, let's break down the transformation logic for this task.

**Perception of Elements:**

1.  **Input Grid:** Contains a background of white pixels (0), several scattered gray pixels (5), and one contiguous shape of a primary color (green=3, blue=1, or yellow=4).
2.  **Output Grid:** Is identical to the input grid, except a new rectangular frame has been added.
3.  **Frame Color:** The color of the added frame matches the color of the primary shape in the input grid.
4.  **Frame Position:** The frame appears to be related to the positions of *all* non-white pixels (both the primary shape and the gray pixels). Specifically, it seems to be derived from the bounding box encompassing all these non-white pixels.
5.  **Frame Calculation:** Observing the examples, the frame isn't the exact bounding box of all non-white pixels. Instead, it looks like the bounding box of all non-white pixels is determined first, and then this box is shrunk inwards by one pixel from each side (top, bottom, left, right) to define the position of the final frame.
6.  **Drawing Rule:** The frame is drawn only by changing white pixels (0) to the primary shape's color along the perimeter of the calculated shrunk bounding box. Existing non-white pixels (the original shape, gray pixels) that fall on this perimeter are *not* overwritten; they retain their original color.

**YAML Facts:**


```yaml
task_description: "Draw a rectangular frame based on the spatial extent of all non-background pixels."
elements:
  - object: primary_shape
    description: "A single contiguous block of a non-white (0), non-gray (5) color."
    properties:
      - color: Varies (e.g., green=3, blue=1, yellow=4). Determines the frame color.
      - pixels: Coordinates of the shape's pixels.
  - object: gray_pixels
    description: "Multiple individual pixels of gray (5)."
    properties:
      - color: Always gray (5).
      - pixels: Coordinates of each gray pixel.
  - object: background
    description: "Pixels with white color (0)."
  - object: combined_non_white
    description: "The set of all pixels belonging to the primary_shape and gray_pixels."
    properties:
      - bounding_box: The minimum rectangle enclosing all these pixels [min_row, min_col, max_row, max_col].
  - object: target_frame
    description: "The rectangular frame to be drawn in the output."
    properties:
      - color: Same as the primary_shape color.
      - bounding_box: Derived by shrinking the combined_non_white bounding_box inwards by 1 pixel from each side [(min_row+1), (min_col+1), (max_row-1), (max_col-1)].
      - location: Drawn on the perimeter of its bounding_box.
actions:
  - action: find_all_non_white_pixels
    description: "Identify coordinates of all pixels that are not white (0)."
  - action: identify_primary_color
    description: "Find the color of the contiguous non-white, non-gray shape among the non-white pixels."
  - action: calculate_combined_bounding_box
    description: "Determine the minimum and maximum row and column indices for all non-white pixels."
  - action: calculate_shrunk_bounding_box
    description: "Calculate the frame's bounding box by adding 1 to min_row and min_col, and subtracting 1 from max_row and max_col of the combined bounding box."
  - action: draw_frame_perimeter
    description: "Iterate over the coordinates defining the perimeter of the shrunk_bounding_box. If a coordinate corresponds to a white (0) pixel in the input grid, change its color in the output grid to the primary_color. Otherwise, leave it unchanged."
relationships:
  - relationship: "The output grid starts as a copy of the input grid."
  - relationship: "The target_frame's color is determined by the primary_shape's color."
  - relationship: "The target_frame's position and size are derived from the bounding box of *all* non-white pixels (primary_shape + gray_pixels) after an inward shrinking operation."
  - relationship: "The drawing action modifies only background pixels on the target_frame's perimeter."
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the locations (row, column) of all non-white pixels in the input grid.
3.  From these non-white pixels, identify the contiguous shape that is not gray (color 5). Record the color of this shape (this is the `frame_color`).
4.  Determine the overall bounding box for *all* non-white pixels identified in step 2. Find the minimum row (`min_r`), maximum row (`max_r`), minimum column (`min_c`), and maximum column (`max_c`).
5.  Calculate the coordinates for the inner, shrunk frame:
    *   `frame_min_r = min_r + 1`
    *   `frame_max_r = max_r - 1`
    *   `frame_min_c = min_c + 1`
    *   `frame_max_c = max_c - 1`
6.  Iterate through the rows from `frame_min_r` to `frame_max_r`:
    *   Check the pixel at (`row`, `frame_min_c`) in the *input* grid. If it's white (0), set the pixel at (`row`, `frame_min_c`) in the *output* grid to `frame_color`.
    *   Check the pixel at (`row`, `frame_max_c`) in the *input* grid. If it's white (0), set the pixel at (`row`, `frame_max_c`) in the *output* grid to `frame_color`.
7.  Iterate through the columns from `frame_min_c + 1` to `frame_max_c - 1` (note the range excludes corners already processed):
    *   Check the pixel at (`frame_min_r`, `col`) in the *input* grid. If it's white (0), set the pixel at (`frame_min_r`, `col`) in the *output* grid to `frame_color`.
    *   Check the pixel at (`frame_max_r`, `col`) in the *input* grid. If it's white (0), set the pixel at (`frame_max_r`, `col`) in the *output* grid to `frame_color`.
8.  Return the modified output grid.