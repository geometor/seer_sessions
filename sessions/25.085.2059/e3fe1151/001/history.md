
## train_1

**input:**
```
7 1 7 8 0
0 8 7 7 1
7 7 7 7 7
8 7 7 7 1
0 1 7 8 5
```


**output:**
```
5 1 7 8 0
0 8 7 5 1
7 7 7 7 7
8 5 7 0 1
0 1 7 8 5
```


## train_2

**input:**
```
8 9 7 9 3
3 7 7 7 8
7 7 7 7 7
8 7 7 7 8
2 9 7 9 2
```


**output:**
```
8 9 7 9 3
3 2 7 2 8
7 7 7 7 7
8 3 7 3 8
2 9 7 9 2
```


## train_3

**input:**
```
7 4 7 4 5
4 3 7 7 3
7 7 7 7 7
5 7 7 4 3
3 4 7 5 7
```


**output:**
```
5 4 7 4 5
4 3 7 4 3
7 7 7 7 7
5 4 7 4 3
3 4 7 5 4
```

**Perception of the Elements:**

1.  **Grid Structure:** The task operates on a 5x5 grid of colored pixels.
2.  **Central Feature:** A prominent feature is the central cross formed by the middle row (row index 2) and the middle column (column index 2). This cross consists entirely of orange (7) pixels in the input.
3.  **Stability:** The central orange cross remains unchanged in the output grid. Pixels outside this cross may or may not change.
4.  **Key Transformation:** The primary transformation involves orange (7) pixels located *outside* the central cross.
5.  **Conditional Change:** These external orange pixels change based on their neighboring pixels (including diagonals).
    *   An orange (7) pixel changes to gray (5) if none of its 8 neighbors are gray (5).
    *   An orange (7) pixel changes to white (0) if at least one of its 8 neighbors is gray (5).
6.  **Other Pixels:** All other pixels (non-orange pixels outside the central cross) remain unchanged.

**Facts:**


```yaml
grid:
  size: 5x5
structure:
  - type: cross
    color: orange # 7
    location: central row (index 2) and central column (index 2)
    behavior: static (remains unchanged)
pixels_of_interest:
  - color: orange # 7
    location: outside the central cross
    behavior: conditional transformation based on neighbors
transformation_rule:
  - condition: pixel is orange (7) AND located outside the central cross
    actions:
      - if: any neighbor (orthogonal or diagonal) is gray (5)
        change_pixel_to: white (0)
      - else: # no neighbor is gray (5)
        change_pixel_to: gray (5)
  - condition: pixel is NOT orange (7) AND located outside the central cross
    actions:
      - change_pixel_to: original color (no change)
  - condition: pixel is part of the central cross
    actions:
      - change_pixel_to: original color (no change)
neighbor_definition: 8 adjacent cells (orthogonal and diagonal)
```


**Natural Language Program:**

1.  Identify the central row and central column of the input grid. These form the "central cross".
2.  Create the output grid as a copy of the input grid.
3.  Iterate through each pixel of the input grid, excluding those in the central cross.
4.  For each examined pixel:
    a.  If the pixel's color is orange (7):
        i.  Check all 8 neighboring pixels (orthogonal and diagonal).
        ii. If any neighbor's color is gray (5), change the corresponding pixel in the output grid to white (0).
        iii. If no neighbor's color is gray (5), change the corresponding pixel in the output grid to gray (5).
    b.  If the pixel's color is not orange (7), leave the corresponding pixel in the output grid unchanged (it retains its original color from the copy).
5.  The pixels within the central cross remain unchanged in the output grid (they retain their original orange color from the copy).
6.  Return the modified output grid.
