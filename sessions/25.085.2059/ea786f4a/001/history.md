
## train_1

**input:**
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```


**output:**
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```


## train_2

**input:**
```
1 1 1
1 0 1
1 1 1
```


**output:**
```
0 1 0
1 0 1
0 1 0
```


## train_3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```


**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

*   **Perception of Task Elements:**
    *   The input grids consistently feature a single white pixel (0) embedded within a larger area filled with a single non-white color (red=2, blue=1, or green=3).
    *   The output grids retain the same dimensions as the input grids.
    *   The original white pixel's position remains white in the output.
    *   Several pixels that were non-white in the input are changed to white (0) in the output.
    *   The pattern of pixels changing to white appears symmetric around the original white pixel's location.
    *   The specific non-white color (red, blue, green) from the input seems to determine the color of the pixels *not* changed to white in the output.
    *   Comparing input and output, the pixels that change to white form a checkerboard-like pattern originating from the initial white pixel. Specifically, pixels whose Manhattan distance from the initial white pixel is an even number become white. Pixels at an odd Manhattan distance retain their original non-white color.

*   **Facts:**
    
```yaml
    task_type: pattern_transformation
    grid_properties:
      - dimensions: remain constant between input and output.
      - background_color: input has a dominant non-white color.
      - key_element: input contains exactly one white pixel (0).
    objects:
      - type: pixel
        attributes:
          - color: (0-9)
          - position: (row, column)
      - type: anchor_pixel
        description: The single white pixel present in the input grid.
        properties:
          - color: 0
          - position: (r0, c0)
    relationships:
      - type: distance
        from: any pixel (r, c)
        to: anchor_pixel (r0, c0)
        metric: Manhattan distance (|r - r0| + |c - c0|)
    transformation:
      - based_on: Manhattan distance from the anchor_pixel.
      - rule:
          - if distance is even: output pixel color becomes white (0).
          - if distance is odd: output pixel color remains the same as the input pixel color at that position.
    ```


*   **Natural Language Program:**
    1.  Identify the coordinates (row `r0`, column `c0`) of the single white pixel (color 0) in the input grid. This is the "anchor pixel".
    2.  Create an output grid with the same dimensions as the input grid.
    3.  For each pixel at coordinates (row `r`, column `c`) in the input grid:
        a.  Calculate the Manhattan distance `d` between this pixel (`r`, `c`) and the anchor pixel (`r0`, `c0`): `d = abs(r - r0) + abs(c - c0)`.
        b.  Check if the distance `d` is even or odd.
        c.  If `d` is even, set the color of the corresponding pixel (`r`, `c`) in the output grid to white (0).
        d.  If `d` is odd, set the color of the corresponding pixel (`r`, `c`) in the output grid to the original color of the input pixel at (`r`, `c`).
    4.  Return the completed output grid.
