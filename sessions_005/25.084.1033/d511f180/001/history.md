
## train_1

**input:**
```
3 5 1
4 5 8
2 4 9
```


**output:**
```
3 8 1
4 8 5
2 4 9
```


## train_2

**input:**
```
2 7 8 8 8
5 5 6 5 4
8 5 5 5 2
8 8 4 3 6
6 5 1 9 3
```


**output:**
```
2 7 5 5 5
8 8 6 8 4
5 8 8 8 2
5 5 4 3 6
6 8 1 9 3
```


## train_3

**input:**
```
6 5 3
5 7 5
8 8 2
```


**output:**
```
6 8 3
8 7 8
5 5 2
```

## Perception

The input and output are grids of the same dimensions in each example. The transformation involves changing the colors (values) of specific pixels within the grid. Observing the changes across the examples, it appears that only two colors are consistently affected: gray (value 5) and azure (value 8). In every location where the input grid has a gray pixel, the output grid has an azure pixel, and conversely, where the input grid has an azure pixel, the output grid has a gray pixel. All other colors remain in their original positions. This suggests a simple substitution or swap between these two specific colors.

## Facts


```yaml
task_type: color_transformation
components:
  - type: grid
    properties:
      - dimensions: constant between input and output
      - elements: pixels
  - type: pixel
    properties:
      - color: integer value 0-9
transformation:
  type: color_swap
  details:
    - target_color_1: 5 # gray
    - target_color_2: 8 # azure
    - scope: applies to all pixels in the grid
    - action: replace all instances of target_color_1 with target_color_2, and replace all instances of target_color_2 with target_color_1
  unchanged_elements:
    - pixels with colors other than 5 or 8
    - grid dimensions
```


## Natural Language Program

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each pixel (cell) of the input grid, examining its color value.
3.  If the input pixel's color is gray (5), set the corresponding pixel in the new grid to azure (8).
4.  If the input pixel's color is azure (8), set the corresponding pixel in the new grid to gray (5).
5.  If the input pixel's color is neither gray (5) nor azure (8), set the corresponding pixel in the new grid to the same color as the input pixel.
6.  The new grid is the output.
