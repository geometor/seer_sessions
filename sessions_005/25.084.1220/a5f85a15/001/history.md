
## train_1

**input:**
```
0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 9 0 0
9 0 0 0 0 0 9 0
0 9 0 0 0 0 0 9
0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0
```


**output:**
```
0 0 9 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 4 0 0
9 0 0 0 0 0 9 0
0 4 0 0 0 0 0 4
0 0 9 0 0 0 0 0
0 0 0 4 0 0 0 0
```


## train_2

**input:**
```
2 0 0
0 2 0
0 0 2
```


**output:**
```
2 0 0
0 4 0
0 0 2
```


## train_3

**input:**
```
0 0 3 0 0 0
0 0 0 3 0 0
0 0 0 0 3 0
3 0 0 0 0 3
0 3 0 0 0 0
0 0 3 0 0 0
```


**output:**
```
0 0 3 0 0 0
0 0 0 4 0 0
0 0 0 0 3 0
3 0 0 0 0 4
0 4 0 0 0 0
0 0 3 0 0 0
```

Okay, let's analyze the task examples.

## Perception

1.  **Grid Structure:** Each example consists of an input grid and an output grid of the same dimensions.
2.  **Pixel Colors:** The grids contain a background color (white, 0) and sparsely distributed pixels of a single other color (maroon 9 in ex 1, red 2 in ex 2, green 3 in ex 3).
3.  **Transformation:** The transformation modifies the color of *some* of the non-white pixels to yellow (4). The background pixels (white, 0) remain unchanged.
4.  **Positional Dependence:** The decision to change a pixel's color seems to depend on its position (row and column index) within the grid.
5.  **Pattern:** Comparing the coordinates of pixels that change color versus those that don't reveals a consistent pattern across all examples: Non-white pixels located in columns with an *odd* index change their color to yellow (4). Non-white pixels in columns with an *even* index retain their original color.

## Facts


```yaml
task_description: Modify the color of certain non-background pixels based on their column position.
grid_properties:
  - dimension_preservation: Input and output grids have the same height and width.
  - background_color: White (0) pixels remain unchanged.
objects:
  - type: foreground_pixel
    description: A pixel with a color other than white (0).
    properties:
      - initial_color: The color of the pixel in the input grid (e.g., 9, 2, 3).
      - position: Coordinates (row, column) within the grid.
      - column_parity: Whether the column index is 'even' or 'odd'.
transformation:
  - type: conditional_color_change
    input: foreground_pixel
    condition: The 'column_parity' of the foreground_pixel's position is 'odd'.
    action: Change the pixel's color to yellow (4).
    condition_else: The 'column_parity' of the foreground_pixel's position is 'even'.
    action_else: Keep the pixel's 'initial_color'.
```


## Natural Language Program

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each pixel of the input grid using its row index `r` and column index `c`.
3.  Get the color `color` of the pixel at `(r, c)`.
4.  Check if the `color` is white (0).
    *   If yes, set the color of the corresponding pixel `(r, c)` in the new grid to white (0).
5.  If the `color` is not white (0):
    *   Check if the column index `c` is odd (i.e., `c % 2 != 0`).
    *   If `c` is odd, set the color of the corresponding pixel `(r, c)` in the new grid to yellow (4).
    *   If `c` is even, set the color of the corresponding pixel `(r, c)` in the new grid to its original `color`.
6.  Return the new grid as the output.
