
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 4 4 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 6 0 0 6 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0
6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception**

Observing the input and output grids in both examples, the core transformation appears to be a form of "gravity" acting vertically within each column.

1.  **Color Preservation:** The colors of the non-white pixels (yellow in example 1, magenta in example 2) remain unchanged from input to output.
2.  **Vertical Movement:** Non-white pixels move downwards. White pixels (0) seem to represent empty space through which other pixels can fall.
3.  **Column Independence:** The movement happens independently within each column. A pixel in one column does not affect the movement of pixels in other columns.
4.  **Stacking:** When a non-white pixel falls, it stops when it reaches the bottom edge of the grid or rests on top of another non-white pixel within the same column.
5.  **Order Preservation (within column):** Although pixels fall, their relative vertical order within a column seems to be preserved if you read the non-white pixels from top to bottom in the input and compare them to the stacked pixels read from top to bottom in the output. However, it's simpler to think of it as collecting all non-white pixels in a column and stacking them at the bottom.
6.  **Grid Size:** The dimensions (height and width) of the grid remain constant.

**Facts**


```yaml
task_context:
  - The transformation simulates vertical gravity independently within each column of the grid.
  - The grid dimensions remain unchanged.
objects:
  - name: grid
    properties:
      - type: 2D array
      - pixels: cells containing integer values (0-9) representing colors
      - dimensions: height, width
  - name: pixel
    properties:
      - color: integer value (0-9)
      - position: row, column
      - type: white (0) or non-white (1-9)
  - name: column
    properties:
      - index: integer representing the vertical slice of the grid
      - contains: sequence of pixels
actions:
  - identify: locate all non-white pixels in the input grid.
  - collect: gather the non-white pixels for each column separately.
  - stack: place the collected non-white pixels at the bottom of their respective columns in the output grid.
  - fill: ensure all remaining positions above the stacked pixels in each column are filled with white (0).
relationships:
  - spatial: pixels exist within columns; columns make up the grid.
  - transformation: input grid pixels determine output grid pixels based on the gravity rule.
  - column_constraint: gravity acts solely within the boundaries of each column.
```


**Natural Language Program**

1.  Initialize a new output grid with the same dimensions as the input grid, filled entirely with the white color (0).
2.  Process each column of the input grid independently, from left to right.
3.  For the current column:
    a.  Scan the column from top to bottom and collect the colors of all non-white pixels encountered into a temporary list, preserving their top-to-bottom order.
    b.  Determine the number of non-white pixels collected (`count`).
    c.  Starting from the bottom row (`row = height - 1`) of the output grid's current column and moving upwards for `count` rows:
        i.  Place the collected colors sequentially (from the temporary list) into the output grid cells `(row, column)`.
4.  Once all columns are processed, the resulting output grid represents the final state after gravity has been applied.
