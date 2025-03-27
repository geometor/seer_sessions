
## train_1

**input:**
```
7 7 7 7 7 7 7 7
7 9 7 7 7 5 5 7
7 9 7 5 5 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 4 4 7
7 7 7 7 7 7 7 7
```


**output:**
```
7 9 7 7 7 7 7 7
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
7 9 7 7 7 7 7 7
7 9 7 7 7 7 7 7
7 9 7 7 7 7 7 7
4 4 4 4 4 4 4 4
7 9 7 7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 6 7 7 7 7
7 7 6 7 2 7 7
7 7 7 7 2 7 7
7 5 5 7 7 7 7
7 7 7 7 1 1 7
7 7 7 7 7 7 7
```


**output:**
```
7 7 6 7 2 7 7
7 7 6 7 2 7 7
7 7 6 7 2 7 7
7 7 6 7 2 7 7
5 5 5 5 5 5 5
1 1 1 1 1 1 1
7 7 6 7 2 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7
0 7 7 7 7 7 7 7 7
0 7 7 7 1 7 3 3 7
7 7 7 7 1 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 0 0 7
7 7 7 7 7 7 7 7 7
7 6 6 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```


**output:**
```
0 7 7 7 1 7 7 7 7
0 7 7 7 1 7 7 7 7
3 3 3 3 3 3 3 3 3
0 7 7 7 1 7 7 7 7
0 7 7 7 1 7 7 7 7
0 0 0 0 0 0 0 0 0
0 7 7 7 1 7 7 7 7
6 6 6 6 6 6 6 6 6
0 7 7 7 1 7 7 7 7
```

Okay, let's analyze the provided examples.

### Perception

1.  **Grid Structure:** The input and output are 2D grids of colored pixels, with orange (7) typically acting as the background color.
2.  **Objects:** Non-orange pixels often form contiguous shapes (objects). These objects seem to be the primary focus of the transformation.
3.  **Object Orientation:** Objects appear to be either primarily horizontal (width >= 1, height = 1, contained within a single row) or vertical (height > 1). Some objects might be single pixels (1x1), which can be considered horizontal.
4.  **Transformation Rules:** There seem to be two main rules operating:
    *   **Row Filling:** If a row in the input contains a horizontal object (a contiguous segment of non-orange color entirely within that row), the *entire* corresponding row in the output is filled with the color of that horizontal object. This fill overwrites everything else in that row.
    *   **Vertical Propagation:** For rows that are *not* filled based on the first rule, their content seems derived from the input row, but with modifications. Specifically, if a column in the input contains a vertical object (a contiguous segment of non-orange color with height > 1), the color of that vertical object is propagated vertically into any orange (7) cells within that same column in the output, but only in the non-filled rows. Non-orange pixels from the input generally persist in these non-filled output rows unless overwritten by a vertical propagation into an orange cell.
5.  **Precedence:** The row-filling rule based on horizontal objects takes precedence over the vertical propagation rule. If a row is filled, its original content (including parts of vertical objects) is completely replaced. Vertical propagation only affects cells that remain orange (7) in rows *not* subject to the row-filling rule.

### Facts


```yaml
elements:
  - role: background
    color: 7 (orange)
    description: The default color of the grid, typically representing empty space.
  - role: object
    description: Contiguous block(s) of non-background pixels.
    properties:
      - color: Any color except 7 (orange).
      - shape: Can be horizontal segments, vertical segments, or single pixels.
      - orientation: Determined by dimensions and position relative to rows/columns.

definitions:
  - term: horizontal_segment
    description: A contiguous sequence of one or more pixels of the same non-orange color, located entirely within a single row.
    example: `[7, 5, 5, 7]` in a row contains a horizontal segment of color 5. `[7, 9, 7, 9]` does not (not contiguous). `[7, 4, 4, 4]` does.
  - term: vertical_object_pixel
    description: A pixel belonging to a contiguous vertical sequence (within a single column) of two or more pixels of the same non-orange color in the input grid.
    example: In a column `[7, 9, 9, 7]`, the pixels at index 1 and 2 are vertical_object_pixels of color 9.

transformations:
  - type: row_fill
    trigger: Presence of one or more horizontal_segments in an input row `r`.
    action: Fill the entire corresponding output row `r` with the color of the horizontal_segment(s).
    precedence: High (overrides other rules for the affected row).
    assumption: If multiple horizontal segments of different colors exist in a row, the behavior is undefined by examples (assume only one color per row matters or this case doesn't occur). Based on examples, only one color triggers the fill per row.
  - type: conditional_copy_and_propagate
    trigger: Input row `r` does *not* contain any horizontal_segments.
    action: For each cell `(r, c)` in the output row:
      - If input cell `(r, c)` is non-orange, copy its color to output `(r, c)`.
      - If input cell `(r, c)` is orange (7):
        - Check if column `c` contains any vertical_object_pixels in the *input* grid.
        - If yes, set output `(r, c)` to the color of the vertical_object_pixel(s) in that column. (Assumption: only one such color per column if multiple vertical objects exist).
        - If no, set output `(r, c)` to orange (7).
    precedence: Low (only applies to rows not affected by row_fill).

grid_properties:
  - size: Input and output grids have the same dimensions.
```


### Natural Language Program

1.  Create an output grid with the same dimensions as the input grid.
2.  Identify all rows in the input grid that contain at least one "horizontal segment" (a contiguous block of identical non-orange pixels existing entirely within that single row). Record the color associated with each such row (assuming only one relevant color per row based on examples).
3.  For each row `r` identified in step 2, fill the *entire* row `r` in the output grid with the recorded color.
4.  For all remaining rows `r` in the output grid (those *not* filled in step 3):
    a.  Iterate through each column `c`.
    b.  Examine the pixel at `input[r, c]`.
    c.  If `input[r, c]` is *not* orange (7), copy its color to `output[r, c]`.
    d.  If `input[r, c]` *is* orange (7):
        i.  Check the entire column `c` in the *input* grid. Determine if this column contains any "vertical object pixels" (pixels belonging to a vertical contiguous block of height 2 or more of the same non-orange color).
        ii. If column `c` contains vertical object pixels, determine their color (assuming a single consistent color for vertical objects within a column based on examples) and set `output[r, c]` to that color.
        iii. If column `c` does *not* contain any vertical object pixels, set `output[r, c]` to orange (7).
5.  The
