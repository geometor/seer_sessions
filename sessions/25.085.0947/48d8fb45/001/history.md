
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 0
0 0 4
0 4 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 5 0 0 0 1 1 0
0 0 0 1 0 0 0 0 1 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 1 0 0
```


**output:**
```
0 1 0
1 1 1
0 1 1
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2
2 2 0
0 2 0
```

*   **Perception:**
    *   Each input grid is 10x10 and contains mostly white pixels (0).
    *   Each input grid contains exactly one gray pixel (5).
    *   Each input grid contains pixels of one other color (the "target color"): yellow (4) in example 1, blue (1) in example 2, and red (2) in example 3.
    *   The output grid is always 3x3.
    *   The output grid contains only white pixels and pixels of the target color from the corresponding input.
    *   The gray pixel seems to act as an anchor or reference point in the input grid.
    *   The output grid appears to represent the presence or absence of the target color in specific locations relative to the gray pixel in the input grid.
    *   By examining the relative positions of the target color pixels with respect to the gray pixel, a consistent pattern emerges. The output grid corresponds to a 3x3 window of relative coordinates: rows `+1` to `+3` and columns `-1` to `+1`, relative to the gray pixel's position.

*   **Facts:**
    
```yaml
    task_type: object_transformation # or pattern_extraction
    input_grid_size: fixed (10x10 in examples)
    output_grid_size: fixed (3x3)
    elements:
      - type: background
        color: white (0)
      - type: anchor
        color: gray (5)
        count: 1 per input
        role: defines a reference coordinate
      - type: target_pixels
        color: variable (non-white, non-gray, unique per input - e.g., yellow, blue, red)
        role: pixels whose relative positions are mapped to the output
    transformation:
      - action: identify_anchor
        input: input_grid
        output: anchor_coordinates (row, col)
      - action: identify_target_color
        input: input_grid
        criteria: color is not white (0) and not gray (5)
        output: target_color
      - action: initialize_output_grid
        size: 3x3
        fill_color: white (0)
      - action: map_relative_pixels
        input: input_grid, anchor_coordinates, target_color
        output: modified_output_grid
        details: |
          Iterate through output grid coordinates (out_r, out_c) from (0,0) to (2,2).
          Calculate relative coordinates: rel_r = out_r + 1, rel_c = out_c - 1.
          Calculate source coordinates in input: src_r = anchor_row + rel_r, src_c = anchor_col + rel_c.
          If source coordinates are within input bounds AND input_grid[src_r][src_c] == target_color:
            Set output_grid[out_r][out_c] = target_color.
    relationships:
      - The output grid's content depends on the spatial relationship between the target pixels and the anchor pixel in the input grid.
      - The specific relationship is a fixed 3x3 window of relative coordinates: rows [+1, +3], columns [-1, +1].
    ```


*   **Natural Language Program:**
    1.  Locate the single gray (5) pixel in the input grid and record its row and column index (`anchor_row`, `anchor_col`).
    2.  Identify the unique color present in the input grid that is not white (0) and not gray (5). This is the `target_color`.
    3.  Create a new 3x3 grid, called `output_grid`, and fill it entirely with white (0) pixels.
    4.  For each cell in the `output_grid` at position (`row`, `col`), where `row` ranges from 0 to 2 and `col` ranges from 0 to 2:
        a.  Calculate the corresponding source row index in the input grid: `source_row = anchor_row + (row + 1)`.
        b.  Calculate the corresponding source column index in the input grid: `source_col = anchor_col + (col - 1)`.
        c.  Check if the calculated `source_row` and `source_col` are valid indices within the boundaries of the input grid.
        d.  If the source indices are valid, check the color of the pixel at `input_grid[source_row][source_col]`.
        e.  If the color at `input_grid[source_row][source_col]` is equal to the `target_color`, set the pixel at `output_grid[row][col]` to the `target_color`.
    5.  Return the final `output_grid`.
