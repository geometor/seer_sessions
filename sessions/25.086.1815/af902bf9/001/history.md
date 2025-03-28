
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
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
0 0 0 4 0 4 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 2 2 2 2 0
0 0 0 0 4 0 0 0 0 4
```

*   **Perception:**
    The task involves identifying rectangular regions defined by specific markers in the input grid and filling the interior of these regions with a different color in the output grid.
    The input grids contain multiple yellow (4) pixels scattered on a white (0) background.
    These yellow pixels appear in groups of four, forming the corners of rectangles. There can be multiple such rectangles within a single input grid.
    The output grid retains the original yellow pixels and the white background but fills the area *strictly inside* the boundaries defined by each set of four yellow corner pixels with red (2) pixels.
    The size and location of the rectangles vary across examples. The area to be filled is the bounding box defined by the yellow corners, excluding the corners themselves.

*   **Facts:**
    
```yaml
    task_type: object_manipulation_filling
    elements:
      - color: white (0)
        role: background
      - color: yellow (4)
        role: marker
        property: appears in groups of four, defining rectangle corners
      - color: red (2)
        role: fill_color
        property: fills the interior of rectangles defined by yellow markers
    objects:
      - type: rectangle
        defined_by: four yellow (4) pixels at corners (r1, c1), (r1, c2), (r2, c1), (r2, c2)
        properties:
          - location: determined by yellow corner pixels
          - size: determined by yellow corner pixels
    actions:
      - action: find_rectangles
        input: yellow (4) pixels
        output: sets of four yellow pixels defining rectangle corners
      - action: fill_interior
        input: identified rectangles
        target_area: pixels (r, c) such that min_row < r < max_row and min_col < c < max_col for each rectangle
        fill_value: red (2)
    relationships:
      - The positions of the four yellow (4) pixels define the boundary of a rectangular area.
      - The red (2) pixels in the output correspond to the area strictly inside the boundaries defined by the yellow (4) pixels in the input.
      - Non-yellow and non-interior pixels remain unchanged between input and output.
    grid_properties:
      - size: constant between input and output (10x10 in examples)
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Find all locations of yellow (4) pixels in the input grid.
    3.  Identify all unique sets of four yellow pixels that form the corners of a rectangle. A set of four pixels at coordinates (r1, c1), (r1, c2), (r2, c1), and (r2, c2) forms a rectangle (where r1 != r2 and c1 != c2).
    4.  For each identified rectangle:
        a.  Determine the minimum and maximum row indices (min\_row, max\_row) and minimum and maximum column indices (min\_col, max\_col) from its four corner coordinates.
        b.  Iterate through all rows `r` from `min_row + 1` to `max_row - 1`.
        c.  Iterate through all columns `c` from `min_col + 1` to `max_col - 1`.
        d.  Set the pixel at location (r, c) in the output grid to red (2).
    5.  Return the modified output grid.
