## Perception

The input grids contain one or more hollow rectangular frames drawn with a single non-white color on a white background. The frames observed in the examples are one pixel thick. The output grid is the same size as the input grid. The transformation modifies the area enclosed by these frames based on the size of the frame.

1.  **train_1:**
    *   Input: A 7x7 grid with a single 5x5 green frame.
    *   Output: The 5x5 green frame remains, and the single pixel at the geometric center of the hollow area inside the frame is changed from white to green.
2.  **train_2:**
    *   Input: A 10x10 grid with two yellow frames: a 3x3 frame and a 5x5 frame.
    *   Output: The 3x3 frame in the input is completely filled with yellow in the output. The 5x5 yellow frame remains, and the single pixel at the geometric center of its hollow area is changed from white to yellow.

**Key Observations:**
*   The task involves identifying hollow rectangular frames of a single color.
*   The modification depends on the size of the frame.
*   For 3x3 frames, the entire frame area (including the hollow interior) is filled with the frame's color.
*   For frames larger than 3x3 (specifically 5x5 in the examples), only the centermost pixel of the hollow interior region is filled with the frame's color.
*   The background color (white) and the frame pixels themselves (except when filling a 3x3 frame) are unchanged.

## Facts


```yaml
task_type: object_manipulation
grid_properties:
  size: variable (input and output sizes are identical for each example)
  background_color: white (0)

objects:
  - type: frame
    properties:
      shape: hollow_rectangle
      thickness: 1 pixel
      color: non-white (green=3, yellow=4 in examples)
      size: variable (3x3, 5x5 in examples)
    relationship: surrounds an area of background color

actions:
  - name: fill_center
    target: frame
    condition: frame size > 3x3
    effect: changes the color of the centermost pixel of the hollow interior area to the frame's color
  - name: fill_all
    target: frame
    condition: frame size == 3x3
    effect: changes the color of all pixels within the frame's bounding box (frame and interior) to the frame's color

transformation_logic:
  - Identify all hollow rectangular frames (1 pixel thick, single non-white color).
  - For each identified frame:
    - If the frame's outer dimension is 3x3, apply the 'fill_all' action.
    - If the frame's outer dimension is greater than 3x3, apply the 'fill_center' action.
  - Pixels not part of identified frames or their modified interiors remain unchanged.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to identify all hollow rectangular frames. A hollow rectangular frame is defined as a rectangular border, one pixel thick, made of a single non-white color, surrounding a rectangular area composed entirely of the background color (white).
3.  For each identified hollow rectangular frame:
    a.  Determine the outer dimensions (height and width) of the frame.
    b.  If the dimensions are 3x3:
        i.  Identify the top-left corner coordinates (row, col) of the 3x3 frame.
        ii. Iterate through all pixels within the 3x3 area defined by (row, col) to (row+2, col+2).
        iii. Change the color of each pixel in this 3x3 area in the output grid to the color of the frame.
    c.  If the dimensions are greater than 3x3:
        i.  Identify the bounding box of the hollow interior region (the white area inside the frame).
        ii. Calculate the coordinates (center_row, center_col) of the geometric center of this interior region. For an interior region with height `h` starting at `r` and width `w` starting at `c`, the center is `(r + floor((h-1)/2), c + floor((w-1)/2))`.
        iii. Change the color of the pixel at (center_row, center_col) in the output grid to the color of the frame.
4.  Return the modified output grid.