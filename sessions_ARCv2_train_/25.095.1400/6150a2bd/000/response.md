**Perception:**

The input and output are both 2D grids (or matrices) of integers. In both provided examples, the input grid seems to undergo a spatial transformation to produce the output grid. The numbers themselves within the grid are preserved, but their positions change. Comparing the input and output grids side-by-side, the transformation appears consistent with a 180-degree rotation. The element at the top-left corner of the input moves to the bottom-right corner of the output, the element at the top-right moves to the bottom-left, and so on, effectively reversing both row and column order.

**Facts:**


```yaml
Input:
  type: Grid
  data_type: integer
  dimensions: 3x3 (based on examples)
Output:
  type: Grid
  data_type: integer
  dimensions: 3x3 (based on examples)
Transformation:
  type: Spatial Rotation
  details: 180-degree rotation
  preserves_values: true
  changes_positions: true
Relationships:
  - Output grid element at row `r`, column `c` corresponds to the input grid element at row `max_row - 1 - r`, column `max_col - 1 - c`.
  - The set of numerical values present in the input grid is identical to the set of numerical values in the output grid.
```


**Natural Language Program:**

1.  Read the input grid.
2.  Create a new output grid with the same dimensions as the input grid.
3.  Iterate through each cell `(r, c)` of the input grid, where `r` is the row index and `c` is the column index.
4.  Determine the dimensions of the input grid (let `num_rows` be the number of rows and `num_cols` be the number of columns).
5.  Place the value from the input grid cell `(r, c)` into the output grid cell at position `(num_rows - 1 - r, num_cols - 1 - c)`.
6.  Return the completed output grid.