
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 4 0 0 0
8 0 0 0 4 4 4 4 0 0
8 8 8 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 8 8 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0
8 8 8 8 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 4 0 0
8 0 0 0 0 4 4 4 4 0
8 8 8 0 0 0 0 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 3 3 3
0 3 3 0 0 0 0 0 0 0
0 3 3 0 4 4 4 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 4 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
3 3 3 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 3 3 0 4 4 4 0 0
3 3 0 0 0 0 4 4 0 0
3 3 0 0 0 0 4 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 9 9 9 0
7 7 7 7 0 0 9 9 9 0
0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 9 9 9 0 0
0 7 7 0 0 9 9 9 0 0
7 7 7 7 0 0 0 0 0 0
0 7 7 0 0 9 9 9 9 9
```


## train_4

**input:**
```
0 0 0 1 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
6 6 0 0 0 0 6 6 0 0
6 6 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 1 0 0 0 0 0
6 6 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 0 0 1 1 1 0 0 0
6 6 0 1 1 1 1 0 0 0
```

**Perception**

1.  **Input/Output Structure:** Both input and output are 2D grids of pixels with values 0-9 representing colors. The background is predominantly white (0).
2.  **Objects:** The non-white pixels form distinct, contiguous objects of various shapes and colors (Azure, Yellow, Green, Orange, Maroon, Blue, Magenta).
3.  **Transformation:** The core transformation appears to be a vertical downward shift of all non-white pixels.
4.  **Gravity Effect:** The pixels seem to "fall" within their respective columns until they either hit the bottom edge of the grid or land on top of another non-white pixel that has already settled in that column.
5.  **Object Integrity:** The relative shapes of the objects are maintained during the fall, although their absolute positions change. Objects do not merge or change color.
6.  **Column Independence:** The movement within each column seems independent of the movement in other columns. Pixels only interact vertically within their own column.

**Facts**


```yaml
Context:
  - The task operates on a 2D grid of pixels.
  - Pixels have a color attribute (represented by integers 0-9).
  - Pixels at value 0 (white) represent the background.
  - Pixels with values 1-9 represent colored elements.

Objects:
  - Colored Objects: Contiguous blocks of pixels with the same non-zero color.
  - Individual Colored Pixels: Can be considered the fundamental units affected by the transformation.

Properties:
  - Position: Each pixel has a row and column index.
  - Color: Each pixel has a color value.

Relationships:
  - Adjacency: Pixels can be adjacent horizontally, vertically, or diagonally. (Relevant for object definition, but less so for the core transformation logic).
  - Vertical Stacking: In the output, colored pixels within the same column are stacked vertically from the bottom upwards.

Action:
  - Apply Gravity: Non-white pixels move downwards within their column.
  - Stop Condition: A pixel stops moving when it reaches the bottom row of the grid or the row immediately above another non-white pixel in the same column.

Constraints:
  - Movement is strictly vertical (within the same column).
  - The relative vertical order of pixels originating from the same column is preserved.
  - White pixels (0) are unaffected and act as empty space.
```


**Natural Language Program**

1.  Create a new output grid of the same dimensions as the input grid, initialized with the background color (white, 0).
2.  Iterate through each column of the input grid from left to right (column index `c`).
3.  For the current column `c`, collect all non-white pixels, preserving their original color and their relative vertical order (from top to bottom as they appeared in the input column).
4.  Place these collected non-white pixels into the corresponding column `c` of the output grid, starting from the bottom row and moving upwards, maintaining their collected relative order. Fill the remaining cells above the placed pixels in that column with the background color (white, 0).
5.  Repeat steps 3 and 4 for all columns.
6.  The resulting grid is the final output.
