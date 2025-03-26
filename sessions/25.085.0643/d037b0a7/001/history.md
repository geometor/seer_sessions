
## train_1

**input:**
```
0 2 0
7 0 8
0 0 0
```


**output:**
```
0 2 0
7 2 8
7 2 8
```


## train_2

**input:**
```
0 0 6
0 4 0
3 0 0
```


**output:**
```
0 0 6
0 4 6
3 4 6
```


## train_3

**input:**
```
4 0 0
0 2 0
0 0 0
```


**output:**
```
4 0 0
4 2 0
4 2 0
```

Okay, let's analyze the provided examples.

**Perception**

The task involves transforming an input grid into an output grid of the same dimensions. Observing the examples, it appears that non-white pixels (colors other than 0) have an effect on the white pixels (color 0) located directly below them within the same column. Specifically, if a cell contains a non-white color, any white cell immediately below it adopts that color. This effect propagates downwards within the column, essentially "staining" or "filling" the white space below a colored pixel with that same color. The process occurs independently for each column. If a cell is white and the cell directly above it is also white, it remains white unless affected by a color further up in the column.

**Facts**


```yaml
task_context:
  grid_dimensions: Input and output grids have the same height and width.
  colors: The transformation involves white (0) and various other colors (non-zero).
  background_color: White (0) acts as the background or empty space.
objects:
  - type: pixel
    properties:
      - color: An integer from 0 to 9.
      - position: (row, column) coordinates.
      - is_colored: Boolean (True if color is not 0, False otherwise).
actions:
  - name: fill_down
    description: A non-white pixel's color propagates downwards into adjacent white pixels within the same column.
    conditions:
      - The target pixel must be white (0).
      - The pixel directly above the target pixel must be non-white.
    effect: The target pixel's color changes to match the color of the pixel directly above it.
relationships:
  - type: vertical_adjacency
    description: Pixels in the same column, one directly above the other.
  - type: column_independence
    description: The transformation process within one column does not directly affect other columns.
  - type: propagation
    description: The color-filling effect cascades downwards. If cell (r-1, c) colors cell (r, c), and cell (r+1, c) is white, then cell (r+1, c) will subsequently be colored by the new color at (r, c).
```


**Natural Language Program**

1.  Initialize the output grid as an exact copy of the input grid.
2.  Iterate through each column `c` of the grid.
3.  Within each column `c`, iterate through the rows `r` starting from the second row (index 1) down to the last row (index `height - 1`).
4.  For each cell at `(r, c)`:
    a.  Check if the cell `(r, c)` in the current output grid is white (color 0).
    b.  If it is white, check the color of the cell directly above it, at `(r-1, c)`, in the current output grid.
    c.  If the cell above `(r-1, c)` is *not* white, update the color of the current cell `(r, c)` in the output grid to match the color of the cell above `(r-1, c)`.
5.  After iterating through all specified cells, the resulting output grid is the final transformed grid.
