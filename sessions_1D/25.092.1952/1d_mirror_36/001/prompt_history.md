
## train_1

**input:**
```
0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 4 4 4 4 4 4 4 0
```


## train_2

**input:**
```
0 0 7 7 7 7 7 7 7 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 0 7 7 7 7 7 7 7 0 0 0 0 0
```


## train_3

**input:**
```
6 6 6 6 6 6 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 6 6 6 6 6 6 0 0 0 0 0
```

*   **Perception:**
    *   The task operates on 1-dimensional grids (represented as single rows).
    *   Each input grid contains three distinct elements: a background of white pixels (0), a single maroon pixel (9), and a single contiguous horizontal line of another uniform color (yellow, orange, or magenta in the examples).
    *   The maroon pixel acts as a fixed anchor point; its position remains unchanged between the input and output grids.
    *   The colored horizontal line object moves its position relative to the maroon pixel. It is always to the left of the maroon pixel in the input and always to the right in the output.
    *   The transformation rule calculates the new starting position of the colored line based on its original position relative to the maroon pixel and whether the original line crossed the vertical center of the grid.
    *   The length and color of the moving line object are preserved in the output.
    *   The distance (number of pixels) between the end of the line and the maroon pixel in the input (`dist_in`) determines the distance between the maroon pixel and the start of the line in the output (`dist_out`).
    *   Specifically, `dist_out` equals `dist_in` unless the input line crosses the grid's center, in which case `dist_out = dist_in + 1`.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1 # Effectively 1D grids (single row)
    background_color: 0 # white
    objects:
      - id: anchor
        color: 9 # maroon
        count: 1
        shape: pixel
        properties:
          - position is constant between input and output
      - id: mover
        color: any except 0 or 9
        count: 1
        shape: horizontal_line
        properties:
          - contiguous
          - uniform_color
        actions:
          - moves position relative to anchor
    relationships:
      - type: relative_positioning
        object1: mover
        object2: anchor
        input_state: mover is to the left of anchor
        output_state: mover is to the right of anchor
      - type: spatial_calculation
        name: input_distance
        value: anchor.position - mover.end_position
        variable_name: dist_in
      - type: grid_property_check
        name: center_crossing
        object: mover
        details: Checks if the interval [mover.start_position, mover.end_position] includes the grid's center index/indices. For width W, center is floor(W/2) if W is odd, or indices W/2-1 and W/2 if W is even.
        variable_name: crosses_center
      - type: spatial_calculation
        name: output_distance
        value: "dist_in + 1 if crosses_center else dist_in"
        variable_name: dist_out
      - type: spatial_calculation
        name: new_mover_start_position
        value: anchor.position + dist_out
    transformation:
      - Preserve grid dimensions.
      - Initialize output grid with background color.
      - Place the anchor object at its original position.
      - Calculate `new_mover_start_position`.
      - Place the mover object (preserving color and length) starting at `new_mover_start_position`.
    ```


*   **Natural Language Program:**
    1.  Identify the single maroon pixel (color 9) and record its index (`maroon_pos`).
    2.  Identify the single contiguous horizontal line of a color other than white (0) or maroon (9). Record its color (`line_color`), start index (`line_start`), and end index (`line_end`). Calculate its length (`line_length = line_end - line_start + 1`).
    3.  Calculate the input distance `dist_in` between the end of the line and the maroon pixel: `dist_in = maroon_pos - line_end`.
    4.  Determine the width `W` of the grid. Calculate the center index/indices. If `W` is odd, the center index is `floor(W/2)`. If `W` is even, the center indices are `W/2 - 1` and `W/2`.
    5.  Check if the input line interval [`line_start`, `line_end`] includes the center index (for odd `W`) or either center index (for even `W`). Set a flag `crosses_center` to true if it does, otherwise false.
    6.  Calculate the output distance `dist_out`: If `crosses_center` is true, `dist_out = dist_in + 1`. Otherwise, `dist_out = dist_in`.
    7.  Create a new output grid of the same dimensions as the input, filled entirely with the background color (white, 0).
    8.  Place the maroon pixel (color 9) at `maroon_pos` in the output grid.
    9.  Calculate the new starting index for the line: `new_line_start = maroon_pos + dist_out`.
    10. Draw the horizontal line using `line_color` and `line_length` starting at `new_line_start` in the output grid.
