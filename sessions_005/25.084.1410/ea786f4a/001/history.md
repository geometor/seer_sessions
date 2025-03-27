
## train_1

**input:**
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```


**output:**
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```


## train_2

**input:**
```
1 1 1
1 0 1
1 1 1
```


**output:**
```
0 1 0
1 0 1
0 1 0
```


## train_3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```


**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

Okay, let's break down this task.

**Perception:**

Each example consists of an input grid and an output grid of the same dimensions. The input grids predominantly feature one color (red, blue, or green) with a single white pixel located somewhere within the grid. The output grids also contain the original white pixel, but additional pixels have been changed to white. The pattern of these new white pixels seems related to their position relative to the original white pixel. Specifically, the pixels that become white in the output appear to form a pattern based on their distance from the initial white pixel. Calculating the Manhattan distance (`|row1 - row2| + |col1 - col2|`) between each pixel and the original white pixel reveals that pixels with an *even* Manhattan distance become white in the output, while pixels with an *odd* Manhattan distance retain their original color (which is the background color, since the only other input color is white at distance 0).

**Facts:**


```yaml
Task: Color pixels based on Manhattan distance parity from a specific point.

Input:
  - type: grid
  - properties:
      - contains pixels of a single background color (e.g., red, blue, green)
      - contains exactly one white (0) pixel, acting as a reference point.

Output:
  - type: grid
  - properties:
      - same dimensions as the input grid.
      - pixels at coordinates (r, c) are white (0) if the Manhattan distance `|r - r0| + |c - c0|` from the reference white pixel at (r0, c0) is even.
      - pixels at coordinates (r, c) retain their original color from the input grid if the Manhattan distance `|r - r0| + |c - c0|` from the reference white pixel at (r0, c0) is odd.

Relationships:
  - The position of the single white pixel in the input determines the pattern in the output.
  - The color of each output pixel depends on its Manhattan distance parity relative to the input white pixel.
```


**Natural Language Program:**

1.  Find the coordinates (row `r0`, column `c0`) of the unique white pixel (value 0) in the input grid.
2.  Create a new grid with the same dimensions as the input grid.
3.  For each pixel at position (row `r`, column `c`) in the input grid:
    a.  Calculate the Manhattan distance `d` to the white pixel: `d = absolute_difference(r, r0) + absolute_difference(c, c0)`.
    b.  Check if `d` is an even number.
    c.  If `d` is even, set the pixel at `(r, c)` in the new grid to white (0).
    d.  If `d` is odd, copy the color of the pixel at `(r, c)` from the input grid to the new grid.
4.  The new grid is the output.
