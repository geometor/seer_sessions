
## train_1

**input:**
```
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
```


**output:**
```
0 0 0 0 0
0 0 0 3 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 2 0
0 0 0 0 0
```


**output:**
```
0 0 3 0 6
0 0 0 0 0
0 0 8 0 7
```


## train_4

**input:**
```
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
```


**output:**
```
3 0 6 0 0
0 0 0 0 0
8 0 7 0 0
```

**Perception:**

The input grids are 3x5 and contain a single red pixel (2) on a white background (0). The output grids are also 3x5, but the red pixel is replaced, and new colored pixels appear around the original red pixel's location. Specifically, green (3), magenta (6), azure (8), and orange (7) pixels are placed in positions diagonally adjacent to where the red pixel was.

*   Green (3) appears diagonally Up-Left.
*   Magenta (6) appears diagonally Up-Right.
*   Azure (8) appears diagonally Down-Left.
*   Orange (7) appears diagonally Down-Right.

The placement of these new pixels is conditional on whether the target diagonal position falls within the grid boundaries. If a diagonal position is outside the grid, the corresponding colored pixel is not placed. The original position of the red pixel becomes white in the output.

**Facts:**


```yaml
task_description: Place specific colored pixels diagonally around a single red pixel, respecting grid boundaries.
grid_size:
  input: 3x5 (constant across examples)
  output: 3x5 (constant across examples)
objects:
  input:
    - object: red_pixel
      color: 2 (red)
      count: 1
      location: variable
    - object: background
      color: 0 (white)
  output:
    - object: green_pixel
      color: 3 (green)
      count: 0 or 1
      location: relative to red_pixel (up-left diagonal)
    - object: magenta_pixel
      color: 6 (magenta)
      count: 0 or 1
      location: relative to red_pixel (up-right diagonal)
    - object: azure_pixel
      color: 8 (azure)
      count: 0 or 1
      location: relative to red_pixel (down-left diagonal)
    - object: orange_pixel
      color: 7 (orange)
      count: 0 or 1
      location: relative to red_pixel (down-right diagonal)
    - object: background
      color: 0 (white)
transformation_rule:
  - action: find
    target: red_pixel (color 2)
    variable: red_pos
  - action: create
    target: output_grid
    properties:
      size: same as input_grid
      initial_color: 0 (white)
  - action: check_and_place
    conditions:
      - position: (red_pos.row - 1, red_pos.col - 1) is within grid bounds
    actions:
      - place: green_pixel (color 3) at (red_pos.row - 1, red_pos.col - 1) in output_grid
  - action: check_and_place
    conditions:
      - position: (red_pos.row - 1, red_pos.col + 1) is within grid bounds
    actions:
      - place: magenta_pixel (color 6) at (red_pos.row - 1, red_pos.col + 1) in output_grid
  - action: check_and_place
    conditions:
      - position: (red_pos.row + 1, red_pos.col - 1) is within grid bounds
    actions:
      - place: azure_pixel (color 8) at (red_pos.row + 1, red_pos.col - 1) in output_grid
  - action: check_and_place
    conditions:
      - position: (red_pos.row + 1, red_pos.col + 1) is within grid bounds
    actions:
      - place: orange_pixel (color 7) at (red_pos.row + 1, red_pos.col + 1) in output_grid
```


**Natural Language Program:**

1.  Identify the coordinates (row, column) of the single red pixel (color 2) in the input grid.
2.  Create a new output grid of the same dimensions as the input grid, filled entirely with white pixels (color 0).
3.  Define the four diagonal target positions relative to the red pixel's coordinates:
    *   Up-Left: (row - 1, column - 1)
    *   Up-Right: (row - 1, column + 1)
    *   Down-Left: (row + 1, column - 1)
    *   Down-Right: (row + 1, column + 1)
4.  For each target position:
    *   Check if the target coordinates are within the bounds of the grid (row >= 0, row < grid_height, column >= 0, column < grid_width).
    *   If the Up-Left position is within bounds, place a green pixel (color 3) at that position in the output grid.
    *   If the Up-Right position is within bounds, place a magenta pixel (color 6) at that position in the output grid.
    *   If the Down-Left position is within bounds, place an azure pixel (color 8) at that position in the output grid.
    *   If the Down-Right position is within bounds, place an orange pixel (color 7) at that position in the output grid.
5.  Return the modified output grid.
