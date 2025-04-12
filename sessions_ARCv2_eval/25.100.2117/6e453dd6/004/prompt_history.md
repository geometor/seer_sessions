
## train_1

**input:**
```
0 0 0 0 6 6 6 6 6 6 6 5 6 6 6 6
0 0 6 0 6 6 6 6 6 6 6 5 6 6 6 6
6 0 0 0 0 6 6 6 6 6 6 5 6 6 6 6
0 0 0 0 0 0 6 6 6 6 6 5 6 6 6 6
6 6 6 0 6 0 6 6 6 6 6 5 6 6 6 6
6 6 6 0 6 0 6 6 6 6 6 5 6 6 6 6
6 6 6 0 6 0 6 6 6 6 6 5 6 6 6 6
6 6 6 0 0 0 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 6 6 6 0 6 0 5 6 6 6 6
6 6 6 6 6 6 6 6 0 6 0 5 6 6 6 6
6 6 6 6 6 6 6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
```


**output:**
```
6 6 6 6 6 0 0 0 0 6 6 5 6 6 6 6
6 6 6 6 6 0 0 6 0 6 6 5 6 6 6 6
6 6 6 6 6 6 0 0 0 0 6 5 6 6 6 6
6 6 6 6 6 0 0 0 0 0 0 5 6 6 6 6
6 6 6 6 6 6 6 6 0 6 0 5 2 2 2 2
6 6 6 6 6 6 6 6 0 6 0 5 2 2 2 2
6 6 6 6 6 6 6 6 0 6 0 5 2 2 2 2
6 6 6 6 6 6 6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 6 6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 6 6 6 0 6 0 5 2 2 2 2
6 6 6 6 6 6 6 6 0 6 0 5 2 2 2 2
6 6 6 6 6 6 6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 5 6 6 6 6
```

*   **Initial Perception:**

    The task involves transforming a grid of numbers. The input grid primarily consists of the number 6, with some scattered 0s forming distinct shapes and a single vertical line of 5s. The output grid retains the background 6s and the line of 5s but replaces the 0s. A new rectangular area filled with 2s appears in the output. The transformation seems to involve identifying the shapes formed by the 0s in the input, removing them (filling with 6s), and then using properties (like bounding box coordinates) of these shapes to determine the location and size of the new rectangle of 2s in the output.

*   **Observed Facts:**

    
```yaml
    input_grid:
      type: 2D array (list of lists)
      dimensions: 16x16
      values:
        - 0: Forms distinct shapes (two L-shapes in this example)
        - 5: Forms a vertical line at column index 11
        - 6: Background value
    output_grid:
      type: 2D array (list of lists)
      dimensions: 16x16
      values:
        - 2: Forms a rectangular region in the output
        - 5: Forms a vertical line at column index 11 (preserved from input)
        - 6: Background value (original 6s and replaced 0s)
    objects:
      - background: Composed of cells with value 6.
      - marker_line: A vertical line composed of cells with value 5.
      - input_shapes: Contiguous regions composed of cells with value 0.
        - shape_1: An L-shape in the upper-left quadrant. Bounding box: rows 0-7, cols 4-10.
        - shape_2: An L-shape (rotated) in the lower-right quadrant. Bounding box: rows 11-14, cols 8-10.
      - output_rectangle: A rectangular region composed of cells with value 2. Bounding box: rows 4-7, cols 12-15.
    relationships:
      - The marker_line (value 5) is unchanged between input and output.
      - The background value (6) persists, replacing the input_shapes (value 0).
      - The location and dimensions of the output_rectangle (value 2) appear derived from the bounding boxes of the two input_shapes.
        - Output rectangle top row = Input shape 1 min column index.
        - Output rectangle bottom row = Input shape 1 max row index.
        - Output rectangle left column = Input shape 2 min row index + 1.
        - Output rectangle right column = Input shape 2 max row index + 1.
        - Output rectangle height = Input shape 2 height.
        - Output rectangle width = Input shape 2 height.
    actions:
      - Identify all contiguous shapes formed by the value 0 in the input grid.
      - Calculate the bounding box for each identified shape.
      - Determine which shape corresponds to 'shape 1' (e.g., the one with the overall minimum row index) and which is 'shape 2'.
      - Replace all 0s in the input grid with 6s to form the initial output grid base.
      - Calculate the coordinates for the output rectangle using the bounding box properties of shape 1 and shape 2 as described in 'relationships'.
      - Fill the calculated rectangular area in the output grid with the value 2.
    ```


*   **Natural Language Program:**

    1.  Initialize the output grid as a copy of the input grid.
    2.  Find all distinct contiguous regions (shapes) composed of the value 0 in the input grid.
    3.  If exactly two such shapes are found:
        a.  Determine the bounding box (minimum row, minimum column, maximum row, maximum column) for each shape.
        b.  Identify 'Shape 1' as the shape whose bounding box has the smaller minimum row index. Identify 'Shape 2' as the other shape.
        c.  Let Bbox1 = (r1_min, c1_min, r1_max, c1_max) be the bounding box of Shape 1.
        d.  Let Bbox2 = (r2_min, c2_min, r2_max, c2_max) be the bounding box of Shape 2.
        e.  Replace all cells with the value 0 in the output grid with the value 6.
        f.  Calculate the coordinates for a new rectangular region:
            i.  `top_row = c1_min`
            ii. `bottom_row = r1_max`
            iii. `left_col = r2_min + 1`
            iv. `right_col = r2_max + 1`
        g.  Fill all cells within the calculated rectangle (from `top_row` to `bottom_row` inclusive, and from `left_col` to `right_col` inclusive) in the output grid with the value 2.
    4.  If the number of shapes is not exactly two, return the initial copy of the input grid with 0s potentially replaced by 6s (or handle as an error/undefined case based on further examples).

## train_2

**input:**
```
0 0 0 6 6 5 6 6 6 6
0 6 0 6 6 5 6 6 6 6
0 0 0 0 6 5 6 6 6 6
6 0 6 0 6 5 6 6 6 6
6 0 0 0 6 5 6 6 6 6
6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 5 6 6 6 6
0 0 0 6 6 5 6 6 6 6
0 6 0 6 6 5 6 6 6 6
0 0 0 6 6 5 6 6 6 6
0 6 6 6 6 5 6 6 6 6
0 0 0 6 6 5 6 6 6 6
6 6 6 6 6 5 6 6 6 6
0 0 0 6 6 5 6 6 6 6
0 6 0 6 6 5 6 6 6 6
0 0 0 6 6 5 6 6 6 6
```


**output:**
```
6 0 0 0 6 5 6 6 6 6
6 0 6 0 6 5 6 6 6 6
6 0 0 0 0 5 6 6 6 6
6 6 0 6 0 5 2 2 2 2
6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 5 6 6 6 6
6 6 6 6 6 5 6 6 6 6
6 6 0 0 0 5 6 6 6 6
6 6 0 6 0 5 2 2 2 2
6 6 0 0 0 5 6 6 6 6
6 6 0 6 6 5 6 6 6 6
6 6 0 0 0 5 6 6 6 6
6 6 6 6 6 5 6 6 6 6
6 6 0 0 0 5 6 6 6 6
6 6 0 6 0 5 2 2 2 2
6 6 0 0 0 5 6 6 6 6
```

*   **Refined Perception:**

    The task involves transforming a grid containing background cells (6), a vertical marker line (5), and foreground shapes made of 0s. The transformation logic depends critically on whether the specific horizontal pattern `[0, 6, 0]` exists anywhere in the input grid rows.

    *   If the `[0, 6, 0]` pattern *is present* (as in `train_2`), the transformation involves:
        1.  Shifting all 0s one column to the right.
        2.  Replacing the original locations of the 0s with the background value (6).
        3.  Identifying the rows containing the `[0, 6, 0]` pattern.
        4.  For each such row `r`, adding rectangles of 2s in the output grid at rows `r` and `r+1`, in columns determined relative to the marker line's position (specifically, from marker column + 2 to marker column + 5).

    *   If the `[0, 6, 0]` pattern *is absent* (as in `train_1`), the transformation involves:
        1.  Identifying the distinct shapes formed by the 0s (assuming exactly two shapes).
        2.  Calculating the bounding boxes of these two shapes.
        3.  Replacing all 0s with the background value (6).
        4.  Adding a single rectangle of 2s, whose coordinates are derived from the minimum/maximum row/column indices of the two input shapes' bounding boxes.

    The marker line (5) is always preserved in its original location. The grid dimensions can vary between examples.

*   **Updated Facts:**

    
```yaml
    input_grid:
      type: 2D array (list of lists)
      dimensions: Variable (e.g., 16x16, 16x10)
      values:
        - 0: Forms distinct foreground shapes. Key trigger pattern is [0, 6, 0] horizontally.
        - 5: Forms a single vertical marker line.
        - 6: Background value.
    output_grid:
      type: 2D array (list of lists)
      dimensions: Same as input grid.
      values:
        - 0: Present only if input contains [0, 6, 0]; represents input 0s shifted right.
        - 2: Forms rectangular regions. Location/presence depends on input pattern.
        - 5: Preserved vertical marker line from input.
        - 6: Background value (original 6s and replaced 0s).
    objects:
      - background: Cells with value 6.
      - marker_line: A vertical line of cells with value 5. Its column index is important (let's call it c5).
      - input_shapes: Contiguous regions of cells with value 0 in the input.
      - output_shapes_0: Contiguous regions of cells with value 0 in the output (shifted from input). Present only if input contains [0, 6, 0].
      - output_rectangles_2: Rectangular regions of cells with value 2.
    patterns:
      - trigger_pattern: The horizontal sequence [0, 6, 0] appearing in any row of the input grid.
    relationships_and_conditions:
      - The marker_line (5) is always unchanged.
      - Condition: Check if the trigger_pattern [0, 6, 0] exists in any input row.
      - Case 1 (Trigger pattern exists - e.g., train_2):
          - Input 0s at (r, c) are effectively moved to output 0s at (r, c+1).
          - Original input 0 locations (r, c) become 6 in the output.
          - For each input row 'r' containing the trigger_pattern [0, 6, 0]:
              - A block of 2s is created in the output grid covering rows r and r+1 (within grid bounds).
              - This block spans columns from c5 + 2 to c5 + 5 (inclusive).
      - Case 2 (Trigger pattern does NOT exist - e.g., train_1):
          - All input 0s are replaced by 6s in the output grid. No 0s remain.
          - Exactly two input_shapes are assumed to exist.
          - Bbox1 (r1_min, c1_min, r1_max, c1_max) is found for the shape with the overall minimum row index.
          - Bbox2 (r2_min, c2_min, r2_max, c2_max) is found for the other shape.
          - A single output_rectangle_2 is created with:
              - top_row = c1_min
              - bottom_row = r1_max
              - left_col = r2_min + 1
              - right_col = r2_max + 1
    actions:
      - Find the column index `c5` of the marker_line (value 5).
      - Check all rows in the input grid for the presence of the subsequence `[0, 6, 0]`.
      - Based on whether the pattern is found, apply the logic described in 'Case 1' or 'Case 2'.
      - Initialize the output grid appropriately (copying input or starting with background 6s).
      - Modify the output grid by placing 0s (if applicable), replacing 0s with 6s, copying the marker line, and drawing the rectangle(s) of 2s.
    ```


*   **Updated Natural Language Program:**

    1.  Create the output grid, initially as a copy of the input grid.
    2.  Find the column index `c5` where the value 5 (marker line) occurs in the input grid.
    3.  Search the input grid to determine if any row contains the horizontal sequence
 `[0, 6, 0]`. Let `pattern_found` be true if found, false otherwise.
    4.  Find all coordinates `(r, c)` of cells with value 0 in the input grid. Store these coordinates.
    5.  **If `pattern_found` is true:**
        a.  Iterate through the stored input 0-coordinates `(r, c)`: Replace the value at `(r, c)` in the output grid with 6.
        b.  Iterate through the stored input 0-coordinates `(r, c)` again: Set the value at `(r, c+1)` in the output grid to 0 (ensure `c+1` is within grid bounds).
        c.  Iterate through each row index `r` of the input grid:
            i.  Check if the input row `r` contains the sequence `[0, 6, 0]`.
            ii. If it does, define the column range `c_start = c5 + 2` to `c_end = c5 + 5`.
            iii.Fill the cells in the output grid with 2s for row `r` in the column range `[c_start, c_end]` (inclusive, checking bounds).
            iv. Fill the cells in the output grid with 2s for row `r+1` in the column range `[c_start, c_end]` (inclusive, checking bounds).
    6.  **If `pattern_found` is false:**
        a.  Replace all cells with value 0 in the output grid with 6.
        b.  Identify all distinct contiguous regions (shapes) of 0s from the *original* input grid. Assume exactly two shapes are found.
        c.  Determine the bounding box (min_row, min_col, max_row, max_col) for each shape.
        d.  Identify 'Shape 1' as the shape whose bounding box has the smaller minimum row index. Let its bounding box be `(r1_min, c1_min, r1_max, c1_max)`.
        e.  Identify 'Shape 2' as the other shape. Let its bounding box be `(r2_min, c2_min, r2_max, c2_max)`.
        f.  Calculate the coordinates for the output rectangle:
            i.  `top_row = c1_min`
            ii. `bottom_row = r1_max`
            iii. `left_col = r2_min + 1`
            iv. `right_col = r2_max + 1`
        g.  Fill all cells within the calculated rectangle (from `top_row` to `bottom_row` inclusive, and from `left_col` to `right_col` inclusive) in the output grid with the value 2 (checking bounds).
    7.  Ensure the marker line (value 5) is correctly preserved in the output grid (it should be, as the modifications target 0s or specific calculated regions).
    8.  Return the final output grid.

## train_3

**input:**
```
6 0 0 0 0 0 6 5 6 6
6 0 6 6 6 0 6 5 6 6
6 0 0 0 0 0 6 5 6 6
6 6 6 6 6 6 6 5 6 6
6 6 0 0 0 0 6 5 6 6
6 6 0 6 6 0 6 5 6 6
6 6 0 6 6 0 6 5 6 6
6 6 0 0 0 0 6 5 6 6
6 6 6 6 6 6 6 5 6 6
6 6 6 6 0 0 6 5 6 6
6 6 6 6 0 0 6 5 6 6
6 6 6 6 6 6 6 5 6 6
6 0 0 0 0 0 6 5 6 6
6 0 6 0 6 0 6 5 6 6
6 0 0 0 0 0 6 5 6 6
6 6 6 6 6 6 6 5 6 6
6 0 0 0 0 6 6 5 6 6
6 0 6 6 0 6 6 5 6 6
6 0 0 0 0 6 6 5 6 6
6 6 6 6 6 6 6 5 6 6
```


**output:**
```
6 6 0 0 0 0 0 5 6 6
6 6 0 6 6 6 0 5 2 2
6 6 0 0 0 0 0 5 6 6
6 6 6 6 6 6 6 5 6 6
6 6 6 0 0 0 0 5 6 6
6 6 6 0 6 6 0 5 2 2
6 6 6 0 6 6 0 5 2 2
6 6 6 0 0 0 0 5 6 6
6 6 6 6 6 6 6 5 6 6
6 6 6 6 6 0 0 5 6 6
6 6 6 6 6 0 0 5 6 6
6 6 6 6 6 6 6 5 6 6
6 6 0 0 0 0 0 5 6 6
6 6 0 6 0 6 0 5 2 2
6 6 0 0 0 0 0 5 6 6
6 6 6 6 6 6 6 5 6 6
6 6 6 0 0 0 0 5 6 6
6 6 6 0 6 6 0 5 2 2
6 6 6 0 0 0 0 5 6 6
6 6 6 6 6 6 6 5 6 6
```

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
```python
import copy
from collections import deque

"""
Transforms a 2D grid based on the presence or absence of a specific horizontal 
pattern `(0, 6+, 0)` (a 0, followed by one or more 6s, followed by a 0) 
within any row of the input grid. The grid also contains a background value (6) 
and a single vertical marker line (5).

Transformation Rules:

Case 1: Pattern (0, 6+, 0) is Present
    - All 0s in the input grid are shifted one column to the right in the output grid.
    - The original locations of the input 0s are filled with the background value 6.
    - For every row in the *input* grid that contained the (0, 6+, 0) pattern, 
      the corresponding row in the *output* grid has cells filled with 2s, 
      starting from the column immediately to the right of the marker line (5) 
      and extending to the right edge of the grid.

Case 2: Pattern (0, 6+, 0) is Absent
    - All 0s in the input grid are replaced by the background value 6.
    - The input grid is expected to contain exactly two distinct contiguous shapes 
      formed by 0s.
    - The bounding boxes of these two input shapes are determined.
    - A single rectangular area is filled with 2s in the output grid. The 
      coordinates of this rectangle are derived from a combination of the 
      min/max row/col indices of the two input shapes' bounding boxes:
        - top_row = shape1.min_col
        - bottom_row = shape1.max_row
        - left_col = shape2.min_row + 1
        - right_col = shape2.max_row + 1
      (Where shape1 is the shape with the smaller min_row index).

The marker line (5) is always preserved in its original position.
"""

def find_marker_col(grid: list[list[int]], marker_value: int) -> int:
    """Finds the column index of the first occurrence of the marker value."""
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == marker_value:
                return c
    return -1 # Should not happen based on problem description

def pattern_06plus0(row: list[int]) -> bool:
    """Checks if a row contains the pattern (0, 6+, 0)."""
    n = len(row)
    for i in range(n):
        if row[i] == 0:
            for j in range(i + 2, n): # Need at least one 6 in between
                if row[j] == 0:
                    # Check if all elements between i and j are 6
                    all_sixes = True
                    for k in range(i + 1, j):
                        if row[k] != 6:
                            all_sixes = False
                            break
                    if all_sixes:
                        return True
            # Optimization: if we found a 0 at i, we don't need to re-check
            # pairs starting before the next 0 found after the inner loop.
            # But simpler implementation is fine for typical grid sizes.
    return False

def check_pattern_in_grid(grid: list[list[int]]) -> bool:
    """Checks if the (0, 6+, 0) pattern exists in any row of the grid."""
    for row in grid:
        if pattern_06plus0(row):
            return True
    return False

def find_all_coords(grid: list[list[int]], value: int) -> list[tuple[int, int]]:
    """Finds coordinates of all cells with a specific value."""
    coords = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == value:
                coords.append((r, c))
    return coords

def get_neighbors(r: int, c: int, height: int, width: int) -> list[tuple[int, int]]:
    """Gets valid 4-directional neighbors within grid bounds."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_shapes(grid: list[list[int]], value: int) -> list[set[tuple[int, int]]]:
    """Finds distinct contiguous shapes of a given value using BFS."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    shapes = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] == value and (r, c) not in visited:
                # Start BFS for a new shape
                current_shape = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_shape.add((curr_r, curr_c))
                    
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width):
                        if grid[nr][nc] == value and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if current_shape:
                    shapes.append(current_shape)
                    
    return shapes

def get_bounding_box(shape_coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a shape."""
    if not shape_coords:
        return (-1, -1, -1, -1) # Or raise error
        
    min_r = min(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    max_r = max(r for r, c in shape_coords)
    max_c = max(c for r, c in shape_coords)
    return min_r, min_c, max_r, max_c

# --------------------------------------------------------------------------

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules based on the (0, 6+, 0) pattern.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    
    # --- Initialization and Analysis ---
    output_grid = copy.deepcopy(input_grid)
    marker_col = find_marker_col(input_grid, 5)
    pattern_found = check_pattern_in_grid(input_grid)
    zero_coords = find_all_coords(input_grid, 0)
    
    # --- Case 1: Pattern (0, 6+, 0) Found ---
    if pattern_found:
        # Step 1: Replace original 0s with 6s
        for r, c in zero_coords:
            if 0 <= r < height and 0 <= c < width:
                 output_grid[r][c] = 6
                 
        # Step 2: Place 0s shifted one column to the right
        for r, c in zero_coords:
            if 0 <= r < height and c + 1 < width: # Check bounds for shift
                 output_grid[r][c + 1] = 0
                 
        # Step 3: Draw horizontal lines of 2s for rows containing the pattern
        for r_in in range(height):
            if pattern_06plus0(input_grid[r_in]): # Check original input row
                for c_out in range(marker_col + 1, width):
                     if 0 <= r_in < height and 0 <= c_out < width: # Bounds check
                         output_grid[r_in][c_out] = 2
                         
    # --- Case 2: Pattern (0, 6+, 0) Not Found ---
    else:
        # Step 1: Replace all 0s with 6s
        for r, c in zero_coords:
             if 0 <= r < height and 0 <= c < width:
                 output_grid[r][c] = 6
                 
        # Step 2: Find the two shapes of 0s in the *original* input
        # Use the pre-calculated zero_coords to potentially speed up find_shapes,
        # but using the standard find_shapes on the input grid is more robust.
        shapes = find_shapes(input_grid, 0)
        
        # Assuming exactly two shapes exist if pattern is not found
        if len(shapes) == 2:
            # Step 3: Calculate bounding boxes
            bboxes = [get_bounding_box(s) for s in shapes]
            
            # Step 4: Sort shapes by min_row to identify Shape 1 and Shape 2
            # Shape 1 has the smaller min_row
            if bboxes[0][0] <= bboxes[1][0]:
                bbox1 = bboxes[0] # r1_min, c1_min, r1_max, c1_max
                bbox2 = bboxes[1] # r2_min, c2_min, r2_max, c2_max
            else:
                bbox1 = bboxes[1]
                bbox2 = bboxes[0]
                
            # Step 5: Calculate output rectangle coordinates
            r1_min, c1_min, r1_max, c1_max = bbox1
            r2_min, c2_min, r2_max, c2_max = bbox2
            
            top_row = c1_min
            bottom_row = r1_max
            left_col = r2_min + 1
            right_col = r2_max + 1
            
            # Step 6: Fill the output rectangle with 2s
            for r in range(top_row, bottom_row + 1):
                for c in range(left_col, right_col + 1):
                    if 0 <= r < height and 0 <= c < width: # Check bounds
                        output_grid[r][c] = 2
        # else: handle cases with not exactly 2 shapes if necessary
        # (e.g., return the grid with 0s replaced by 6s)

    return output_grid
```
