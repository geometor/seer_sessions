*   **Refined Perception:**

    The task involves transforming a 2D grid based on the presence or absence of a specific horizontal pattern within the input rows: `(0, 6+, 0)`, meaning a `0` followed by one or more `6`s, followed by another `0`. The grid also contains a background value (6) and a single vertical marker line (5). The transformation rule depends entirely on whether this `(0, 6+, 0)` pattern exists anywhere in the input grid.

    *   **Case 1: Pattern `(0, 6+, 0)` is Present (Examples `train_2`, `train_3`)**
        *   All `0`s in the input grid are effectively shifted one column to the right in the output grid.
        *   The original locations of the input `0`s are filled with the background value `6`.
        *   For every row in the *input* grid that contained the `(0, 6+, 0)` pattern, the corresponding row in the *output* grid has cells filled with `2`s, starting from the column immediately to the right of the marker line (5) and extending to the right edge of the grid.

    *   **Case 2: Pattern `(0, 6+, 0)` is Absent (Example `train_1`)**
        *   All `0`s in the input grid are replaced by the background value `6`.
        *   The input grid is expected to contain exactly two distinct contiguous shapes formed by `0`s.
        *   The bounding boxes of these two input shapes are determined.
        *   A single rectangular area is filled with `2`s in the output grid. The coordinates of this rectangle are derived from a combination of the minimum/maximum row/column indices of the two input shapes' bounding boxes.

    The marker line (5) is always preserved in its original position in both cases. Grid dimensions can vary.

*   **Updated Facts:**

    
```yaml
    input_grid:
      type: 2D array (list of lists)
      dimensions: Variable (e.g., 16x16, 16x10, 20x10)
      values:
        - 0: Forms foreground shapes/patterns.
        - 5: Forms a single vertical marker line.
        - 6: Background value.
    output_grid:
      type: 2D array (list of lists)
      dimensions: Same as input grid.
      values:
        - 0: Present only if the trigger pattern `(0, 6+, 0)` was found in the input. Represents input 0s shifted right.
        - 2: Forms rectangular regions (potentially multiple rows in Case 1, single block in Case 2).
        - 5: Preserved vertical marker line from input.
        - 6: Background value (original 6s and replaced/unmodified input 0 locations).
    objects:
      - background: Cells with value 6.
      - marker_line: A vertical line of cells with value 5. Its column index is critical (`c5`).
      - input_zeros: Coordinates of all cells with value 0 in the input.
      - input_shapes_case2: (Only relevant if trigger pattern absent) The two distinct contiguous regions of 0s in the input.
      - output_zeros_case1: Cells with value 0 in the output (shifted from input). Present only if trigger pattern was found.
      - output_regions_2: Rectangular regions of cells with value 2.
    patterns:
      - trigger_pattern: The pattern `(0, 6+, 0)` - a 0, followed by one or more 6s, followed by another 0 - appearing horizontally within any row of the input grid.
    properties:
      - height: Number of rows in the grid.
      - width: Number of columns in the grid.
      - marker_col (`c5`): The column index of the marker line (value 5).
      - pattern_found: Boolean flag indicating if the `trigger_pattern` exists anywhere in the input grid.
      - Bbox1, Bbox2 (Case 2 only): Bounding boxes (r_min, c_min, r_max, c_max) of the two input shapes. Shape 1 has the smaller `r_min`.
    relationships_and_conditions:
      - The marker_line (5) is always unchanged.
      - Condition: Check if `pattern_found` is true or false.
      - Case 1 (`pattern_found` is true - e.g., train_2, train_3):
          - Input 0s at `(r, c)` are effectively moved to output 0s at `(r, c+1)` (within bounds).
          - Original input 0 locations `(r, c)` become 6 in the output.
          - For each input row `r_in` containing the `trigger_pattern`:
              - A horizontal line of 2s is created in the output grid at row `r_in`.
              - This line spans columns from `c5 + 1` to `width - 1` (inclusive).
      - Case 2 (`pattern_found` is false - e.g., train_1):
          - All input 0s are replaced by 6s in the output grid. No 0s remain in the output.
          - Exactly two `input_shapes_case2` are assumed to exist.
          - Bbox1 (`r1_min`, `c1_min`, `r1_max`, `c1_max`) and Bbox2 (`r2_min`, `c2_min`, `r2_max`, `c2_max`) are calculated.
          - A single rectangular `output_regions_2` is created with:
              - top_row = `c1_min`
              - bottom_row = `r1_max`
              - left_col = `r2_min + 1`
              - right_col = `r2_max + 1`
    actions:
      - Determine grid `height` and `width`.
      - Find the column index `c5` of the marker_line (value 5).
      - Scan all rows in the input grid to check for the presence of the `trigger_pattern` `(0, 6+, 0)`. Set `pattern_found` flag.
      - Initialize the output grid as a copy of the input grid.
      - Store the coordinates `(r, c)` of all input cells containing 0.
      - Apply Case 1 or Case 2 logic based on `pattern_found`:
          - Case 1: Modify output by setting original 0 positions to 6, setting `(r, c+1)` to 0, and drawing horizontal lines of 2s in relevant rows from `c5+1` to `width-1`.
          - Case 2: Modify output by setting all original 0 positions to 6, finding the two 0-shapes (from input), calculating the output rectangle coordinates based on their bounding boxes, and filling that rectangle with 2s.
    ```


*   **Updated Natural Language Program:**

    1.  Get the dimensions (`height`, `width`) of the input grid.
    2.  Find the column index `c5` where the value 5 (marker line) occurs in the input grid. Assume it exists and is unique.
    3.  Scan all rows of the input grid to determine if any row contains the horizontal pattern `(0, 6+, 0)` (a `0`, followed by one or more `6`s, followed by another `0`). Set a boolean flag `pattern_found` accordingly.
    4.  Create the `output` grid as a deep copy of the `input` grid.
    5.  Find and store all coordinates `(r, c)` where `input[r][c] == 0`. Let this list be `zero_coords`.
    6.  **If `pattern_found` is true (Case 1):**
        a.  Iterate through each coordinate `(r, c)` in `zero_coords`: Set `output[r][c] = 6`.
        b.  Iterate through each coordinate `(r, c)` in `zero_coords`: If `c + 1 < width`, set `output[r][c+1] = 0`.
        c.  Iterate through each row index `r_in` from 0 to `height - 1`:
            i.  Check if the original `input` grid's row `r_in` contains the `(0, 6+, 0)` pattern.
            ii. If yes, then for each column index `c_out` from `c5 + 1` to `width - 1` (inclusive): Set `output[r_in][c_out] = 2`.
    7.  **If `pattern_found` is false (Case 2):**
        a.  Iterate through each coordinate `(r, c)` in `zero_coords`: Set `output[r][c] = 6`.
        b.  Identify the distinct contiguous regions (shapes) formed by the cells listed in `zero_coords` within the *original input grid*. Assume exactly two shapes are found.
        c.  Calculate the bounding box (`r_min`, `c_min`, `r_max`, `c_max`) for each of the two shapes.
        d.  Identify 'Shape 1' as the shape whose bounding box has the smaller `r_min`. Let its bounding box be `(r1_min, c1_min, r1_max, c1_max)`.
        e.  Identify 'Shape 2' as the other shape. Let its bounding box be `(r2_min, c2_min, r2_max, c2_max)`.
        f.  Calculate the coordinates for the output rectangle:
            i.  `top_row = c1_min`
            ii. `bottom_row = r1_max`
            iii. `left_col = r2_min + 1`
            iv. `right_col = r2_max + 1`
        g.  Iterate through row indices `r` from `top_row` to `bottom_row` (inclusive) and column indices `c` from `left_col` to `right_col` (inclusive): If `r` and `c` are within grid bounds, set `output[r][c] = 2`.
    8.  Return the final `output` grid.