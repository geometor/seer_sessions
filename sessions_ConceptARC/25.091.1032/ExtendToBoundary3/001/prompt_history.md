
## train_1

**input:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```


**output:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```

Okay, let's break down these examples.

**Perception of Task Elements**

Across the three examples, the core operation involves identifying two key components in the input grid:
1.  A single, isolated "trigger" pixel of a specific color (yellow, orange, red in the examples).
2.  A "barrier" structure, which can be a line (vertical gray, horizontal orange/white pattern) or a set of points defining a line (diagonal green).

The transformation uses the trigger pixel's color and position, along with the barrier's position and orientation, to draw a new line or path onto the grid. The background white pixels are replaced by the trigger pixel's color along this new line/path. The original trigger pixel and barrier remain unchanged.

*   **Example 1:** A vertical gray barrier exists at column 1. A yellow trigger pixel exists at (5, 11). A horizontal yellow line is drawn on the trigger's row (row 5), starting from the column immediately to the right of the barrier (column 2) and extending to the grid's right edge.
*   **Example 2:** A horizontal patterned barrier exists at row 1. An orange trigger pixel exists at (7, 8). A vertical orange line is drawn in the trigger's column (column 8), starting from the row immediately below the barrier (row 2) and extending downwards, stopping just before the trigger's row (ending at row 7).
*   **Example 3:** A diagonal barrier is formed by green pixels (implicitly defining y=x for even coordinates). A red trigger pixel exists at (6, 0). A diagonal path of red pixels is drawn, starting from the trigger's position and moving towards the barrier (up and left: -1 row, -1 column per step), leaving a trail. The path stops just before it would intersect the implicit barrier line. The new pixels are added at (5, 1) and (4, 2).

**YAML Facts**


```yaml
task_description: Draw a line or path based on a trigger pixel and a barrier structure.

examples:
  - example_index: 1
    input_description: Grid with a vertical gray line at x=1 and a single yellow pixel at (5, 11).
    output_description: Input grid with an added horizontal yellow line from (5, 2) to (5, 11).
    objects:
      - id: barrier
        type: vertical_line
        color: gray
        position: column 1
      - id: trigger
        type: pixel
        color: yellow
        position: (5, 11)
    action:
      type: draw_line
      color: yellow
      orientation: horizontal
      start_position: adjacent to barrier (column 2) on trigger's row (row 5)
      end_position: right grid edge (column 11) on trigger's row (row 5)
    relationship: Trigger is to the right of the barrier. Line is drawn on trigger's row, from barrier towards grid edge.

  - example_index: 2
    input_description: Grid with a horizontal orange/white pattern at y=1 and a single orange pixel at (7, 8).
    output_description: Input grid with an added vertical orange line from (2, 8) to (7, 8).
    objects:
      - id: barrier
        type: horizontal_pattern_line
        color: orange/white
        position: row 1
      - id: trigger
        type: pixel
        color: orange
        position: (7, 8)
    action:
      type: draw_line
      color: orange
      orientation: vertical
      start_position: adjacent to barrier (row 2) in trigger's column (column 8)
      end_position: row before trigger (row 7) in trigger's column (column 8)
    relationship: Trigger is below the barrier. Line is drawn in trigger's column, from barrier towards (but stopping before) trigger row.

  - example_index: 3
    input_description: Grid with scattered green pixels suggesting a diagonal line (y=x) and a single red pixel at (6, 0).
    output_description: Input grid with added red pixels at (5, 1) and (4, 2).
    objects:
      - id: barrier
        type: diagonal_implicit_line
        color: green
        positions: (0,0), (2,2), (4,4), (6,6) - suggests y=x
      - id: trigger
        type: pixel
        color: red
        position: (6, 0)
    action:
      type: draw_path_trace
      color: red
      path_direction: diagonal up-left (-1 row, -1 column)
      start_position: adjacent to trigger (5, 1)
      end_position: position before hitting barrier line (4, 2) -> next step (3,3) would be on/near barrier
    relationship: Trigger is below/right of the implicit barrier line. Path moves towards the barrier, leaving a trace, stopping before intersection.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the single "trigger" pixel: Find the pixel whose color is not white (0) and is isolated (not part of a larger line/structure of the same color). Record its color (C) and position (tr, tc).
3.  Identify the "barrier" structure: Find the line or pattern of connected/aligned pixels (can be gray, or another color like orange or green). Determine its orientation (vertical, horizontal, or diagonal) and its primary position (e.g., column index for vertical, row index for horizontal, implicit line like y=x for diagonal).
4.  Based on the barrier orientation and trigger position:
    *   **If the barrier is vertical (at column b):**
        *   Determine the starting column (sc): if tc > b, sc = b + 1; else sc = b - 1.
        *   Determine the ending column (ec): if tc > b, ec = grid_width - 1; else ec = 0.
        *   Iterate through columns from sc to ec (inclusive, direction depends on sc vs ec). For each column `c`, set the pixel at `(tr, c)` in the output grid to color C.
    *   **If the barrier is horizontal (at row b):**
        *   Determine the starting row (sr): if tr > b, sr = b + 1; else sr = b - 1.
        *   Determine the ending row (er): if tr > b, er = tr - 1; else er = tr + 1.
        *   Iterate through rows from sr to er (inclusive, direction depends on sr vs er). For each row `r`, set the pixel at `(r, tc)` in the output grid to color C.
    *   **If the barrier is diagonal (e.g., implies line y=x):**
        *   Determine the step direction (dr, dc) based on the trigger's position relative to the barrier (e.g., if trigger is below/right of y=x like (6,0), step is (-1, -1)).
        *   Initialize current position (cr, cc) = (tr, tc).
        *   Loop:
            *   Update current position: cr = cr + dr, cc = cc + dc.
            *   Check boundary conditions: if cr or cc are outside grid bounds, stop.
            *   Check barrier condition: if the position (cr, cc) is "on" or "past" the barrier line (e.g., for y=x barrier, check if cr == cc or if the step crossed the line), stop.
            *   Set the pixel at `(cr, cc)` in the output grid to color C.
5.  Return the modified output grid.
