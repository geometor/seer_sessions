
## train_1

**input:**
```
0 0 8 8 0
0 0 0 0 0
3 0 3 3 3
3 3 3 3 3
```


**output:**
```
0 0 0 0 0
0 8 0 0 0
3 8 3 3 3
3 3 3 3 3
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
0 0 0 0 0 5 5 0
0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0
8 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 5 5 0 2 2 2 0
8 5 5 8 2 2 2 8
8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 7 7 0 0 0 0 0 0
6 6 0 0 7 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 1 0 0 1 1 0 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 6 6 0 0 7 7 7 0 0
1 5 1 6 6 1 1 7 7 7 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```


## train_4

**input:**
```
0 0 0 0 0 0
0 2 2 0 0 0
0 0 0 0 3 3
0 0 0 0 3 3
0 0 0 0 0 0
1 0 1 0 0 1
1 1 1 1 1 1
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 2 0 3 3 0
1 2 1 3 3 1
1 1 1 1 1 1
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input/Output Structure**: Both input and output are 2D grids of colored pixels.
2.  **Colors**: Multiple colors are used (white, azure, green, red, gray, magenta, orange, blue). White (0) consistently acts as the background.
3.  **Key Action**: The primary transformation appears to be a form of "gravity" affecting non-white pixels. Pixels or contiguous blocks of the same color seem to fall downwards within their columns.
4.  **Stopping Condition**: Falling pixels stop when they encounter another non-white pixel directly below them or when they reach the bottom-most row of the grid.
5.  **Bottom Row**: The bottom row of the grid seems special. It acts as a "floor" and its contents remain unchanged from input to output. Pixels fall onto this row or onto other pixels that have already settled.
6.  **Independence**: The falling process appears to happen independently for each column. Pixels do not move horizontally.
7.  **Overwriting**: When pixels fall, they vacate their original positions, leaving behind the background color (white, 0), unless another pixel falls into that vacated spot.

**YAML Fact Document:**


```yaml
task_name: gravity_on_floor
description: Apply gravity to non-background pixels, making them fall downwards until they hit another non-background pixel or the bottom row.
grid_properties:
  dimensionality: 2
  background_color: 0 # white
elements:
  - element_type: pixel
    properties:
      - color: Integer (1-9) # Non-white colors
      - is_static: False # Subject to gravity unless on bottom row or blocked
  - element_type: pixel
    properties:
      - color: 0 # white
      - is_static: True # Background, does not move
  - element_type: grid_row
    properties:
      - position: last_row # The bottom-most row of the grid
      - is_static: True # Acts as a floor, pixels do not fall from or through it. Its initial state is preserved.
actions:
  - action_type: apply_gravity
    target: non-white pixels not on the bottom row
    constraints:
      - direction: downwards (increasing row index)
      - stops_when: cell below is non-white OR cell below is out of bounds (i.e., pixel reaches the bottom row)
    effects:
      - pixel moves to the lowest available position in its column
      - original position becomes white (background color)
relationships:
  - type: support
    from: non-white pixel OR bottom_row
    to: non-white pixel above it in the same column
    description: A non-white pixel or the bottom row prevents pixels directly above it from falling further.
```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Copy the contents of the bottom row (last row) from the input grid directly to the bottom row of the output grid.
3.  Iterate through each column `c` of the input grid (from left to right).
4.  Within each column `c`, iterate through the rows `r` from the second-to-last row up to the top row (i.e., from `height - 2` down to `0`).
5.  Examine the pixel at `(r, c)` in the *input* grid.
6.  If the pixel at `(r, c)` in the input grid is *not* the background color (i.e., its value is > 0):
    a.  Determine its final resting row, `dest_r`. Start searching downwards from row `r` in the *output* grid.
    b.  Find the largest row index `k` (where `k >= r`) such that the cell `(k + 1, c)` in the output grid is either out of bounds (meaning `k` is the last row) or contains a non-background pixel. The destination row `dest_r` is this row `k`.
    c.  Place the color of the input pixel `(r, c)` into the output grid at position `(dest_r, c)`.
7.  After processing all columns and relevant rows, the output grid contains the final transformed state.
