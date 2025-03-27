
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 1 1 1 1 1 1
```


## train_2

**input:**
```
0 0 0
0 0 0
0 3 0
0 0 0
0 0 0
```


**output:**
```
3 3 3
3 0 3
3 0 3
3 0 3
3 3 3
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 6
```


## train_4

**input:**
```
0 0 0
0 2 0
0 0 0
```


**output:**
```
2 2 2
2 0 2
2 2 2
```

Okay, let's analyze the provided examples.

## Perception

1.  **Input Structure:** Each input grid consists primarily of `white` (0) pixels, with a single non-`white` pixel located somewhere within the grid, but not on the absolute edge.
2.  **Output Structure:** Each output grid has the same dimensions as its corresponding input. The output features a one-pixel thick border around its perimeter. The color of this border matches the color of the single non-`white` pixel found in the input. The interior of the output grid (everything inside the border) is filled with `white` (0) pixels.
3.  **Color Transformation:** The key transformation involves identifying the color of the single non-`white` pixel in the input and using that color to draw the border in the output.
4.  **Shape Transformation:** The input's single pixel structure is replaced by a hollow rectangle (the border) in the output. The size of this rectangle is determined by the dimensions of the input grid.
5.  **Consistency:** This pattern holds across all provided training examples. The input color dictates the output border color, and the output is always a border of that color around a `white` interior, matching the input grid dimensions.

## Facts


```yaml
task_description: Create a border around the grid using the color of the single non-background pixel found in the input.
grid_properties:
  - input_dimensions: variable (e.g., 5x7, 5x3, 5x5, 3x3)
  - output_dimensions: same as input
  - background_color: white (0)
input_objects:
  - object: single_pixel
    attributes:
      - color: variable (blue(1), green(3), magenta(6), red(2))
      - count: 1 per input grid
      - location: not on the perimeter
output_objects:
  - object: border
    attributes:
      - color: matches the color of the input single_pixel
      - thickness: 1 pixel
      - location: perimeter of the grid
  - object: interior
    attributes:
      - color: white (0)
      - location: inside the border
transformation_rule:
  - step: Identify the single non-white pixel in the input grid.
  - step: Record its color (let's call it 'border_color').
  - step: Get the dimensions (height H, width W) of the input grid.
  - step: Create an output grid of the same dimensions (H x W).
  - step: Fill the top row (row 0) and bottom row (row H-1) of the output grid with 'border_color'.
  - step: Fill the leftmost column (col 0) and rightmost column (col W-1) of the output grid with 'border_color'.
  - step: Fill all remaining interior pixels of the output grid with white (0).
```


## Natural Language Program

1.  Determine the height (H) and width (W) of the input grid.
2.  Scan the input grid to find the single pixel that is not `white` (0). Record the color of this pixel; let this be `border_color`.
3.  Create a new grid with the same dimensions (H x W) as the input grid.
4.  Fill the entire perimeter of the new grid with `border_color`. This means:
    *   Set all pixels in the first row (row index 0) to `border_color`.
    *   Set all pixels in the last row (row index H-1) to `border_color`.
    *   Set all pixels in the first column (column index 0) to `border_color`.
    *   Set all pixels in the last column (column index W-1) to `border_color`.
5.  Fill all pixels within the interior of the new grid (i.e., all pixels not on the perimeter) with `white` (0).
6.  The resulting grid is the output.
