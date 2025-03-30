
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 3 0 0 4 0 0 0 0 0
0 0 0 0 0 1 0 0 2 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 3 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 2 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 1 0 0 2 0 0 0 0
0 0 3 0 0 4 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 4 0 0 0 0
0 0 0 1 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 4 0 1 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input Structure:** The input grids consist of a white (0) background with one or more distinct 2x2 squares made of gray (5) pixels.
2.  **Output Structure:** The output grids are identical to the input grids, but with additional colored pixels placed around each gray square.
3.  **Key Transformation:** The core transformation involves identifying each 2x2 gray square and adding four specific colored pixels at precise locations relative to that square.
4.  **Added Pixels and Colors:** For every 2x2 gray square found in the input:
    *   A blue (1) pixel is added diagonally off the top-left corner.
    *   A red (2) pixel is added diagonally off the top-right corner.
    *   A green (3) pixel is added diagonally off the bottom-left corner.
    *   A yellow (4) pixel is added diagonally off the bottom-right corner.
5.  **Relative Positioning:** If the top-left pixel of a 2x2 gray square is at row `r` and column `c`, the new pixels are added at:
    *   Blue (1): `(r-1, c-1)`
    *   Red (2): `(r-1, c+2)`
    *   Green (3): `(r+2, c-1)`
    *   Yellow (4): `(r+2, c+2)`
6.  **Preservation:** The original gray squares and the background remain unchanged in the output grid, except where overwritten by the newly added colored pixels (though in the examples, the new pixels are always placed on the white background).

**YAML Fact Documentation:**


```yaml
task_description: "Identify each 2x2 gray square in the input grid and add four colored pixels (blue, red, green, yellow) at specific diagonal positions relative to the corners of each square."
objects:
  - object: background
    properties:
      color: white (0)
  - object: primary_shape
    type: square
    properties:
      color: gray (5)
      size: 2x2 pixels
      count: variable (one or more per input)
      location: various positions within the grid
  - object: added_pixels
    type: single pixel
    properties:
      color: [blue (1), red (2), green (3), yellow (4)]
      count: 4 per primary_shape instance
      location: fixed relative positions to the corners of a primary_shape
actions:
  - action: detect_shapes
    target: primary_shape (2x2 gray square)
    method: Iterate through the grid, checking for the 2x2 pattern of gray pixels. Record the top-left coordinate (r, c) of each detected square.
  - action: place_pixels
    target: output grid (copy of input grid)
    details: For each detected primary_shape at (r, c):
      - Place blue (1) at (r-1, c-1) if within grid bounds.
      - Place red (2) at (r-1, c+2) if within grid bounds.
      - Place green (3) at (r+2, c-1) if within grid bounds.
      - Place yellow (4) at (r+2, c+2) if within grid bounds.
relationships:
  - type: spatial_relative
    description: The locations of the added_pixels are defined relative to the coordinates of the corners of each primary_shape.
    details:
      - blue is top-left diagonal (-1 row, -1 col from top-left corner)
      - red is top-right diagonal (-1 row, +1 col from top-right corner, or r-1, c+2 from top-left)
      - green is bottom-left diagonal (+1 row, -1 col from bottom-left corner, or r+2, c-1 from top-left)
      - yellow is bottom-right diagonal (+1 row, +1 col from bottom-right corner, or r+2, c+2 from top-left)
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each possible top-left corner position `(r, c)` in the input grid, ensuring that checking `(r, c)`, `(r+1, c)`, `(r, c+1)`, and `(r+1, c+1)` stays within the grid boundaries.
3.  For each position `(r, c)`, check if it marks the top-left corner of a 2x2 gray (5) square. This means checking if `input[r, c]`, `input[r+1, c]`, `input[r, c+1]`, and `input[r+1, c+1]` are all equal to 5.
4.  If a 2x2 gray square is found starting at `(r, c)`:
    a.  Calculate the position `(r-1, c-1)`. If this position is within the grid boundaries, change the pixel at this position in the output grid to blue (1).
    b.  Calculate the position `(r-1, c+2)`. If this position is within the grid boundaries, change the pixel at this position in the output grid to red (2).
    c.  Calculate the position `(r+2, c-1)`. If this position is within the grid boundaries, change the pixel at this position in the output grid to green (3).
    d.  Calculate the position `(r+2, c+2)`. If this position is within the grid boundaries, change the pixel at this position in the output grid to yellow (4).
5.  After checking all possible top-left corners, return the modified output grid.
