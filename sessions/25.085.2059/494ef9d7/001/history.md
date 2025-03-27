
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

## Perception of Task Elements

1.  **Grid Structure:** The input and output are grids of the same dimensions. The background is consistently white (0).
2.  **Objects:** The primary objects are individual pixels with colors other than white (values 1-9). They appear sparsely distributed.
3.  **Transformation:** Comparing input and output grids reveals that most pixels remain unchanged. The changes involve the horizontal movement of *some* colored pixels within their rows.
4.  **Movement Pattern:**
    *   The movement is always horizontal, from right to left within a single row.
    *   A pixel that moves leaves its original position, which becomes white (0).
    *   The moving pixel stops immediately to the right of another non-white pixel in the same row.
5.  **Condition for Movement:** By examining all examples, the movement seems conditional:
    *   It only occurs in rows containing *exactly two* non-white pixels.
    *   Furthermore, it only occurs for specific *pairs* of colors. Let the left pixel have color `C1` and the right pixel have color `C2`. Movement happens only if the pair (`C1`, `C2`) is one of:
        *   (blue(1), azure(8))
        *   (azure(8), blue(1))
        *   (yellow(4), orange(7))
        *   (orange(7), yellow(4))
    *   If a row has exactly two non-white pixels, but the color pair (left, right) is *not* one of the above, no movement occurs (e.g., train_2 row 1: (maroon(9), red(2)); train_4 row 2: (magenta(6), orange(7))).
    *   Rows with 0, 1, or more than 2 non-white pixels are never modified.

## YAML Fact Document


```yaml
elements:
  - element: grid
    description: A 2D array of pixels representing colors (0-9). Constant dimensions between input and output.
  - element: pixel
    description: A single cell in the grid.
    properties:
      - color: Integer value 0-9. 0 is background (white). 1-9 are distinct colors.
      - position: (row, column) coordinates.
  - element: row
    description: A horizontal line of pixels in the grid.
    properties:
      - non_white_pixels: A list of pixels in the row with color > 0.
      - count_non_white: The number of non-white pixels in the row.

transformation:
  - scope: row-by-row
    description: The grid transformation is applied independently to each row.
  - condition:
      description: A transformation applies to a row only if it meets specific criteria.
      criteria:
        - count_non_white == 2
        - Let the two non-white pixels be P1 (left, color C1, col1) and P2 (right, color C2, col2).
        - The pair of colors (C1, C2) must be one of {(1, 8), (8, 1), (4, 7), (7, 4)}.
          (blue, azure), (azure, blue), (yellow, orange), (orange, yellow).
  - action:
      description: If the condition is met, the right pixel (P2) moves left.
      steps:
        - Identify the positions (row, col1) and (row, col2) and colors C1, C2.
        - Change the pixel at (row, col2) in the output grid to white (0).
        - Change the pixel at (row, col1 + 1) in the output grid to color C2.
  - default:
      description: If the condition is not met for a row, the row remains unchanged in the output grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid, identified by its `row_index`.
3.  For the current row, find all non-white pixels, storing their color and column index. Let this list be `pixels`.
4.  Check if the number of pixels in the `pixels` list is exactly two.
5.  If there are exactly two pixels, let the left pixel be `P1` (with `color1` at `col1`) and the right pixel be `P2` (with `color2` at `col2`).
6.  Determine if the pair of colors (`color1`, `color2`) is one of the following "active pairs": (blue(1), azure(8)), (azure(8), blue(1)), (yellow(4), orange(7)), or (orange(7), yellow(4)).
7.  If the pair (`color1`, `color2`) is one of the active pairs:
    a.  Update the output grid at `(row_index, col2)` by setting its color to white (0).
    b.  Update the output grid at `(row_index, col1 + 1)` by setting its color to `color2`.
8.  If the number of non-white pixels is not two, or if the color pair is not an active pair, make no changes to the current row in the output grid.
9.  After processing all rows, return the final output grid.
