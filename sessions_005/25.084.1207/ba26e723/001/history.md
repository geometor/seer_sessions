
## train_1

**input:**
```
4 0 4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4 0 4 0
```


**output:**
```
6 0 4 0 4 0 6 0 4 0 4 0 6
6 4 4 6 4 4 6 4 4 6 4 4 6
0 4 0 6 0 4 0 4 0 6 0 4 0
```


## train_2

**input:**
```
0 4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 0 4 0 4 0 4
```


**output:**
```
0 4 0 6 0 4 0 4 0 6 0
6 4 4 6 4 4 6 4 4 6 4
6 0 4 0 4 0 6 0 4 0 4
```


## train_3

**input:**
```
4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4 0
```


**output:**
```
6 0 4 0 4 0 6 0 4 0 4
6 4 4 6 4 4 6 4 4 6 4
0 4 0 6 0 4 0 4 0 6 0
```


## train_4

**input:**
```
0 4 0 4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 0 4 0 4 0 4 0 4 0
```


**output:**
```
0 4 0 6 0 4 0 4 0 6 0 4 0 4
6 4 4 6 4 4 6 4 4 6 4 4 6 4
6 0 4 0 4 0 6 0 4 0 4 0 6 0
```


## train_5

**input:**
```
4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4
```


**output:**
```
6 0 4 0 4 0 6 0 4 0
6 4 4 6 4 4 6 4 4 6
0 4 0 6 0 4 0 4 0 6
```

*   **Perception:**
    *   The input grids are always 3 rows high, with varying widths.
    *   The input grids contain only white (0) and yellow (4) pixels.
    *   The output grids are the same dimensions as their corresponding inputs.
    *   The output grids introduce magenta (6) pixels.
    *   The white pixels remain unchanged between input and output.
    *   Some yellow pixels in the input are changed to magenta in the output, while others remain yellow.
    *   The transformation depends on the column position of the yellow pixels. Specifically, yellow pixels located in columns whose index is a multiple of 3 (0, 3, 6, 9, ...) are changed to magenta. Yellow pixels in other columns remain yellow.

*   **Facts:**
    
```yaml
    elements:
      - type: grid
        properties:
          height: 3
          colors_input: [white, yellow]
          colors_output: [white, yellow, magenta]
      - type: pixel
        properties:
          color: [white, yellow, magenta]
          location: [row_index, column_index]
    transformation:
      - action: conditional_color_change
        input_element: pixel
        output_element: pixel
        condition:
          - property: color
            value: yellow
          - property: location.column_index
            constraint: multiple_of_3
        output_change:
          - property: color
            value: magenta
      - action: identity
        input_element: pixel
        output_element: pixel
        condition:
          - or:
              - property: color
                value: white
              - property: color
                value: yellow
              - and:
                  - property: color
                    value: yellow
                  - property: location.column_index
                    constraint: not_multiple_of_3
        output_change:
          - property: color
            value: same_as_input
    ```


*   **Natural Language Program:**
    1.  Create an output grid with the same dimensions as the input grid.
    2.  Iterate through each pixel of the input grid using its row and column index.
    3.  Check if the current pixel's color is yellow (4) AND its column index is divisible by 3 (index % 3 == 0).
    4.  If both conditions are true, set the color of the corresponding pixel in the output grid to magenta (6).
    5.  Otherwise (if the pixel is not yellow, or if its column index is not divisible by 3), copy the color of the input pixel to the corresponding pixel in the output grid.
    6.  Return the completed output grid.
