
## train_1

**input:**
```
0 0 9
0 0 9
9 9 9
```


**output:**
```
9 9 9
0 0 9
0 0 9
```


## train_2

**input:**
```
6 6 6
0 0 0
6 6 0
```


**output:**
```
6 0 0
6 0 6
6 0 6
```


## train_3

**input:**
```
2 0 2
0 0 2
0 2 2
```


**output:**
```
2 2 2
0 0 2
2 0 0
```


## train_4

**input:**
```
9 0 0
9 9 9
9 9 9
```


**output:**
```
0 9 9
0 9 9
9 9 9
```

## Perception

1.  **Grid Size:** All input and output grids are 3x3.
2.  **Colors:** Various colors (maroon, magenta, red, white) are used. The background color is consistently white (0). The non-white pixels form distinct shapes or patterns within the grid.
3.  **Transformation:** Comparing each input grid to its corresponding output grid, the pattern appears to be a rotation of the entire grid.
4.  **Rotation Direction:**
    *   In example 1, the bottom-left 'L' shape (maroon) moves to the top-right, consistent with a 90-degree clockwise rotation.
    *   In example 2, the 'C'-like shape (magenta) rotates similarly.
    *   In example 3, the red pattern rotates.
    *   In example 4, the larger 'L' shape (maroon) rotates.
    All examples consistently show a 90-degree clockwise rotation.
5.  **Content Preservation:** The colors and relative positions of the pixels within the grid are preserved during the rotation. No pixels change color or disappear/appear; they only change their absolute position due to the rotation of the grid itself.

## Facts


```yaml
task_description: Apply a geometric transformation to the entire input grid.
grid_properties:
  - input_dimensions: 3x3
  - output_dimensions: 3x3
transformation:
  type: rotation
  object: entire_input_grid
  details:
    direction: clockwise
    angle_degrees: 90
pixel_behavior: Pixels maintain their color and relative positions during the rotation.
```


## Natural Language Program

1.  Receive the input grid.
2.  Rotate the input grid 90 degrees clockwise.
3.  Output the resulting rotated grid.
