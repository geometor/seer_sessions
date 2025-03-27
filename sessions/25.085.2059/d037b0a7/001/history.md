
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

Okay, let's break down this task.

## Perception

1.  **Grid Structure:** The input and output are both grids of the same dimensions (3x3 in all examples).
2.  **Color Palette:** The grids use colors represented by integers 0-9. White (0) seems to act as a background or empty space. Other colors (red, orange, azure, magenta, yellow, green) are present.
3.  **Transformation Pattern:** The transformation appears to operate column by column. Within each column, there's a downward propagation or filling effect.
4.  **Source Pixels:** The non-white pixels in the input seem to act as the source of color for the filling process.
5.  **Filling Logic:** In each column, the color of the *topmost* non-white pixel seems to determine the color used for filling downwards. All pixels below this topmost non-white pixel (including itself if it was originally white, but that doesn't happen in the examples) are filled with that color down to the bottom of the grid.
6.  **Empty Columns:** If a column contains only white pixels, it remains unchanged (as seen implicitly in train_3, column 2).
7.  **Overwriting:** The filling process overwrites existing white pixels and potentially other non-white pixels if they are below the topmost non-white pixel in that column (though the latter case isn't explicitly shown, the logic implies it).

## Facts


```yaml
task_type: grid_transformation
dimensionality: 2D
grid_properties:
  size_relation: input and output grids have identical dimensions
  color_palette: integers 0-9, with 0 (white) acting as a background/empty state
transformation_scope: column-wise, independent for each column
objects:
  - type: pixel
    properties:
      - color (integer 0-9)
      - position (row, column)
  - type: column
    properties:
      - contains pixels
      - index
actions:
  - name: find_topmost_non_white_pixel
    inputs: column
    outputs:
      - color of the pixel (if found)
      - row index of the pixel (if found)
      - flag indicating if found
  - name: fill_downwards
    inputs:
      - column index
      - starting row index
      - fill color
      - grid height
    outputs: modified column segment
relationships:
  - type: vertical_adjacency
    description: Pixels within the same column are vertically adjacent.
  - type: propagation
    description: The color of the topmost non-white pixel in a column propagates downwards to fill cells below it in the output grid.
rule_logic:
  - For each column, identify the first non-white pixel encountered scanning from top to bottom.
  - If a non-white pixel is found, its color is used.
  - All pixels in that column, starting from the row where the first non-white pixel was found down to the last row, are set to that color in the output grid.
  - If a column contains only white pixels, it remains unchanged in the output grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Get the height and width of the grid.
3.  Iterate through each column index `c` from 0 to `width - 1`.
4.  Within each column `c`, search for the topmost non-white pixel:
    *   Initialize `found_color = None` and `found_row = -1`.
    *   Iterate through each row index `r` from 0 to `height - 1`.
    *   Check the color of the pixel at `(r, c)` in the *input* grid.
    *   If the color is not white (0), set `found_color` to this color, set `found_row` to `r`, and break the inner row loop (since we only care about the topmost one).
5.  If a non-white pixel was found in the column (i.e., `found_row != -1`):
    *   Iterate through the rows `r_fill` from `found_row` down to `height - 1`.
    *   Set the color of the pixel at `(r_fill, c)` in the *output* grid to `found_color`.
6.  After iterating through all columns, the modified output grid is the result.
