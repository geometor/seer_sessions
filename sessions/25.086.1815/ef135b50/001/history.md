
## train_1

**input:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 2 2 2
2 2 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 2 2
0 0 0 2 2 0 0 2 2 2
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 2 2 2 2
0 0 0 0 0 0 2 2 2 2
```


**output:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
2 2 9 9 9 9 9 2 2 2
2 2 9 9 9 9 9 2 2 2
0 0 0 0 0 0 0 2 2 2
0 0 0 2 2 9 9 2 2 2
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 9 2 2 2 2
0 0 0 0 0 0 2 2 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 2 2 0
2 2 2 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 2 0
0 0 0 2 2 0 0 2 2 0
0 0 0 2 2 0 0 2 2 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 2 2 9 9 9 9 2 2 0
2 2 2 9 9 9 9 2 2 0
0 0 0 0 0 0 0 2 2 0
0 0 0 2 2 9 9 2 2 0
0 0 0 2 2 9 9 2 2 0
0 0 0 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 2 2 2
2 2 2 2 0 0 2 2 2 2
2 2 2 2 0 0 0 0 0 0
2 2 2 2 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 2
2 2 2 2 0 2 2 2 0 2
2 2 2 2 0 2 2 2 0 2
2 2 2 2 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 2 2 2 2
2 2 2 2 9 9 2 2 2 2
2 2 2 2 0 0 0 0 0 0
2 2 2 2 9 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 9 2
2 2 2 2 9 2 2 2 9 2
2 2 2 2 9 2 2 2 9 2
2 2 2 2 0 0 0 0 0 2
```

Okay, let's analyze the provided examples.

**Perception:**

The task involves transforming a 2D grid containing primarily white (0) and red (2) pixels. The transformation introduces maroon (9) pixels into the output grid while preserving the original positions and shapes of the red (2) structures. The maroon pixels appear exclusively in locations that were originally white. Observing the placement of the new maroon pixels, they consistently appear in white areas that are horizontally "sandwiched" between red pixels on the same row. That is, a white pixel changes to maroon if and only if there is at least one red pixel somewhere to its left and at least one red pixel somewhere to its right within the same row. Vertical relationships between red pixels do not seem to influence the transformation.

**Facts:**


```yaml
task_context:
  grid_size: fixed 10x10 for examples, but variable in general (up to 30x30)
  colors_present_input: [white (0), red (2)]
  colors_present_output: [white (0), red (2), maroon (9)]
  transformation_type: color substitution based on spatial context

objects:
  - type: pixel
    properties:
      - color: white (0), red (2), maroon (9)
      - location: (row, column)
  - type: shape
    description: contiguous blocks of red (2) pixels, mostly rectangular in examples
    properties:
      - color: red (2)
      - location: set of pixel coordinates

relationships:
  - type: spatial
    description: Relative positioning of pixels within the grid.
    details: Focus is on horizontal alignment within the same row.
    concepts: [left_of, right_of, same_row]

actions:
  - name: identify_target_pixels
    input: input grid
    output: list of coordinates of white (0) pixels
    condition: pixel color is white (0)
  - name: check_horizontal_containment
    input: coordinates of a white (0) pixel, input grid
    output: boolean (true if contained, false otherwise)
    condition: >
      Checks if there exists a red (2) pixel at (row, col_left) where col_left < col
      AND there exists a red (2) pixel at (row, col_right) where col_right > col,
      for the target pixel at (row, col).
  - name: change_color
    input: coordinates of a white (0) pixel that meets the containment condition, output grid
    output: modified output grid
    effect: Changes the color of the pixel at the specified coordinates from white (0) to maroon (9).

transformation_rule:
  description: >
    For each white pixel in the input grid, determine if it is horizontally bounded by red pixels
    within its row. If it is, change its color to maroon in the output grid. Otherwise, keep its color.
    All non-white pixels retain their original color in the output grid.
  steps:
    1. Create a copy of the input grid to serve as the initial output grid.
    2. Iterate through each row and column of the grid.
    3. If the pixel at (row, col) in the input grid is white (0):
       a. Check if there is any red (2) pixel in the same row to the left (columns < col).
       b. Check if there is any red (2) pixel in the same row to the right (columns > col).
       c. If both checks (a and b) are true, set the color of the pixel at (row, col) in the output grid to maroon (9).
    4. Return the final output grid.
```


**Natural Language Program:**

1.  Create the output grid as an identical copy of the input grid.
2.  For each row in the grid:
    a.  Find the column indices of all red (2) pixels within that row.
    b.  If there are at least two red pixels in the row:
        i.  Determine the minimum column index (`min_red_col`) and the maximum column index (`max_red_col`) of the red pixels in that row.
        ii. For each column index `col` between `min_red_col` and `max_red_col` (exclusive of the bounds):
            1. If the pixel at (`row`, `col`) in the input grid is white (0), change the color of the pixel at (`row`, `col`) in the output grid to maroon (9).
3.  Return the modified output grid.
