
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

## Perception

The task involves transforming an input grid into an output grid of the same dimensions.
1.  **Input Grid:** Each input grid contains predominantly `white` (0) pixels and exactly one non-`white` pixel. The color of this single pixel varies across examples (`blue`, `green`, `magenta`, `red`). Its position also varies but tends to be near the center.
2.  **Output Grid:** Each output grid has the same dimensions as the corresponding input grid. It features a border of thickness 1 pixel around its perimeter. The color of this border matches the color of the single non-`white` pixel found in the input grid. All pixels inside this border are `white` (0).
3.  **Transformation:** The core transformation identifies the unique non-`white` color in the input and uses it to draw a frame or border on an otherwise `white` grid of the same size. The original position or color of the central pixel in the input grid does not seem to affect the *interior* pixels of the output grid; they are always set to `white`.

## Facts


```yaml
task_description: Create a border around the grid using the color of the single non-white pixel found in the input.
grid_properties:
  - dimensions_match: Input and output grids have the same height and width.

input_elements:
  - element: background
    color: white (0)
    description: The predominant color in the input grid.
  - element: source_pixel
    count: 1
    color: non-white (varies: 1, 2, 3, 6)
    description: A single pixel with a color other than white.
    location: variable, often near the center.

output_elements:
  - element: border
    thickness: 1 pixel
    location: perimeter of the grid (row 0, last row, column 0, last column)
    color: Same as the input source_pixel color.
    description: A frame around the edge of the output grid.
  - element: interior
    color: white (0)
    location: All pixels not part of the border.
    description: The area inside the border.

transformation:
  - step: Identify the dimensions (height H, width W) of the input grid.
  - step: Find the single non-white pixel in the input grid and determine its color (C).
  - step: Create a new grid of dimensions H x W, initially filled with white (0).
  - step: Set the color of all pixels in the first row (row 0) to C.
  - step: Set the color of all pixels in the last row (row H-1) to C.
  - step: Set the color of all pixels in the first column (column 0) to C.
  - step: Set the color of all pixels in the last column (column W-1) to C.
  - result: The final grid has a border of color C and a white interior.
```


## Natural Language Program

1.  Determine the height (H) and width (W) of the input grid.
2.  Scan the input grid to find the unique pixel that is not `white` (0). Record its color, C.
3.  Create a new output grid with the same height H and width W.
4.  Initialize all pixels in the output grid to `white` (0).
5.  Color the top row (row index 0) of the output grid with color C.
6.  Color the bottom row (row index H-1) of the output grid with color C.
7.  Color the leftmost column (column index 0) of the output grid with color C.
8.  Color the rightmost column (column index W-1) of the output grid with color C.
9.  The resulting grid is the final output.
