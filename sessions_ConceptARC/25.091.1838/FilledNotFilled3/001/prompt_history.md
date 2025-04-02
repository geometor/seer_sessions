
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 1 3 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 4 4 4 0 0 7 7 7 0
0 4 4 4 0 0 7 7 7 0
0 4 4 4 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0
0 0 0 0 4 0 0 4 0 0
0 0 0 0 4 0 0 4 0 0
4 4 4 0 4 4 4 4 0 0
4 4 4 0 0 0 0 0 0 0
4 4 4 0 0 6 6 6 0 0
4 4 4 0 0 6 6 6 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0
0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 3 3 0 0
0 8 8 8 0 3 3 3 0 0
0 8 5 8 0 3 3 3 0 0
0 8 8 8 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 9 9 9 0 0
```


**output:**
```
5
```

*   **Perception:** The input grids contain multiple distinct geometric shapes formed by colored pixels on a white background. The shapes observed include solid squares (3x3) and 'plus' shapes (3x3 squares with a distinctly colored center pixel). The output is always a small grid (1x1 or 2x2) filled with a single color. The color and size of the output grid seem dependent on the presence and type of shapes in the input grid. Specifically, the presence of a 'plus' shape appears crucial.

*   **YAML Facts:**
    
```yaml
    examples:
      train_1:
        input:
          grid_size: [10, 10]
          background_color: white
          objects:
            - shape: plus
              size: [3, 3]
              frame_color: green
              center_color: blue
            - shape: square
              size: [3, 3]
              color: yellow
            - shape: square
              size: [3, 3]
              color: orange
        output:
          grid_size: [1, 1]
          fill_color: blue
          derived_from: center_color of the 'plus' object
      train_2:
        input:
          grid_size: [10, 10]
          background_color: white
          objects:
            - shape: u_shape # Or hollow square
              size: [4, 4] # Bounding box
              color: yellow
            - shape: square
              size: [3, 3]
              color: yellow
            - shape: square
              size: [3, 3]
              color: magenta
        output:
          grid_size: [2, 2]
          fill_color: white
          derived_from: absence of a 'plus' object
      train_3:
        input:
          grid_size: [10, 10]
          background_color: white
          objects:
            - shape: square
              size: [3, 3]
              color: green
            - shape: plus
              size: [3, 3]
              frame_color: azure
              center_color: gray
            - shape: square
              size: [3, 3]
              color: maroon
        output:
          grid_size: [1, 1]
          fill_color: gray
          derived_from: center_color of the 'plus' object
    general_properties:
      - Objects are contiguous blocks of non-white color.
      - A 'plus' object is defined as a 3x3 square of one color (frame_color) with a single pixel of a different color (center_color) exactly in the middle.
      - Other shapes observed include solid squares and U-shapes.
      - The background color is consistently white (0).
    ```


*   **Natural Language Program:**
    1.  Identify all distinct objects in the input grid, where an object is a contiguous area of non-white pixels.
    2.  Examine each identified object to determine if it matches the pattern of a 'plus' shape: a 3x3 square area where the 8 outer pixels share one color (the frame color) and the single central pixel has a different color (the center color).
    3.  **Condition 1:** If exactly one object matching the 'plus' shape pattern is found:
        *   Extract the color of the central pixel of this 'plus' shape.
        *   Construct the output as a 1x1 grid filled with this extracted center color.
    4.  **Condition 2:** If no objects matching the 'plus' shape pattern are found:
        *   Construct the output as a 2x2 grid filled entirely with the white color (0).
    5.  (Implicit Assumption: The case of multiple 'plus' shapes is not covered by the examples and its outcome is undefined by this program).
