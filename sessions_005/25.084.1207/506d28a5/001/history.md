
## train_1

**input:**
```
0 0 0 0 0
0 2 2 2 0
0 2 0 0 0
2 2 2 0 2
4 4 4 4 4
1 1 0 0 1
1 1 0 1 1
1 0 1 0 1
0 1 0 1 1
```


**output:**
```
3 3 0 0 3
3 3 3 3 3
3 3 3 0 3
3 3 3 3 3
```


## train_2

**input:**
```
2 2 2 2 2
0 0 0 2 0
0 2 0 2 2
2 2 2 2 2
4 4 4 4 4
0 1 1 0 0
1 1 0 1 0
1 1 0 0 0
0 0 1 1 1
```


**output:**
```
3 3 3 3 3
3 3 0 3 0
3 3 0 3 3
3 3 3 3 3
```


## train_3

**input:**
```
0 2 0 0 2
0 2 2 0 2
0 0 0 2 2
0 0 2 2 0
4 4 4 4 4
1 0 1 0 0
1 0 0 1 0
0 0 0 0 1
0 1 1 1 0
```


**output:**
```
3 3 3 0 3
3 3 3 3 3
0 0 0 3 3
0 3 3 3 0
```


## train_4

**input:**
```
0 2 2 0 0
2 2 2 2 0
0 0 2 2 0
0 0 2 2 0
4 4 4 4 4
1 0 0 1 0
1 1 1 0 1
0 0 1 1 1
1 1 1 0 0
```


**output:**
```
3 3 3 3 0
3 3 3 3 3
0 0 3 3 3
3 3 3 3 0
```

Okay, let's analyze the provided examples.

## Perception

1.  **Input Structure:** The input grids consistently feature a horizontal line composed entirely of yellow (4) pixels. This line divides the grid into two distinct regions: an upper region above the yellow line and a lower region below it.
2.  **Color Distribution (Input):**
    *   The **upper region** contains only red (2) and white (0) pixels.
    *   The **lower region** contains only blue (1) and white (0) pixels.
    *   The **separator** line is always yellow (4).
3.  **Output Structure:** The output grid is always smaller than the input grid. Its dimensions precisely match the dimensions of the lower region of the input grid (below the yellow line).
4.  **Color Distribution (Output):** The output grid contains only green (3) and white (0) pixels.
5.  **Transformation Pattern:** The yellow separator line is absent in the output. The output grid seems to be a combination or overlay of the patterns found in the upper and lower regions of the input grid. Specifically, a pixel in the output grid becomes green (3) if the corresponding pixel in the *upper* input region was red (2) *or* if the corresponding pixel in the *lower* input region was blue (1). If neither of these conditions is met (i.e., both corresponding input pixels were white), the output pixel remains white (0).

## Facts

```
yaml
task_description: Combine information from two regions of the input grid, separated by a specific color line, based on a logical OR operation between the colors present in those regions.

input_grid:
  properties:
    - contains_separator: true
    - separator_color: yellow (4)
    - separator_orientation: horizontal
  components:
    - upper_part:
        location: Above the separator line.
        pixels: Contains only red (2) and white (0).
        dimensions: Matches the dimensions of the lower_part.
    - lower_part:
        location: Below the separator line.
        pixels: Contains only blue (1) and white (0).
        dimensions: Matches the dimensions of the upper_part.
    - separator:
        pixels: All yellow (4).
        shape: Horizontal line spanning the grid width.

output_grid:
  properties:
    - dimensions: Same as the lower_part (and upper_part) of the input grid.
    - pixels: Contains only green (3) and white (0).

transformation:
  type: overlay_or_combination
  mapping:
    - rule: A pixel at position (row, col) in the output is green (3) if the pixel at (row, col) in the input's upper_part is red (2) OR the pixel at (row, col) in the input's lower_part is blue (1).
    - rule: Otherwise, the pixel at position (row, col) in the output is white (0).
  relationship: The output grid structure directly corresponds positionally to the upper and lower parts of the input grid.

