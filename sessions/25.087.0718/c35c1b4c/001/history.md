
## train_1

**input:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 0 0
6 1 1 1 1 1 1 1 6 0
6 1 1 1 1 1 1 1 6 8
0 8 1 1 1 8 6 8 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


**output:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 8
0 8 1 1 1 1 1 1 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


## train_2

**input:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 0 0 0 3 9
9 3 3 3 3 0 0 9 3 0
3 3 3 3 3 9 0 0 3 7
3 3 3 3 3 0 9 9 3 0
0 9 0 3 3 3 9 9 9 9
7 9 7 9 0 0 7 7 0 0
```


**output:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 3 3 0 3 9
9 3 3 3 3 3 3 3 3 0
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
0 9 0 3 3 3 3 9 9 9
7 9 7 9 0 0 7 7 0 0
```


## train_3

**input:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 0 0 1 1 0
0 0 1 2 2 2 1 0 1 0
0 4 0 2 2 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 1 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```


**output:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 2 2 1 1 0
0 0 1 2 2 2 2 0 1 0
0 4 0 2 2 2 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 2 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```

Okay, let's analyze the task examples.

**Perception of Elements:**

Each example pair consists of an input grid and an output grid. The grids contain pixels of different colors.

Comparing the input and output grids in each example, I observe the following:
1.  **Structure Preservation:** Much of the grid structure and colors remain the same between input and output.
2.  **Color Spreading:** In each example, one specific color seems to "spread" or "grow" into adjacent cells.
    *   In `train_1`, the blue (1) pixels expand into neighboring cells.
    *   In `train_2`, the green (3) pixels expand into neighboring cells.
    *   In `train_3`, the red (2) pixels expand into neighboring cells.
3.  **Target Color:** The color that spreads appears to be the color of the largest contiguous block of non-background (non-white/0) pixels in the input grid.
4.  **Expansion Rule:** The expansion happens to all cells that are directly adjacent (horizontally, vertically, or diagonally) to a pixel of the target color in the input grid. These adjacent cells take on the target color in the output grid, regardless of their original color.
5.  **Original Object:** Pixels that were already the target color remain unchanged.

**YAML Facts:**


```yaml
task_description: Expand the largest contiguous object by one pixel layer in all directions.
elements:
  - type: grid
    properties:
      - contains pixels of different colors (0-9)
      - size varies (up to 30x30)
  - type: object
    properties:
      - contiguous block of pixels of the same color
      - connectivity includes horizontal, vertical, and diagonal adjacency
      - excludes background color (white/0)
  - type: target_object
    properties:
      - the object with the largest number of pixels in the input grid
      - has a specific color (target_color)
actions:
  - identify_objects: Find all contiguous non-background objects in the input grid.
  - find_largest_object: Determine the object with the maximum number of pixels.
  - identify_target_color: Get the color of the largest object.
  - identify_expansion_pixels: Find all pixels in the input grid that are adjacent (including diagonals) to any pixel of the target_object.
  - modify_grid: Create the output grid by changing the color of the expansion_pixels to the target_color. All other pixels retain their original input color.
relationships:
  - adjacency: Pixels are adjacent if they touch horizontally, vertically, or diagonally.
  - expansion: The target_object expands into adjacent pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all contiguous regions (objects) of pixels having the same non-white color in the input grid. Consider pixels connected horizontally, vertically, and diagonally as part of the same object.
3.  Determine the object with the largest area (most pixels). Let its color be `target_color`.
4.  Iterate through each pixel `(r, c)` in the input grid.
5.  For each pixel `(r, c)`, examine its eight neighbours (up, down, left, right, and the four diagonals).
6.  If the pixel at `(r, c)` in the input grid does *not* have the `target_color`, *and* at least one of its neighbours in the input grid *does* have the `target_color`, then change the color of the pixel at `(r, c)` in the *output* grid to `target_color`.
7.  Return the final output grid.
