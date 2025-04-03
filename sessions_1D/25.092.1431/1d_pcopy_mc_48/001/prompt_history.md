
## train_1

**input:**
```
0 0 7 7 7 0 0 6 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 6 6 6 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 6 6 6 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 1 0 0 0 0 8 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 1 1 1 0 0 0 8 8 8 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output are grids of the same dimensions. The background is white (0) and remains unchanged.
The task involves identifying specific patterns of colored pixels in the input and modifying them in the output.
Two types of patterns are relevant:
1.  Single, isolated colored pixels (dots).
2.  Horizontal lines consisting of exactly three consecutive pixels of the same color.

Observations across examples:
-   Horizontal lines of length 3 present in the input are preserved in the output at the same location and with the same color. (e.g., `777` in train_1, `666` in train_2, `111` in train_3).
-   Single colored pixels (dots) in the input are transformed into horizontal lines of length 3 in the output. The line has the same color as the original dot and is centered horizontally at the column where the dot was located. (e.g., the magenta `6` at col 7 in train_1 becomes `666` at cols 6, 7, 8; the green `3` at col 6 in train_2 becomes `333` at cols 5, 6, 7; the azure `8` at col 8 in train_3 becomes `888` at cols 7, 8, 9).
-   The transformations seem to happen independently for each identified pattern. The row of the transformation is the same as the row of the original pattern.

## Facts


```yaml
grid_properties:
  - background_color: 0  # white
  - dimensions_preserved: True

elements:
  - type: pixel
    properties:
      - color: Integer (0-9)
      - position: (row, column)

objects:
  - type: dot
    definition: A single non-white pixel with no horizontal neighbors of the same color.
    properties:
      - color: C (non-white)
      - position: (r, c)
  - type: h_line_3
    definition: A horizontal sequence of exactly 3 contiguous pixels of the same non-white color.
    properties:
      - color: C (non-white)
      - position: spans from (r, c) to (r, c+2)

transformations:
  - object: dot
    action: expand_horizontally
    details: Replace the dot at (r, c) with a horizontal line of the same color, spanning columns c-1, c, and c+1 (within grid bounds) on the same row r.
  - object: h_line_3
    action: copy
    details: Keep the line unchanged in the output grid at the same position and with the same color.
  - object: background / other pixels
    action: copy
    details: Keep white pixels and any other non-white pixels not matching 'dot' or 'h_line_3' definitions unchanged.

processing_order:
  - Initialize the output grid as a copy of the input grid.
  - Identify all 'dots' in the input grid.
  - For each identified 'dot' at input position (r, c) with color C:
      - Modify the output grid by setting pixels (r, c-1), (r, c), and (r, c+1) to color C, ensuring column indices stay within grid boundaries.
```


## Natural Language Program

1.  Create a new grid (output) identical to the input grid.
2.  Iterate through each pixel of the input grid at position (row `r`, column `c`).
3.  Let `C` be the color of the pixel `input[r, c]`.
4.  If `C` is not white (0):
    a.  Check if the pixel at `(r, c)` is horizontally isolated (i.e., it's a 'dot'). A pixel is horizontally isolated if its left neighbor (`input[r, c-1]`, if `c>0`) and its right neighbor (`input[r, c+1]`, if `c < width-1`) are not also color `C`.
    b.  If the pixel `(r, c)` is horizontally isolated:
        i.  Set the color of the pixel at `(r, c)` in the output grid to `C`.
        ii. Set the color of the pixel at `(r, c-1)` in the output grid to `C`, if `c > 0`.
        iii. Set the color of the pixel at `(r, c+1)` in the output grid to `C`, if `c < width - 1`.
5.  All other pixels (white pixels and non-white pixels that are part of horizontal structures longer than a single pixel) retain their original color from the initial copy.
6.  Return the modified output grid.
