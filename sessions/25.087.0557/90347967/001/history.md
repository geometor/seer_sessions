
## train_1

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


## train_2

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

*   **Perception:** The task involves rotating the contents of the input grid. In each example, there is a collection of non-background colored pixels, including one unique gray pixel. The output grid shows these colored pixels rearranged as if rotated around the gray pixel. The grid dimensions remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: geometric_transformation
    transformation: rotation
    rotation_angle: 90_degrees_clockwise
    center_of_rotation:
      identifier: specific_color
      color: gray # value 5
    input_elements:
      - type: grid
      - type: objects # contiguous non-background pixels
      - type: pivot_point # the gray pixel
    output_elements:
      - type: grid # same dimensions as input
      - type: objects # rotated versions of input objects
    background_color: white # value 0
    object_handling:
      - all non-background pixels are treated as part of the rotation
    grid_properties:
      - dimensions remain constant
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the background color (white, 0).
    2.  Locate the coordinates (center\_row, center\_col) of the single gray pixel (color 5) within the input grid.
    3.  Iterate through every pixel in the input grid at coordinates (input\_row, input\_col) with its color `c`.
    4.  If the color `c` is not the background color (white, 0):
        a.  Calculate the pixel's relative coordinates to the center of rotation: `relative_row = input_row - center_row`, `relative_col = input_col - center_col`.
        b.  Apply a 90-degree clockwise rotation transformation to the relative coordinates: `new_relative_row = relative_col`, `new_relative_col = -relative_row`.
        c.  Calculate the pixel's new absolute coordinates in the output grid: `output_row = center_row + new_relative_row`, `output_col = center_col + new_relative_col`.
        d.  If the calculated (output\_row, output\_col) are within the bounds of the grid dimensions, place the color `c` at these coordinates in the output grid.
    5.  Return the completed output grid.
