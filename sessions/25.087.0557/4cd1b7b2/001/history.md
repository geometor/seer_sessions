
## train_1

**input:**
```
1 0 3 4
0 0 2 1
2 1 4 0
0 3 1 2
```


**output:**
```
1 2 3 4
3 4 2 1
2 1 4 3
4 3 1 2
```


## train_2

**input:**
```
0 4 2 3
4 1 0 2
0 3 4 0
3 0 1 4
```


**output:**
```
1 4 2 3
4 1 3 2
2 3 4 1
3 2 1 4
```


## train_3

**input:**
```
3 0 2 1
1 0 0 0
4 3 0 2
0 1 4 3
```


**output:**
```
3 4 2 1
1 2 3 4
4 3 1 2
2 1 4 3
```

Okay, let's break down this ARC task.

**Perception of Elements:**

1.  **Grid Structure:** The task operates on 4x4 grids. The input and output grids have the same dimensions.
2.  **Color Palette:** The input grids use colors blue (1), red (2), green (3), yellow (4), and white (0). The output grids only use colors blue (1), red (2), green (3), and yellow (4). White (0) is systematically replaced.
3.  **Pixel Preservation:** Pixels that are not white (0) in the input grid retain their color and position in the output grid.
4.  **White Pixel Replacement:** White pixels (0) in the input grid are replaced by one of the colors {1, 2, 3, 4} in the output grid.
5.  **Row Constraint:** Observing the output grids, each row contains exactly one instance of each color from the set {1, 2, 3, 4}. This resembles a Sudoku-like constraint applied row-wise.
6.  **Filling Logic:** The specific color used to replace a white pixel depends on which colors from the set {1, 2, 3, 4} are already present in that row in the input grid. The white pixels are filled with the "missing" colors for that row.
7.  **Assignment Order (Multiple Whites):** When a row contains multiple white pixels, there's a specific rule for assigning the multiple missing colors:
    *   Identify the missing colors (from {1, 2, 3, 4}) and sort them ascendingly.
    *   Identify the column indices of the white pixels and sort them ascendingly.
    *   If the row index (0-based) is **odd**, assign the *ascendingly* sorted missing colors to the *ascendingly* sorted white pixel indices.
    *   If the row index (0-based) is **even**, assign the *descendingly* sorted missing colors to the *ascendingly* sorted white pixel indices.

**YAML Facts:**


```yaml
task_type: transformation
grid_properties:
  size_relation: input and output grids have the same dimensions (4x4 in examples)
  input_palette: [blue(1), red(2), green(3), yellow(4), white(0)]
  output_palette: [blue(1), red(2), green(3), yellow(4)]
objects:
  - type: pixel
    properties:
      color: one of the palette colors
      position: row and column index
transformation_rules:
  - scope: grid
    action: preserve_pixels
    condition: input pixel color is not white(0)
    effect: output pixel at the same position has the same color as the input pixel
  - scope: row
    action: identify_missing_colors
    condition: true
    details: For each row, determine which colors from the set {blue(1), red(2), green(3), yellow(4)} are not present among the non-white pixels.
  - scope: row
    action: identify_white_pixels
    condition: true
    details: For each row, identify the column indices of all white(0) pixels.
  - scope: row
    action: fill_white_pixels
    condition: white pixels exist in the row
    details: |
      Replace white(0) pixels with the identified missing colors for that row.
      The assignment follows a specific order based on the row index:
      1. Sort missing colors (M) ascendingly.
      2. Sort white pixel column indices (W) ascendingly.
      3. If the row index is odd: Assign M[i] to the pixel at index W[i].
      4. If the row index is even: Assign M[N-1-i] (where N is the number of missing colors/white pixels) to the pixel at index W[i]. Effectively, assign descending missing colors to ascending white positions.
output_constraints:
  - type: row_completion
    details: Each row in the output grid must contain exactly one instance of each color: blue(1), red(2), green(3), yellow(4).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Process the grid row by row, using 0-based indexing for rows.
3.  For each row `r` (from 0 to height-1):
    a.  Find the set of non-white colors (`present_colors`) present in input row `r`.
    b.  Determine the set of `missing_colors` by finding which colors from {1, 2, 3, 4} are *not* in `present_colors`.
    c.  Find the list of column indices (`white_indices`) where the color is white (0) in input row `r`.
    d.  If `white_indices` is not empty:
        i.  Sort `missing_colors` in ascending order.
        ii. Sort `white_indices` in ascending order.
        iii. If the row index `r` is **even**: Reverse the sorted `missing_colors` list (to make it descending).
        iv. Iterate through `white_indices` from `i = 0` to `length(white_indices) - 1`:
            - Get the column index `col = white_indices[i]`.
            - Get the color to fill `fill_color = missing_colors[i]`.
            - Update the output grid at `(r, col)` with `fill_color`.
4.  Return the completed output grid.
