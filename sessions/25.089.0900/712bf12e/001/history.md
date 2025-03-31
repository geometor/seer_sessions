
## train_1

**input:**
```
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 5 5 0 0 0 0 0 0
5 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 5
0 0 0 0 5 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 5 5
0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 5 0 0 5 0 0 0 0
0 5 0 0 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0 5 0 0
0 0 2 0 0 2 0 0 0 2 0 0 0
```


**output:**
```
0 5 0 2 0 0 0 0 0 5 2 0 0
0 5 0 2 0 5 5 0 0 2 2 0 0
5 0 0 2 0 0 2 5 0 2 0 5 0
0 0 0 2 0 5 2 0 0 2 0 0 0
0 0 0 2 5 0 2 0 0 2 0 0 5
0 0 0 2 5 0 2 0 0 2 0 0 0
5 0 0 2 0 0 2 0 0 2 0 5 5
0 0 5 2 0 0 2 0 0 2 0 0 0
0 0 5 2 0 5 2 0 5 2 0 0 0
0 5 2 2 5 2 2 5 0 2 0 0 0
0 0 2 0 0 2 5 5 0 2 5 0 0
0 0 2 0 0 2 0 0 0 2 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 5 5 0 0 0 5 5 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 5 0 0 0
0 5 5 0 0 0 0 0 0 5 0 0 0 0
5 0 5 0 0 5 0 0 0 0 0 0 0 5
5 0 0 0 5 0 5 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 5 0 0 0 5 0 0 0 5 5 0 0
0 0 0 0 0 0 0 5 0 5 5 0 0 0
5 0 2 0 0 2 0 5 5 0 2 0 0 0
```


**output:**
```
0 0 0 0 2 0 5 0 0 0 5 0 0 2
0 0 0 0 2 0 0 0 5 0 0 0 5 2
0 0 0 0 2 0 0 0 0 0 0 5 2 2
0 0 5 5 2 0 0 5 5 0 0 0 2 0
0 0 5 5 2 0 0 0 0 0 0 0 2 0
0 0 0 2 2 0 5 0 0 0 5 0 2 0
0 5 5 2 0 0 0 0 0 5 0 0 2 0
5 0 5 2 0 5 0 0 0 0 0 0 2 5
5 0 0 2 5 2 5 0 0 0 0 0 2 0
5 0 0 2 0 2 0 0 0 0 5 0 2 0
0 0 5 2 0 2 5 0 0 0 5 5 2 0
0 0 2 2 0 2 0 5 0 5 5 2 2 0
5 0 2 0 0 2 0 5 5 0 2 2 0 0
```


## train_3

**input:**
```
0 5 0 0 0 0 0 5 0 0 0 0 0 5 5
0 5 0 0 0 0 0 0 0 0 5 0 0 5 0
5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0 0 0 0
0 5 5 5 5 0 0 0 0 0 5 0 0 5 0
5 5 0 0 0 0 0 5 0 5 5 0 0 0 5
0 5 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 0 0 0 0 5 0 0 0 0 0
0 5 0 0 0 0 0 5 0 0 5 0 5 0 0
0 5 5 0 0 0 5 0 0 0 5 0 0 0 0
0 0 5 0 0 0 0 0 0 5 5 0 5 0 0
0 5 5 2 0 0 0 2 0 2 0 0 5 5 0
```


**output:**
```
0 5 0 0 0 2 0 5 0 2 0 0 2 5 5
0 5 0 0 0 2 0 0 0 2 5 0 2 5 0
5 0 0 0 0 2 0 0 0 2 0 0 2 0 0
0 0 0 0 5 2 0 0 0 2 0 5 2 0 0
0 0 0 0 0 2 0 0 5 2 5 2 2 0 0
0 5 5 5 5 2 0 0 2 2 5 2 0 5 0
5 5 0 0 0 2 0 5 2 5 5 2 0 0 5
0 5 0 0 0 2 0 0 2 0 5 2 0 0 0
0 0 0 5 5 2 0 0 2 5 0 2 0 0 0
0 5 0 2 2 2 0 5 2 0 5 2 5 0 0
0 5 5 2 0 0 5 2 2 0 5 2 0 0 0
0 0 5 2 0 0 0 2 0 5 5 2 5 0 0
0 5 5 2 0 0 0 2 0 2 2 2 5 5 0
```

Okay, let's analyze the provided examples.

**Perception of Task Elements:**

1.  **Grid Structure:** The input and output are 2D grids of varying sizes.
2.  **Colors:** The relevant colors are white (0), gray (5), and red (2). White appears to be the background. Gray pixels are present in specific locations in the input and persist in the same locations in the output. Red pixels exist in the input, usually in a single row near the bottom, and additional red pixels appear in the output.
3.  **Objects:** Gray pixels (5) seem to form static "obstacles" or "barriers". Red pixels (2) in the input act as "sources".
4.  **Transformation:** The core transformation involves adding new red pixels to the grid. These new red pixels always appear vertically *above* the red pixels present in the input grid.
5.  **Mechanism:** The red color appears to "flow" or "fill" upwards from each red pixel found in the input. This upward flow continues through white (0) pixels but is blocked by gray (5) pixels. If the flow reaches the top edge of the grid, it stops there.
6.  **Independence:** The filling process in each column seems independent of other columns, dictated only by the initial red pixel in that column (if any) and the gray obstacles above it.

**YAML Facts:**


```yaml
Grid:
  Type: 2D array of integers (pixels)
  Colors:
    - White (0): Background
    - Gray (5): Obstacles, static
    - Red (2): Source color and fill color
Input:
  Features:
    - Contains scattered Gray pixels.
    - Contains a small number of Red pixels, often located near the bottom row.
Output:
  Relationship to Input:
    - Preserves the original positions of Gray pixels.
    - Preserves the original positions of Red pixels from the input.
    - Adds new Red pixels.
Transformation:
  Action: Vertical upward fill
  Source: Each Red pixel in the input grid.
  Target: White pixels located directly above a source Red pixel or another newly filled Red pixel within the same column.
  Condition: The fill continues upwards in a column until it encounters:
    - A Gray pixel (obstacle) immediately above.
    - The top boundary of the grid.
  Color Change: White (0) pixels targeted by the fill become Red (2).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the locations (row, column) of all red (2) pixels in the input grid. These are the initial "source" pixels.
3.  For each column that contains at least one source red pixel:
    a.  Iterate upwards from each source red pixel in that column (i.e., decrease the row index).
    b.  At each step `(current_row, column)`, examine the pixel directly above at `(current_row - 1, column)`.
    c.  If the pixel above exists (`current_row > 0`) and is white (0), change its color in the output grid to red (2) and continue the upward check from this new red pixel's position `(current_row - 1, column)`.
    d.  If the pixel above does not exist (i.e., `current_row` is 0, the top row) or if the pixel above is gray (5), stop the upward fill for this specific vertical path originating from the initial source pixel.
4.  Repeat step 3 until no more white pixels can be changed to red according to the rules.
5.  The final state of the output grid is the result.
