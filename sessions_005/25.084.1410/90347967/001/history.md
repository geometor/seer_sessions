
## train_1

**input:**
```
6 0 0
2 5 0
2 1 0
```


**output:**
```
0 1 2
0 5 2
0 0 6
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 2 5 0 0 0 0
0 0 3 3 0 0 0 0 0
0 1 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 1 0
0 0 0 0 0 3 3 0 0
0 0 0 0 5 2 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 3 5 0 0 0 0 0
1 1 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0
0 0 0 0 0 1 1 0 0
0 0 0 5 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception

1.  **Grid Structure:** Both input and output are 2D grids of pixels represented by integer color codes (0-9). The background is consistently white (0).
2.  **Content:** The input grids contain various colored pixels (non-zero values), sometimes forming simple shapes or patterns.
3.  **Transformation:** Comparing input and output grids across the examples, the arrangement of colored pixels changes, but the colors themselves and their relative spatial configuration (if viewed as a rotated whole) seem preserved.
4.  **Size:** The dimensions (height and width) of the output grid are always identical to the input grid.
5.  **Geometric Operation:** In each example, the output grid appears to be a 180-degree rotation of the input grid. The pixel at the top-left corner moves to the bottom-right, the pixel at the top-right moves to the bottom-left, and so on. Pixels are effectively mapped from position (r, c) to (H-1-r, W-1-c), where H is the height and W is the width of the grid.

## Facts


```yaml
task_description: Apply a geometric transformation to the input grid.

elements:
  - element: grid
    properties:
      - type: 2D array of integers (colors)
      - dimensions: height (H), width (W) vary per example
      - background_color: white (0)
  - element: pixel
    properties:
      - type: cell within the grid
      - value: color (integer 0-9)
      - position: row (r), column (c)

transformation:
  - type: geometric_rotation
    details:
      - angle: 180 degrees
      - center: center of the grid
      - mapping: Input pixel at (r, c) moves to output position (H-1-r, W-1-c).

input_output_relationship:
  - rule: The output grid is the input grid rotated by 180 degrees.
  - preservation:
    - Grid dimensions (height and width) are preserved.
    - The set of non-background colors present is preserved.
    - The relative arrangement of colored pixels is preserved under rotation.
```


## Natural Language Program

1.  Given an input grid with height `H` and width `W`.
2.  Create a new output grid with the same dimensions (`H` x `W`).
3.  For each pixel in the input grid located at row `r` and column `c` (where `0 <= r < H` and `0 <= c < W`):
    a.  Determine the color value of this input pixel.
    b.  Calculate the corresponding position in the output grid: the new row `r'` is `H - 1 - r`, and the new column `c'` is `W - 1 - c`.
    c.  Assign the color value from step 3a to the output grid pixel at position (`r'`, `c'`).
4.  Return the completed output grid.
