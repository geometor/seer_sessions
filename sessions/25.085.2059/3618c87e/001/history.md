
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 1 0 1 0
0 5 0 5 0
5 5 5 5 5
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 5 0 5 0
5 1 5 1 5
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 5 0 0
5 5 5 5 5
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 5 0 0
5 5 1 5 5
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 1 0 0 1
0 5 0 0 5
5 5 5 5 5
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 5 0 0 5
5 1 5 5 1
```

**Perception:**

1.  **Grid Size:** All examples use a 5x5 grid.
2.  **Colors Present:** The grids contain white (0), blue (1), and gray (5) pixels.
3.  **Input Structure:**
    *   The top rows are mostly white (0).
    *   There are one or more blue (1) pixels located somewhere in the middle rows.
    *   Often, there is a gray (5) pixel directly below each blue (1) pixel.
    *   The bottom row (row index 4) is consistently filled with gray (5) pixels.
4.  **Output Structure:**
    *   The original positions of the blue (1) pixels become white (0).
    *   The gray (5) pixels that were initially below the blue pixels (if present) remain in their positions.
    *   The blue (1) pixels appear in the bottom row (row index 4), specifically in the same columns where they originated. The original gray (5) pixels in those bottom-row positions are replaced by blue (1).
    *   All other pixels remain unchanged from the input.
5.  **Transformation Logic:** The core transformation appears to be a "gravity" or "teleportation" effect specifically for the blue pixels. Each blue pixel moves from its starting position directly down to the last row of the grid within the same column. Its original position is cleared (becomes white), and it overwrites whatever color was in the destination cell in the last row. All non-blue pixels remain stationary.

**Facts:**


```yaml
task_context:
  grid_dimensions: ثابت 5x5 grid for all examples.
  colors_involved: white (0), blue (1), gray (5).
  background_color: white (0).
elements:
  - object: blue_pixel
    color: 1
    count: variable (1 or 2 in examples)
    initial_position: rows 2 or 3, variable columns.
    action: moves vertically downwards within its column.
    destination: the cell in the bottom-most row of the same column.
    effect_on_origin: origin cell becomes white (0).
    effect_on_destination: destination cell becomes blue (1), overwriting previous content.
  - object: gray_pixel
    color: 5
    count: variable
    initial_position: often below blue pixels, always fills the bottom row.
    action: remains stationary.
relationships:
  - type: spatial
    description: Blue pixels often have a gray pixel directly below them in the input.
  - type: spatial
    description: The bottom row is always entirely gray in the input.
  - type: transformation
    description: Each blue pixel's final row position is the last row of the grid.
  - type: transformation
    description: Each blue pixel's final column position is the same as its initial column position.
  - type: transformation
    description: Gray pixels do not move. White pixels (other than those resulting from moved blue pixels) do not change.
```


**Natural Language Program:**

1.  Initialize the output grid as an exact copy of the input grid.
2.  Get the height of the grid and determine the index of the bottom row (height - 1).
3.  Iterate through each cell `(row, column)` of the input grid.
4.  If a cell at `(row, column)` contains a blue pixel (color 1):
    a.  Change the pixel at `(row, column)` in the *output* grid to white (color 0).
    b.  Change the pixel at `(bottom_row_index, column)` in the *output* grid to blue (color 1).
5.  Return the modified output grid.
