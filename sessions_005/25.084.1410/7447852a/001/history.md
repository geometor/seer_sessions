
## train_1

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
```


**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2
```


## train_2

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

Okay, let's break down this task.

## Perception

1.  **Input/Output Structure:** Both input and output are grids of the same dimensions (height 3, variable width).
2.  **Colors:**
    *   Input grids contain only white (0) and red (2) pixels.
    *   Output grids contain white (0), red (2), and yellow (4) pixels.
3.  **Transformation:** The core transformation involves changing *some* white pixels to yellow pixels. The red pixels remain unchanged in position and color.
4.  **Pattern Identification:** The change from white to yellow depends on the local neighborhood of the white pixel in the input grid. Specifically, it relates to the number and arrangement of neighboring red pixels.
5.  **Rule Discovery:** By examining the examples, it appears that a white pixel changes to yellow if and only if it has exactly two red neighbors, and these two red neighbors are diagonally opposite each other relative to the white pixel's position. For a white pixel at `(r, c)`, its red neighbors must be at `(r-1, c-1)` and `(r+1, c+1)` OR at `(r-1, c+1)` and `(r+1, c-1)`. All other pixels retain their original color.

## Facts


```yaml
elements:
  - element: grid
    description: A 2D array of pixels representing the input and output.
    properties:
      - height: 3 (constant across examples)
      - width: Variable (15, 10, 18 in examples)
      - pixels: Contains pixels with specific colors and positions.

  - element: pixel
    description: A single cell within the grid.
    properties:
      - color: Integer value (0-9), representing white, red, or yellow in this task.
      - position: Coordinates (row, column) within the grid.
      - neighbors: The 8 pixels directly or diagonally adjacent to the pixel.

relationships:
  - relationship: adjacency
    description: Pixels can be neighbors (horizontally, vertically, or diagonally).
  - relationship: diagonal_opposition
    description: Two neighboring pixels are diagonally opposite relative to a central pixel. (e.g., top-left and bottom-right neighbors relative to the center).

transformation:
  - action: iterate_pixels
    description: Process each pixel in the input grid one by one.
  - action: check_condition
    description: For each white pixel, check its neighbors.
    conditions:
      - color is white (0).
      - count of red (2) neighbors is exactly 2.
      - the two red neighbors are diagonally opposite each other relative to the white pixel.
  - action: change_color
    description: If the conditions are met for a white pixel, change its color to yellow (4) in the output grid.
  - action: copy_color
    description: If the conditions are not met, or if the pixel is not white, copy its original color to the output grid.

constants:
  - white: 0
  - red: 2
  - yellow: 4
```


## Natural Language Program

1.  Create a new output grid with the same dimensions as the input grid.
2.  Iterate through each pixel `(r, c)` of the input grid.
3.  Get the color of the current pixel `input[r][c]`.
4.  **If** the color of the current pixel `input[r][c]` is white (0):
    a.  Examine the 8 neighbors of the pixel at `(r, c)`. Be mindful of grid boundaries.
    b.  Count the number of neighbors that are red (2).
    c.  Initialize a flag `is_diagonal_pair` to false.
    d.  **If** the count of red neighbors is exactly 2:
        i.  Check if the neighbors at `(r-1, c-1)` and `(r+1, c+1)` are both red (within bounds). If yes, set `is_diagonal_pair` to true.
        ii. Check if the neighbors at `(r-1, c+1)` and `(r+1, c-1)` are both red (within bounds). If yes, set `is_diagonal_pair` to true.
    e.  **If** `is_diagonal_pair` is true:
        i.  Set the color of the corresponding pixel `output[r][c]` to yellow (4).
    f.  **Else** (the count wasn't 2 or they weren't a diagonal pair):
        i.  Set the color of the corresponding pixel `output[r][c]` to white (0) (copy the original color).
5.  **Else** (the color of the current pixel `input[r][c]` is not white):
    a.  Copy the original color from `input[r][c]` to `output[r][c]`.
6.  Return the completed output grid.
