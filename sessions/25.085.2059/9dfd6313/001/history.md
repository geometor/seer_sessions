
## train_1

**input:**
```
5 0 0 0
0 5 0 0
6 0 5 0
6 0 4 5
```


**output:**
```
5 0 6 6
0 5 0 0
0 0 5 4
0 0 0 5
```


## train_2

**input:**
```
5 0 0
3 5 0
0 0 5
```


**output:**
```
5 3 0
0 5 0
0 0 5
```


## train_3

**input:**
```
5 0 0 0 0
0 5 0 0 0
8 8 5 0 0
0 2 0 5 0
0 2 0 1 5
```


**output:**
```
5 0 8 0 0
0 5 8 2 2
0 0 5 0 0
0 0 0 5 1
0 0 0 0 5
```

*   **Perception**:
    *   The input and output grids always have the same dimensions.
    *   The examples are square grids (4x4, 3x3, 5x5). It's possible the task only applies to square grids, or the transformation naturally works for non-square grids too (although matrix transpose is typically defined for any dimension). Assuming square grids based on examples.
    *   There is a prominent diagonal line of `grey (5)` pixels running from the top-left corner to the bottom-right corner in the input grids. These `grey (5)` pixels remain in the exact same positions in the output grids.
    *   Other colored pixels exist in the input grids, generally located off this main diagonal.
    *   In the output grids, these off-diagonal pixels have moved. Their positions appear to be mirrored across the main `grey (5)` diagonal.
    *   Specifically, a pixel at input position (row `r`, column `c`) moves to output position (column `c`, row `r`), *unless* `r` equals `c` (i.e., the pixel is on the main diagonal).
    *   This operation is equivalent to a matrix transpose, but with the constraint that the elements on the main diagonal remain fixed. An alternative way to achieve this is to swap the values of cell `(r, c)` and `(c, r)` for all pairs where `r < c`.

*   **Facts**:
    
```yaml
    task_type: transformation
    grid_properties:
      - input_output_same_dimensions: true
      - background_color: white (0)
      - main_diagonal_defined: top-left to bottom-right (where row_index == column_index)
    objects:
      - type: diagonal_pixels
        description: Pixels located on the main diagonal (row_index == column_index).
        color_in_examples: grey (5)
        action: Remain unchanged in their position.
      - type: off_diagonal_pixels
        description: Pixels located off the main diagonal (row_index != column_index).
        color_in_examples: various (magenta, yellow, green, azure, red, blue, white)
        action: Their position is transposed.
    transformation_logic:
      - type: reflection or transpose across diagonal
        constraint: Pixels on the main diagonal are fixed points.
        mechanism: For any pixel at input position (r, c), its value is moved to output position (c, r).
    relationship:
      - The output grid is a modification of the input grid where off-diagonal elements are reflected across the main diagonal.
    ```


*   **Natural Language Program**:
    1.  Identify the dimensions of the input grid (height H, width W).
    2.  Create an output grid of the same dimensions (H x W), initially identical to the input grid.
    3.  Iterate through all pairs of indices (row `r`, column `c`) such that `0 <= r < H` and `0 <= c < W`.
    4.  Focus on the pairs where the column index `c` is greater than the row index `r` (this covers all pairs off the main diagonal exactly once).
    5.  For each such pair `(r, c)`:
        a.  Get the value `value1` from the output grid at position `(r, c)`.
        b.  Get the value `value2` from the output grid at position `(c, r)`.
        c.  Set the value at position `(r, c)` in the output grid to `value2`.
        d.  Set the value at position `(c, r)` in the output grid to `value1`.
    6.  The resulting output grid is the final transformed grid.
