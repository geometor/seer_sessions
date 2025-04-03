
## train_1

**input:**
```
7 7 7 7 7 1 7 7 7 7 7 7 7 7 7 7 7 7 9 5 7 7 5 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 1 2 5 5 5 5 3 5 3 5 5 5 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 4 4 4 4 4 4 4 7 4 4 4 4 4 4 4 4 4 4 4 4 4 1 4 4 4 4 0 0 0
```


**output:**
```
0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0
```

*   **Perception**:
    *   The input and output grids have the same dimensions.
    *   Each input grid contains multiple colors, including black (0).
    *   Often, there is a single row of black pixels at the bottom of the input grid, which remains unchanged in the output.
    *   In each example, one non-black color appears more frequently than others in the input grid. Let's call this the "dominant color".
    *   In the output grid, all pixels that were *not* black (0) and *not* the dominant color in the input grid are changed to the dominant color.
    *   Pixels that were originally the dominant color or black (0) remain unchanged in the output.

*   **Facts**:
    
```yaml
    Grid:
      - type: object
      - properties:
          - dimensions: height, width (constant between input and output)
          - pixels: 2D array of color values (0-9)
    Pixel:
      - type: object
      - properties:
          - color: integer value (0-9)
          - position: row, column
    Dominant_Color:
      - type: property
      - value: The color value (1-9) that appears most frequently in the input grid.
    Transformation:
      - type: action
      - steps:
          - Identify the Dominant_Color in the input grid (ignoring black pixels, color 0).
          - Create a new output grid of the same dimensions as the input.
          - Iterate through each pixel of the input grid:
              - If the input pixel's color is black (0), copy its color to the corresponding output pixel.
              - If the input pixel's color is the Dominant_Color, copy its color to the corresponding output pixel.
              - Otherwise (if the input pixel's color is not black (0) and not the Dominant_Color), set the corresponding output pixel's color to the Dominant_Color.
    ```


*   **Natural Language Program**:
    1.  Determine the most frequent non-black (color value not 0) color in the input grid. Call this `dominant_color`.
    2.  Create the output grid by iterating through each pixel of the input grid.
    3.  For each pixel:
        a.  If the pixel's color is black (0) or if its color is the `dominant_color`, keep the pixel's color the same in the output grid.
        b.  Otherwise, change the pixel's color to the `dominant_color` in the output grid.
