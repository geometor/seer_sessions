## Perception

The task takes a small input grid (3x3 in all examples) and transforms it into a larger output grid (5x5 in all examples). Each pixel's color in the input grid is preserved in the output grid, but its spatial extent is modified.

Observing the relationship between input and output grids reveals a pattern of selective duplication:
1.  **Row Duplication:** The first and third rows of the input grid are duplicated vertically in the output grid. The middle (second) row is not duplicated.
2.  **Column Duplication:** Similarly, the first and third columns of the input grid are duplicated horizontally in the output grid. The middle (second) column is not duplicated.

This combined duplication results in the expansion from 3x3 to 5x5. Cells at the corners of the input (e.g., (0,0), (0,2), (2,0), (2,2)) become 2x2 blocks in the output. Cells along the edges but not corners (e.g., (0,1), (1,0), (1,2), (2,1)) become 1x2 or 2x1 blocks. The central cell (1,1) remains a 1x1 block.

This suggests a rule based on the position relative to the center of the grid (assuming odd dimensions): rows and columns that are *not* the central row/column are duplicated.

## Facts


```yaml
task_type: grid_transformation
input_shape: [3, 3] # Consistent across examples
output_shape: [5, 5] # Consistent across examples
transformation_type: spatial_resizing_selective_duplication
properties:
  - Input grid dimensions are odd (3x3).
  - Output grid dimensions are derived from input: H_out = H_in + (H_in // 2), W_out = W_in + (W_in // 2). For 3x3 -> 5x5.
  - Pixel colors are preserved.
actions:
  - Identify the central row index (H_in // 2).
  - Identify the central column index (W_in // 2).
  - Duplicate rows vertically, except for the central row.
  - Duplicate columns horizontally, except for the central column.
relationships:
  - Each pixel in the input corresponds to a 1x1, 1x2, 2x1, or 2x2 block of the same color in the output.
  - The size of the block depends on whether the input pixel's row and/or column are the central ones.
    - Central row and central column (input[1,1]): maps to 1x1 block.
    - Central row, non-central column (input[1,0], input[1,2]): maps to 1x2 block.
    - Non-central row, central column (input[0,1], input[2,1]): maps to 2x1 block.
    - Non-central row, non-central column (input[0,0], input[0,2], input[2,0], input[2,2]): maps to 2x2 block.
```


## Natural Language Program

1.  Given an input grid (assumed to be 3x3 based on examples).
2.  Create a new output grid with dimensions 5x5.
3.  Determine the middle row index (`middle_row = 1`) and middle column index (`middle_col = 1`) of the input grid.
4.  Iterate through each cell `(r, c)` of the input grid with its color value `v`.
5.  Determine the corresponding top-left coordinate `(out_r, out_c)` in the output grid:
    *   `out_r = 2 * r` if `r <= middle_row`, else `out_r = 2 * r - 1`. (Maps 0->0, 1->2, 2->3)
    *   `out_c = 2 * c` if `c <= middle_col`, else `out_c = 2 * c - 1`. (Maps 0->0, 1->2, 2->3)
6.  Determine the size of the block (`height`, `width`) to fill in the output grid based on the input cell's position relative to the middle row/column:
    *   `height = 1` if `r == middle_row`, else `height = 2`.
    *   `width = 1` if `c == middle_col`, else `width = 2`.
7.  Fill the block in the output grid starting at `(out_r, out_c)` with dimensions `height` x `width` using the input cell's color value `v`.
8.  Return the completed 5x5 output grid.

*Alternative description (procedural duplication):*
1.  Given the 3x3 input grid.
2.  Create an intermediate grid by iterating through the rows of the input grid:
    *   If the row index is 0 or 2, append the row twice to the intermediate grid.
    *   If the row index is 1, append the row once to the intermediate grid. (Result is a 5x3 grid).
3.  Create the final 5x5 output grid by iterating through the columns of the intermediate grid (using the *original* column indices 0, 1, 2):
    *   If the original column index was 0 or 2, append the current column twice to the final grid.
    *   If the original column index was 1, append the current column once to the final grid.
4.  Return the final 5x5 grid.