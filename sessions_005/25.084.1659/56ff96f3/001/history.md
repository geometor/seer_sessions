
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7
0 0 3 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 3 0 7 7 7 7
0 3 3 0 7 7 7 7
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided task examples.

**Perception of Elements:**

*   **Input Grids:** The input grids are predominantly white (0) with a few scattered, isolated pixels of other colors (yellow, green, orange, blue, red). In each example, for any given color other than white, there appear to be exactly two pixels of that color.
*   **Output Grids:** The output grids contain solid rectangles filled with the colors found in the input grid. The background remains white.
*   **Relationship:** The positions of the colored pixels in the input grid define the boundaries of the filled rectangles in the output grid. Specifically, for each color present in the input, the two pixels of that color seem to define the diagonally opposite corners of a rectangle filled with that same color in the output. The rectangle encompasses all cells between the minimum and maximum row and column coordinates defined by those two input pixels.

**Fact Documentation:**


```yaml
task_description: "Generate filled rectangles based on pairs of same-colored pixels in the input."
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains_pixels: True
  - type: pixel
    properties:
      - color: Integer (0-9)
      - position: (row, column)
  - type: object (derived)
    description: "Pair of pixels of the same non-white color in the input grid."
    properties:
      - color: Non-white color (1-9)
      - pixel_1_position: (r1, c1)
      - pixel_2_position: (r2, c2)
  - type: object (output)
    description: "Filled rectangle in the output grid."
    properties:
      - color: Same as the pair of input pixels defining it.
      - top_left_corner: (min(r1, r2), min(c1, c2))
      - bottom_right_corner: (max(r1, r2), max(c1, c2))
      - filled: True
relationships:
  - description: "Each pair of same-colored non-white pixels in the input defines the boundaries of a solid rectangle of that same color in the output."
    source: Pair of input pixels
    target: Output rectangle
    rule: "The rectangle spans inclusively from the minimum row and column to the maximum row and column defined by the pair of input pixel positions."
actions:
  - action: find_pixel_pairs
    description: "Identify pairs of pixels with the same non-white color in the input grid."
    inputs: input_grid
    outputs: list_of_pixel_pairs [(color, pos1, pos2), ...]
  - action: define_rectangle_bounds
    description: "For each pair, determine the minimum and maximum row and column indices."
    inputs: pixel_pair (color, pos1, pos2)
    outputs: rectangle_definition (color, min_row, min_col, max_row, max_col)
  - action: draw_rectangle
    description: "Fill the area defined by the bounds with the specified color on an initially white output grid."
    inputs: output_grid, rectangle_definition
    outputs: modified_output_grid
grid_properties:
  - size_relation: output grid has the same dimensions as the input grid.
  - background: output grid is initialized to white (0).
```


**Natural Language Program:**

1.  Create a new grid (`output_grid`) with the same height and width as the `input_grid`, and initialize all its pixels to white (0).
2.  Identify all unique non-white colors present in the `input_grid`.
3.  For each unique non-white color identified:
    a.  Find the row and column coordinates of all pixels in the `input_grid` that have this color.
    b.  Determine the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among these coordinates.
    c.  Iterate through all rows from `min_row` to `max_row` (inclusive) and all columns from `min_col` to `max_col` (inclusive).
    d.  For each cell within this range (`current_row`, `current_col`), set the pixel value in the `output_grid` at (`current_row`, `current_col`) to the current unique non-white color.
4.  Return the final `output_grid`.
