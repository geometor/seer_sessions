
## train_1

**input:**
```
8 8 8
5 5 8
8 5 5
```


**output:**
```
5 5 8
8 5 5
8 8 8
```


## train_2

**input:**
```
9 2 4
2 4 4
2 9 2
```


**output:**
```
2 9 2
4 4 2
4 2 9
```


## train_3

**input:**
```
3 2 9
9 9 9
2 3 3
```


**output:**
```
3 3 2
9 9 9
9 2 3
```


## train_4

**input:**
```
2 2 1
2 1 2
2 8 1
```


**output:**
```
1 8 2
2 1 2
1 2 2
```

## Perception of Elements

The task involves transforming a 2D grid of colored pixels. Each example shows an input grid and a corresponding output grid.
- The dimensions (height and width) of the input grid are the same as the output grid in all examples.
- The set of colors (pixel values) present in the input grid is the same as the set of colors in the output grid.
- The transformation appears to be a spatial rearrangement of the pixels within the grid.
- Comparing the input and output grids across all examples reveals a consistent pattern: the output grid is the input grid rotated by 180 degrees.

## Facts


```yaml
Input_Grid:
  type: 2D array of integers (pixels)
  properties:
    - height: H
    - width: W
    - pixels: each has a color (integer 0-9) and a position (row, column)

Output_Grid:
  type: 2D array of integers (pixels)
  properties:
    - height: H (same as Input_Grid)
    - width: W (same as Input_Grid)
    - pixels: each has a color (integer 0-9) and a position (row, column)

Transformation:
  type: Geometric Rotation
  action: Rotate the Input_Grid by 180 degrees around its center point.
  details:
    - A pixel at position (r, c) in the Input_Grid moves to position (H - 1 - r, W - 1 - c) in the Output_Grid.
    - The color of the pixel remains unchanged during the move.
```


## Natural Language Program

1.  Receive the input grid.
2.  Determine the height (H) and width (W) of the input grid.
3.  Create a new output grid of the same height (H) and width (W).
4.  For each pixel in the input grid located at row `r` and column `c` (where `r` ranges from 0 to H-1 and `c` ranges from 0 to W-1):
    a.  Calculate the target position in the output grid: target row `r_out = H - 1 - r`, target column `c_out = W - 1 - c`.
    b.  Copy the color value of the input pixel at `(r, c)` to the output grid at position `(r_out, c_out)`.
5.  Return the completed output grid.
