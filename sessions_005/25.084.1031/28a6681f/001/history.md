
## train_1

**input:**
```
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 3 0 3 1 1
0 0 0 0 0 3 0 3 1 1
0 0 0 0 2 3 0 3 1 1
0 0 0 0 2 3 0 3 1 1
0 2 2 2 2 3 3 3 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 3 1 3 1 1
0 0 0 0 0 3 1 3 1 1
0 0 0 0 2 3 1 3 1 1
0 0 0 0 2 3 1 3 1 1
0 2 2 2 2 3 3 3 1 1
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 1
0 0 3 0 0 0 0 1 1 1
0 0 3 0 0 0 0 1 1 1
0 0 3 0 0 0 1 1 1 1
0 0 3 0 0 3 1 1 1 1
0 0 3 0 0 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 3 3 3 5 5 5 5
```


**output:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 1 1 1 1 1 1 1
0 0 3 1 1 3 1 1 1 1
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 3 3 3 5 5 5 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
9 9 1 1 0 0 0 0 9 9
0 9 9 1 0 0 0 9 9 0
0 0 9 9 0 0 0 9 0 0
0 0 0 9 0 0 9 9 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 4 0 0 0 0
2 0 0 4 0 4 0 0 0 0
2 0 2 4 0 4 0 0 0 0
2 2 2 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 9 9
0 9 9 0 0 0 0 9 9 0
0 0 9 9 0 0 0 9 0 0
0 0 0 9 0 0 9 9 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 4 0 0 0 0
2 0 0 4 1 4 0 0 0 0
2 1 2 4 1 4 0 0 0 0
2 2 2 4 4 4 0 0 0 0
```

## Perception

The core transformation involves identifying specific white pixels (color 0) in the input grid and changing their color to blue (color 1) in the output grid based on their immediate horizontal neighbors. All other pixels retain their original color. The condition for changing a white pixel is that it must be directly horizontally sandwiched between two pixels of the exact same non-white color.

## Facts


```yaml
task_type: pixel_manipulation
focus: local_context
transformation: color_change
input_elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: pixel
    property: color
    value: white (0)
  - type: pixel
    property: color
    value: non-white (1-9)
relationships:
  - type: horizontal_adjacency
    description: Pixels immediately to the left and right of a target pixel.
  - type: pattern
    description: A sequence of three horizontally adjacent pixels (Left, Center, Right).
    specific_pattern:
      Left: non-white color C
      Center: white (0)
      Right: same non-white color C
action:
  - on: Center pixel (white)
    condition: Matches the specific_pattern (C, 0, C) horizontally.
    result: Change color from white (0) to blue (1).
output_elements:
  - type: grid
    description: A modified version of the input grid where specific white pixels have been changed to blue.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the basis for the output grid.
2.  Iterate through each pixel in the input grid, excluding pixels in the first and last columns (as they cannot be the center of a horizontal triplet). Let the current pixel's coordinates be (row, col).
3.  Check if the color of the current pixel at (row, col) is white (0).
4.  If it is white, check the colors of its immediate left neighbor at (row, col-1) and immediate right neighbor at (row, col+1).
5.  If both the left neighbor and the right neighbor are non-white (color 1-9) AND they have the exact same color value, then change the color of the pixel at (row, col) in the *output* grid to blue (1).
6.  If the conditions in steps 3 or 5 are not met, the pixel at (row, col) in the output grid retains its original color from the input grid.
7.  After checking all applicable pixels, the modified grid is the final output.
