Okay, let's break down the task based on the examples.

## Perception

1.  **Grid Structure:** Both input and output are 2D grids of pixels represented by integers (colors). The dimensions vary between examples (4x4 in the first, 6x6 in the second).
2.  **Row-Based Transformation:** The changes occur independently within specific rows. Some rows are modified, while others remain identical to the input.
3.  **Conditional Change:** The modification of a row depends on a specific pattern or condition within that row in the input grid.
    *   In Example 1, rows 1 and 3 change. These rows contain the sequence `8 3` (azure, green) starting at the second column (index 1). Rows 0 and 2, which contain `3 8` (green, azure) at those positions, do not change.
    *   In Example 2, rows 1, 3, and 5 change. These rows contain the sequence `5 0` (gray, white) starting at the first column (index 0). Rows 0, 2, and 4, which contain `0 5` (white, gray) at those positions, do not change.
4.  **Transformation Pattern:** When a row is modified, the change involves a specific rearrangement of three adjacent pixels.
    *   Let the trigger sequence be found starting at column `c`. The transformation affects the pixels at columns `c`, `c+1`, and `c+2`.
    *   Let the original values be `v_c`, `v_{c+1}`, `v_{c+2}`.
    *   The new values at these positions become `v_{c+2}`, `v_c`, `v_{c+1}`.
    *   This is equivalent to a cyclic permutation or a right rotation of the three values: `(v_c, v_{c+1}, v_{c+2}) -> (v_{c+2}, v_c, v_{c+1})`.
5.  **Trigger Specificity:** The trigger conditions seem to be specific pairs of adjacent colors: `(8, 3)` (azure, green) and `(5, 0)` (gray, white).
6.  **First Trigger Only:** In rows where a trigger pattern might occur multiple times or overlap, the examples suggest only the first occurrence (scanning left-to-right) triggers the transformation for that row.

## Facts


```yaml
task_type: row_based_transformation
scope: grid
focus: pixels

input_elements:
  - type: grid
    properties:
      - height: variable (e.g., 4, 6)
      - width: variable (e.g., 4, 6)
      - pixels: color values (0-9)

output_elements:
  - type: grid
    properties:
      - height: same as input
      - width: same as input
      - pixels: color values (0-9), potentially modified from input

transformation:
  type: conditional_pixel_rearrangement
  level: row
  trigger:
    type: specific_adjacent_pixel_pair
    conditions:
      - pair: [8, 3] # azure, green
      - pair: [5, 0] # gray, white
    location: occurs horizontally within a row, starting at column 'c'
    constraint: affects only the first occurrence found per row (left-to-right scan)
  action:
    type: cyclic_permutation_right
    target: three adjacent pixels starting at the trigger column 'c'
    details: |
      Let the original pixel values at (row, c), (row, c+1), (row, c+2) be Vc, Vc+1, Vc+2.
      The new pixel values at these positions become Vc+2, Vc, Vc+1.
    affected_pixels: (row, c), (row, c+1), (row, c+2)
  unmodified_rows: Rows where no trigger pair is found remain unchanged.
  unmodified_pixels: Pixels outside the 3-pixel segment in modified rows remain unchanged.

relationships:
  - input grid dimensions == output grid dimensions
  - output grid is derived from input grid by applying the transformation rule row by row.

examples_summary:
  - example: 1
    trigger_pair: [8, 3]
    trigger_column: 1
    affected_rows: 1, 3
    affected_segment: columns 1, 2, 3
  - example: 2
    trigger_pair: [5, 0]
    trigger_column: 0
    affected_rows: 1, 3, 5
    affected_segment: columns 0, 1, 2
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Define the set of trigger pairs: `{(8, 3), (5, 0)}`.
3.  Iterate through each row `r` of the input grid, from top to bottom.
4.  For the current row `r`, iterate through possible starting column indices `c` from `0` up to `width - 3`.
5.  At each column `c`, check if the pair of pixel values `(input[r, c], input[r, c+1])` exists in the defined set of trigger pairs.
6.  If a trigger pair is found at column `c`:
    a.  Get the three pixel values from the input grid: `v0 = input[r, c]`, `v1 = input[r, c+1]`, `v2 = input[r, c+2]`.
    b.  Update the corresponding pixels in the output grid for row `r`: set `output[r, c] = v2`, `output[r, c+1] = v0`, `output[r, c+2] = v1`.
    c.  Stop searching for triggers in the current row `r` and proceed to the next row (Step 3).
7.  If the inner loop completes for row `r` without finding any trigger pair, the row in the output grid remains unchanged (as it was initially copied).
8.  After processing all rows, return the final output grid.