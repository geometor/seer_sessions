
## train_1

**input:**
```
0 0 8 0 0 0 0 9 0 0
0 0 6 0 0 0 0 7 0 0
0 7 0 0 0 0 0 0 0 4
0 0 0 2 0 4 0 0 0 0
0 0 0 0 1 0 0 0 0 8
0 0 3 0 0 0 9 0 0 0
6 0 0 0 0 0 0 4 0 0
0 0 4 0 0 7 0 0 0 0
0 0 0 0 0 0 8 0 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 0 0 0 0 9 0 0
0 0 6 0 0 0 0 7 0 0
0 7 4 0 0 0 0 0 0 0
0 0 0 2 0 4 0 0 0 0
0 0 0 0 1 8 0 0 0 0
0 0 3 0 0 0 9 0 0 0
6 0 0 0 0 0 0 4 0 0
0 0 4 7 0 0 0 0 0 0
0 0 0 0 0 0 8 1 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
4 0 7 0 0
0 9 0 0 2
0 0 1 0 4
```


**output:**
```
4 7 0 0 0
0 9 0 0 2
0 0 1 0 4
```


## train_3

**input:**
```
0 8 0 4 0 0 0
4 0 0 0 0 0 7
0 0 1 0 0 8 0
0 9 0 0 4 0 0
```


**output:**
```
0 8 0 4 0 0 0
4 7 0 0 0 0 0
0 0 1 8 0 0 0
0 9 0 0 4 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 1 0 8 0 0 0 0
0 0 6 0 0 0 0 7
0 0 0 4 0 7 0 0
3 0 0 0 4 0 0 0
0 2 0 0 0 9 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 1 8 0 0 0 0 0
0 0 6 0 0 0 0 7
0 0 0 4 7 0 0 0
3 0 0 0 4 0 0 0
0 2 0 0 0 9 0 0
0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception:**

1.  **Grid Structure:** The input and output are grids of pixels, with white (0) as the background.
2.  **Colored Pixels:** Various colored pixels (non-zero values) are scattered across the grid, typically appearing as isolated single pixels.
3.  **Row-Based Changes:** The transformation appears to operate independently on each row. Rows with zero, one, or more than two colored pixels seem unchanged between input and output.
4.  **Two-Pixel Interaction:** The core change happens in rows containing exactly two colored pixels.
5.  **Movement/Copying:** In these specific rows, the rightmost colored pixel seems to "move" or have its color "copied" to the position immediately to the right of the leftmost colored pixel.
6.  **Overwriting:** The original position of the rightmost pixel becomes white (0) in the output. The pixel originally to the right of the leftmost pixel (if any) is overwritten by the color of the rightmost pixel.

**Facts (YAML):**


```yaml
task_type: object_manipulation
grid_properties:
  size: variable (observed up to 10x10, 3x5, 4x7, 7x8)
  background_color: white (0)
objects:
  - type: pixel
    color: any non-white color (1-9)
    shape: 1x1
    count_per_row: variable
relationships:
  - type: spatial
    relation: horizontal adjacency
    description: Key interaction occurs between pixels in the same row.
  - type: spatial
    relation: relative position
    description: Distinguishes between the leftmost and rightmost colored pixel within a row.
actions:
  - action: identify
    target: rows containing exactly two non-white pixels
  - action: locate
    target: the leftmost and rightmost non-white pixel within identified rows
  - action: copy_color
    source: the rightmost non-white pixel
    destination: the cell immediately to the right of the leftmost non-white pixel
  - action: change_color
    target: the original position of the rightmost non-white pixel
    new_color: white (0)
  - action: maintain_state
    target: all rows not containing exactly two non-white pixels
    description: These rows are copied directly from input to output.
invariants:
  - Grid dimensions remain the same.
  - Rows with 0, 1, or 3+ non-white pixels are unchanged.
  - The leftmost non-white pixel in a modified row retains its position and color.
```


**Natural Language Program:**

1.  Create a new grid (output grid) with the same dimensions as the input grid, initially identical to the input grid.
2.  Examine each row of the input grid independently.
3.  For a given row, count the number of non-white pixels.
4.  If the count of non-white pixels in the row is exactly two:
    a.  Identify the column index of the leftmost non-white pixel (`col_left`) and the column index of the rightmost non-white pixel (`col_right`).
    b.  Determine the color of the rightmost pixel (`color_right`).
    c.  In the output grid, change the color of the pixel at the current row and column `col_left + 1` to `color_right`.
    d.  In the output grid, change the color of the pixel at the current row and column `col_right` to white (0).
5.  If the count of non-white pixels in the row is not two, make no changes to that row in the output grid (it remains as copied in step 1).
6.  After processing all rows, the resulting grid is the final output.
