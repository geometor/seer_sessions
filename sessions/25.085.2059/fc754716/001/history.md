
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 1 1 1 1 1 1
```


## train_2

**input:**
```
0 0 0
0 0 0
0 3 0
0 0 0
0 0 0
```


**output:**
```
3 3 3
3 0 3
3 0 3
3 0 3
3 3 3
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 6
```


## train_4

**input:**
```
0 0 0
0 2 0
0 0 0
```


**output:**
```
2 2 2
2 0 2
2 2 2
```

*   **Perception:** Each input grid contains a single non-white pixel within a background of white pixels. The corresponding output grid has the same dimensions as the input grid. The transformation involves using the color of the single non-white pixel from the input to draw a border around the output grid. The interior of the output grid (excluding the border) is filled with white pixels. The original position of the non-white pixel in the input does not seem relevant to the final output structure, only its color matters.

*   **Facts:**
    
```yaml
    examples:
      - name: train_1
        input:
          grid_dimensions: [5, 7]
          objects:
            - type: pixel
              color: blue (1)
              location: [2, 3] # row, col
            - type: background
              color: white (0)
        output:
          grid_dimensions: [5, 7]
          objects:
            - type: border
              color: blue (1)
            - type: interior
              color: white (0)
          relationship: The border color is determined by the color of the single non-white pixel in the input.
      - name: train_2
        input:
          grid_dimensions: [5, 3]
          objects:
            - type: pixel
              color: green (3)
              location: [2, 1]
            - type: background
              color: white (0)
        output:
          grid_dimensions: [5, 3]
          objects:
            - type: border
              color: green (3)
            - type: interior
              color: white (0)
          relationship: The border color is determined by the color of the single non-white pixel in the input.
      - name: train_3
        input:
          grid_dimensions: [5, 5]
          objects:
            - type: pixel
              color: magenta (6)
              location: [2, 2]
            - type: background
              color: white (0)
        output:
          grid_dimensions: [5, 5]
          objects:
            - type: border
              color: magenta (6)
            - type: interior
              color: white (0)
          relationship: The border color is determined by the color of the single non-white pixel in the input.
      - name: train_4
        input:
          grid_dimensions: [3, 3]
          objects:
            - type: pixel
              color: red (2)
              location: [1, 1]
            - type: background
              color: white (0)
        output:
          grid_dimensions: [3, 3]
          objects:
            - type: border
              color: red (2)
            - type: interior
              color: white (0)
          relationship: The border color is determined by the color of the single non-white pixel in the input.
    common_rule:
      input_structure: A grid containing exactly one non-white pixel.
      output_structure: A grid of the same dimensions as the input, with a border matching the color of the input's non-white pixel, and a white interior.
      action: Identify the color of the unique non-white pixel in the input grid. Create an output grid of identical dimensions. Fill the border pixels (top row, bottom row, first column, last column) of the output grid with the identified color. Fill all other (interior) pixels with white (0).
    ```


*   **Natural Language Program:**
    1.  Receive the input grid.
    2.  Identify the single pixel in the input grid that is not white (color 0). Record its color.
    3.  Determine the dimensions (height and width) of the input grid.
    4.  Create a new output grid with the same height and width.
    5.  Iterate through each pixel position (row `r`, column `c`) in the new grid.
    6.  If the pixel position is on the border (i.e., `r` is 0, `r` is height-1, `c` is 0, or `c` is width-1), set the pixel's color to the color identified in step 2.
    7.  Otherwise (if the pixel is not on the border), set the pixel's color to white (0).
    8.  Return the completed output grid.
