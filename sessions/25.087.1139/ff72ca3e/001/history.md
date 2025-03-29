
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 2 2 2 0 0 0
0 0 2 4 2 0 0 0
0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0
0 0 2 2 2 2 2 0 0 0
0 5 2 2 4 2 2 0 0 0
0 0 2 2 2 2 2 0 0 0
0 0 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 2 2 2 2 2 2 0 0 0
0 2 2 2 2 2 2 2 0 0 0
0 2 2 2 2 2 2 2 0 0 0
0 2 2 2 4 2 2 2 0 0 0
0 2 2 2 2 2 2 2 0 0 0
0 2 2 2 2 2 2 2 0 0 0
0 2 2 2 2 2 2 2 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
```


**output:**
```
0 0 0 0 0 0 5 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 2 4 2 0 0 0 0 0
0 0 2 2 2 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 2 2 2 2 2 0
5 0 0 0 2 2 2 2 2 0
0 0 0 0 2 2 4 2 2 0
0 0 0 0 2 2 2 2 2 0
0 5 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 5
```

Okay, let's analyze the task examples.

**Perception:**

1.  **Input Grid:** Contains a background of white pixels (0) and scattered single pixels of gray (5) and yellow (4).
2.  **Output Grid:** The output grid retains the original gray and yellow pixels. Additionally, areas around the yellow pixels are filled with red pixels (2).
3.  **Key Objects:** The primary objects are the individual gray (5) and yellow (4) pixels. The transformation introduces areas of red (2) pixels.
4.  **Transformation:** The transformation seems to involve each yellow pixel interacting with its "closest" gray pixel(s). For each yellow pixel, a square area centered on it is filled with red pixels. The size of this red square appears determined by the distance and relative position to the closest gray pixel(s).
5.  **Size Determination:** The side length of the red square centered on a yellow pixel `Y` is calculated based on the gray pixel `G` which has the minimum Manhattan distance to `Y`. If multiple gray pixels share the minimum Manhattan distance, the one that results in the smallest square size based on the formula `Size = 2 * max(abs(Y_row - G_row), abs(Y_col - G_col)) - 1` is chosen.
6.  **Drawing:** The red square is drawn centered on the yellow pixel. Pixels within this square that are originally background (0) are changed to red (2). Original non-background pixels (gray and yellow) within the square's area remain unchanged. If multiple yellow pixels generate overlapping red squares, the red color is applied additively (a background pixel becomes red if it falls within *any* generated square).

**Facts:**


```yaml
elements:
  - role: background
    color: white (0)
    description: The default color filling most of the grid.
  - role: point_A
    color: gray (5)
    description: Single, scattered pixels acting as reference points. Multiple may exist.
  - role: point_B
    color: yellow (4)
    description: Single, scattered pixels acting as centers for the transformation. Multiple may exist.
  - role: fill_color
    color: red (2)
    description: Color used to fill square areas in the output grid.

relationships:
  - type: distance
    element1: point_B (yellow)
    element2: point_A (gray)
    metric: Manhattan distance
    description: The distance between each yellow pixel and all gray pixels is relevant.
  - type: relative_position
    element1: point_B (yellow)
    element2: point_A (gray)
    metric: Max coordinate difference (max(delta_row, delta_col))
    description: The maximum difference in row or column coordinates between a yellow pixel and its closest gray pixel determines the size of the output square.
  - type: centered_on
    element1: fill_color area (red square)
    element2: point_B (yellow)
    description: Each generated red square is centered on a yellow pixel.

actions:
  - action: find_closest
    input: point_B (yellow), all point_A (gray)
    output: closest point_A(s) based on Manhattan distance
    tie_breaking_1: None (consider all ties)
  - action: calculate_size
    input: point_B (yellow), closest point_A(s)
    output: integer size S
    logic: |
      For each closest gray G', calculate potential size s' = 2 * max(abs(Y_row - G'_row), abs(Y_col - G'_col)) - 1.
      The final size S is the minimum value among all calculated s'.
    tie_breaking_2: Minimum resulting size S.
  - action: draw_square
    center: point_B (yellow)
    size: S
    color: fill_color (red)
    target_grid: output grid
    rule: Fill background (white 0) pixels within the square area with red (2). Do not overwrite existing non-white pixels.

goal:
  description: For every yellow pixel in the input, find its closest gray pixel (using a specific tie-breaking rule based on resulting shape size), calculate a square size based on their relative positions, and draw a red square of that size centered on the yellow pixel onto the output grid, preserving original non-white pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the coordinates of all yellow pixels (color 4) and all gray pixels (color 5) in the input grid.
3.  If there are no yellow pixels or no gray pixels, stop and return the initialized output grid.
4.  For each yellow pixel `Y` at coordinates `(yr, yc)`:
    a. Calculate the Manhattan distance (`d = |yr - gr| + |yc - gc|`) from `Y` to every gray pixel `G` at coordinates `(gr, gc)`.
    b. Find the minimum Manhattan distance (`min_d`) among all calculated distances.
    c. Identify the set of all gray pixels (`closest_grays`) that are exactly `min_d` distance away from `Y`.
    d. Determine the side length `S` for the red square:
        i.  Initialize a variable `min_calculated_size` to a very large value.
        ii. For each gray pixel `G'` in `closest_grays` with coordinates `(gr', gc')`:
            1.  Calculate the row difference `dr' = |yr - gr'|`.
            2.  Calculate the column difference `dc' = |yc - gc'|`.
            3.  Calculate a potential size `s' = 2 * max(dr', dc') - 1`.
            4.  If `s'` is less than `min_calculated_size`, update `min_calculated_size` to `s'`.
        iii. Set the final side length `S` to `min_calculated_size`.
    e. Calculate the radius `r` of the square as `floor((S - 1) / 2)`.
    f. Iterate through each cell `(row, col)` in the grid, where `row` ranges from `yr - r` to `yr + r` and `col` ranges from `yc - r` to `yc + r`.
    g. For each cell `(row, col)`:
        i.  Check if the coordinates `(row, col)` are within the bounds of the output grid.
        ii. If the coordinates are valid and the pixel at `(row, col)` in the output grid is currently white (0), change its value to red (2).
5.  Return the final modified output grid.
