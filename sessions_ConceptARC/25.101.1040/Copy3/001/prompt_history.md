
## train_1

**input:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 1 0 1 0 1 0 0 1 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 3 3 3 3 3 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 0 0 7 0 0 0 0
4 0 0 0 0 0 0 0 7 0 0 0 0
0 4 0 0 0 0 0 0 7 0 0 0 0
0 0 6 6 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 3 0 7 0 0 0 0
4 0 0 0 0 0 3 4 7 0 0 0 0
0 4 0 0 0 0 3 0 7 0 0 0 0
0 0 6 6 0 0 3 4 7 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

## Perception

1.  **Grid Structure**: Both examples involve transforming a grid into another grid of the *same dimensions*.
2.  **Example 1 (train_1)**:
    *   The input grid has a width of 16 (even).
    *   Various patterns (yellow 'L' shapes, a blue dotted line, a green bar, small yellow dots/lines) exist, mostly concentrated on the left half (columns 0-7).
    *   The output grid appears to be created by taking the left half of the input grid (columns 0-7) and copying it onto the right half (columns 8-15), overwriting the original content of the right half. The left half remains unchanged.
3.  **Example 2 (train_2)**:
    *   The input grid has a width of 13 (odd).
    *   It contains several distinct objects/patterns: magenta rectangles, a complex shape made of green, yellow, and orange pixels ('Object A') on the left, and scattered orange pixels and magenta rectangles on the right.
    *   The output grid shows that 'Object A' from the left side (specifically, the content within the bounding box from row 2, col 0 to row 7, col 2) has been copied to a new location starting at row 5, col 6.
    *   The original content at the destination location (mostly white space, but including some orange pixels) is overwritten by the copied pattern. Other elements, like the magenta rectangles, remain in their original positions.
4.  **Key Difference**: The transformation logic seems to differ based on some property of the input grid. In train_1 (even width, no magenta), a simple half-grid copy occurs. In train_2 (odd width, contains magenta), a specific complex pattern is identified and copied to a location possibly determined by a magenta marker object. The copy destination in train_2 appears related to the magenta `6 6` block at (3, 6) in the input, with the copy starting 2 rows below it.

## Facts


```yaml
task_description: Copy patterns within the grid based on grid properties or specific markers.

example_1:
  input_grid_properties:
    height: 11
    width: 16
    colors_present: [white, yellow, blue, green]
    contains_magenta: false
  objects:
    - id: left_half
      description: Columns 0 through 7 of the grid.
      contains_patterns: [yellow_L_top, blue_dotted_line, green_bar, misc_yellow]
    - id: right_half
      description: Columns 8 through 15 of the grid.
      contains_patterns: [yellow_L_top, empty_space]
  action:
    type: copy
    source: left_half
    destination: right_half
    overwrite: true
  output_grid_properties:
    identical_dimensions: true
    content: Left half is unchanged, right half is identical to the left half.

example_2:
  input_grid_properties:
    height: 15
    width: 13
    colors_present: [white, magenta, green, orange, yellow]
    contains_magenta: true
  objects:
    - id: pattern_A
      description: Complex pattern composed of green, yellow, orange pixels.
      location: Bounding box (rows 2-7, cols 0-2)
    - id: marker_1
      description: Magenta 1x2 rectangle
      location: (0, 0)
    - id: marker_2
      description: Magenta 1x2 rectangle
      location: (3, 6) # Seems relevant for destination
    - id: marker_3
      description: Magenta 1x2 rectangle
      location: (8, 2)
    - id: marker_4
      description: Magenta 1x2 rectangle
      location: (11, 8)
    - id: other_pixels
      description: Scattered orange pixels on the right side.
  action:
    type: copy
    source: pattern_A (content of its bounding box)
    destination_anchor: marker_2 at (3, 6)
    destination_top_left: Calculated as (marker_2.row + 2, marker_2.col) = (5, 6)
    overwrite: true
  output_grid_properties:
    identical_dimensions: true
    content: pattern_A is copied starting at (5, 6), overwriting original content. Other markers and pixels remain unchanged.

general_rule_hypothesis:
  condition: Check if magenta (color 6) is present in the input grid.
  case_no_magenta:
    condition: Grid width W is even. (Assumption based on example 1)
    action: Copy columns 0 to W/2 - 1 to columns W/2 to W - 1.
  case_magenta_present:
    condition: Grid width W is odd. (Assumption based on example 2)
    action:
      1. Identify the largest connected component group containing colors other than white and magenta ('source pattern'). Get its bounding box.
      2. Identify potential 'marker' objects (magenta rectangles/pixels).
      3. Select the relevant marker (e.g., based on proximity below/after the source pattern). Let its top-left be (r_mark, c_mark).
      4. Calculate the destination top-left as (r_mark + 2, c_mark).
      5. Copy the source pattern (content of its bounding box) to the calculated destination.
```


## Natural Language Program

1.  Examine the input grid to determine if any pixels have the color magenta (6).
2.  **If no magenta pixels are present**:
    a. Determine the width `W` of the grid.
    b. Define the left half of the grid as columns from 0 to `W/2 - 1`.
    c. Define the right half of the grid as columns from `W/2` to `W - 1`.
    d. Create the output grid by copying the input grid.
    e. For each row `r` from 0 to `height - 1`:
        i. For each column `c` from 0 to `W/2 - 1`:
            - Set the pixel value at `(r, c + W/2)` in the output grid to the value of the pixel at `(r, c)` in the input grid.
3.  **If magenta pixels are present**:
    a. Identify all connected components of non-white pixels. Find the component `P` that is the "main pattern" (heuristic: largest bounding box area containing non-magenta colors, as seen in example 2). Determine the bounding box of `P`: `(min_row_P, min_col_P)` to `(max_row_P, max_col_P)`.
    b. Identify all magenta objects/pixels. Find the specific "marker" magenta object `M` (heuristic: the top-most magenta object whose column is greater than `max_col_P` and whose row is closest to `min_row_P`, as seen in example 2). Let the top-left corner of `M` be `(row_M, col_M)`.
    c. Calculate the destination top-left corner `(dest_row, dest_col)` as `(row_M + 2, col_M)`.
    d. Create the output grid by copying the input grid.
    e. Iterate through the pixels within the bounding box of the source pattern `P`. For each source pixel at `(r_src, c_src)` within the bounding box (where `r_src` ranges from `min_row_P` to `max_row_P`, and `c_src` ranges from `min_col_P` to `max_col_P`):
        i. Calculate the corresponding destination coordinates: `(r_dest, c_dest) = (dest_row + (r_src - min_row_P), dest_col + (c_src - min_col_P))`.
        ii. If `(r_dest, c_dest)` is within the grid boundaries, set the pixel value at `(r_dest, c_dest)` in the output grid to the value of the pixel at `(r_src, c_src)` in the input grid.
4.  Return the modified output grid.
