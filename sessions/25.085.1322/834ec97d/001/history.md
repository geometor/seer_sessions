
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
4 0 4 0 4
4 0 4 0 4
4 0 4 0 4
0 0 6 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 2 0
0 0 0
0 0 0
```


**output:**
```
0 4 0
0 2 0
0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

### Perception

1.  **Input Structure:** Each input grid contains a single non-white pixel (the "object") on a white background. The grid sizes and the object's color and position vary.
2.  **Output Structure:** Each output grid has the same dimensions as the corresponding input.
3.  **Object Transformation:** The original non-white pixel appears in the output grid, but shifted one row down from its input position.
4.  **Pattern Generation:** A distinct pattern appears in the output grid. This pattern consists of alternating yellow (4) and white (0) pixels filling entire rows.
5.  **Pattern Location:** The pattern fills all rows from the top of the grid down to and including the original row where the non-white pixel was located in the input.
6.  **Pattern Detail:** The specific alternating pattern (`4 0 4 0...` or `0 4 0 4...`) applied to the rows depends on the column index of the original non-white pixel. If the column index is even, the pattern starts with yellow (4). If the column index is odd, the pattern starts with white (0).
7.  **Overlap:** The non-white pixel, in its new position (one row below its original), overwrites any part of the generated pattern that might occupy the same cell. Rows below the new position of the non-white pixel remain white.

### Facts


```yaml
elements:
  - role: background
    type: grid
    color: white (0)
  - role: object
    type: pixel
    count: 1
    properties:
      color: non-white (varies, e.g., magenta(6), red(2), maroon(9))
      location: (row_in, col_in)
  - role: pattern
    type: grid_fill
    properties:
      colors: [yellow (4), white (0)]
      structure: alternating horizontally
      start_color_rule:
        - if: col_in is even
          then: yellow (4)
        - if: col_in is odd
          then: white (0)
      location: rows 0 to row_in (inclusive) in the output grid

transformation:
  - action: identify_object
    input: input_grid
    output: object_color, (row_in, col_in)
  - action: initialize_output
    input: input_grid_dimensions
    output: output_grid (filled with white)
  - action: determine_pattern_start
    input: col_in
    output: pattern_start_color (yellow or white)
  - action: apply_pattern
    input: output_grid, pattern_start_color, row_in
    modifies: output_grid rows 0 to row_in
    details: Fill rows 0..row_in with alternating pattern starting with pattern_start_color.
  - action: move_object
    input: output_grid, object_color, (row_in, col_in)
    modifies: output_grid
    details: Place object_color at (row_in + 1, col_in), overwriting existing pixel if necessary. Ensure target location is within grid bounds.

output:
  - grid: output_grid after all transformations
```


### Natural Language Program

1.  Identify the single non-white pixel in the input grid. Record its color and its location (input row `r`, input column `c`).
2.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with white (0).
3.  Determine the starting color for an alternating pattern: if the input column `c` is even, the pattern starts with yellow (4); if `c` is odd, the pattern starts with white (0).
4.  Fill each row `i` of the output grid, from row 0 up to and including the input row `r`, with the alternating pattern determined in step 3 (e.g., `4 0 4 0...` or `0 4 0 4...`).
5.  Place the original non-white pixel (identified in step 1) into the output grid at location (`r + 1`, `c`), overwriting the pixel currently at that position. This step should only be performed if `r + 1` is a valid row index within the grid boundaries.
