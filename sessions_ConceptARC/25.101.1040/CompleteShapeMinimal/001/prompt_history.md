
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 0 0 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 6 0 0 6 6 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
3 3 3 3 3 0 3 3
3 3 3 3 3 3 0 3
3 3 0 3 3 3 3 3
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves identifying internal "holes" within the main colored shape in the input grid and filling these holes with the color of the shape itself. The main shape is defined as the largest contiguous block of a single non-white color. The "holes" are areas of the background color (white) that are completely enclosed by the main shape's color. The overall structure and the color of the main shape are preserved, except for the filling of these internal voids.

*   **Facts:**
    
```yaml
    objects:
      - id: primary_shape
        description: The largest contiguous block of a single non-white color.
        properties:
          color: Varies (blue, magenta, green in examples).
          shape: Irregular, generally rectangular or square-like with internal voids.
      - id: background
        description: The area surrounding the primary_shape.
        properties:
          color: white (0)
      - id: holes
        description: Regions of background color pixels completely enclosed within the primary_shape.
        properties:
          color: white (0)
          location: Within the bounding box of the primary_shape.
          topology: Surrounded by pixels of the primary_shape's color.
    actions:
      - id: find_primary_shape
        description: Identify the largest connected component of non-white pixels.
      - id: find_holes
        description: Identify contiguous regions of background pixels completely surrounded by the primary_shape.
      - id: fill_holes
        description: Change the color of the pixels identified as holes to the color of the primary_shape.
    relationships:
      - type: containment
        subject: holes
        object: primary_shape
        description: Holes are spatially contained within the boundaries of the primary_shape.
      - type: adjacency
        subject: holes
        object: primary_shape
        description: All pixels bordering a hole belong to the primary_shape.
    ```


*   **Natural Language Program:**
    1.  Identify the largest contiguous object (`primary_shape`) that is not the background color (white). Determine its color (`shape_color`).
    2.  Identify all pixels with the background color (white).
    3.  For each background pixel, determine if it is completely surrounded by pixels of `shape_color`. A pixel is considered surrounded if all paths from it to the grid's boundary must pass through a pixel of `shape_color`.
    4.  Create the output grid by copying the input grid.
    5.  Change the color of all identified surrounded background pixels (the `holes`) to `shape_color` in the output grid.
