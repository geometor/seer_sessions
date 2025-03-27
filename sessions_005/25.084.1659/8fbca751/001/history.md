
## train_1

**input:**
```
0 8 0 0 8 0 0 0 0 0 0 0
0 8 8 0 8 0 0 8 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
8 8 0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0
```


**output:**
```
2 8 2 2 8 2 2 2 0 0 0 0
2 8 8 2 8 2 2 8 0 0 0 0
2 8 8 8 8 8 8 2 0 0 0 0
8 8 2 2 8 8 8 2 0 0 0 0
0 0 0 0 0 0 0 0 2 8 2 2
0 0 0 0 0 0 0 0 2 8 2 2
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 2 8 2 2
```


## train_2

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 8 0 8
0 0 0 0 0 0 0 0 8 8 0 0
```


**output:**
```
0 0 0 0 2 8 2 2 0 0 0 0
0 0 0 0 8 8 2 2 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 2
0 0 0 0 0 0 0 0 8 8 8 2
0 0 0 0 0 0 0 0 8 8 2 8
0 0 0 0 0 0 0 0 8 8 2 2
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 8 0 0 8 0 0
0 8 8 8 8 0 0
0 0 0 8 0 0 0
0 0 8 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 8 2 2 8 0 0
0 8 8 8 8 0 0
0 2 2 8 2 0 0
0 2 8 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

*   **Perception**:
    *   The task involves transforming an input grid into an output grid of the same dimensions.
    *   The input grids contain only white (0) and azure (8) pixels.
    *   The output grids contain white (0), azure (8), and red (2) pixels.
    *   Azure pixels in the input remain azure in the output.
    *   Some white pixels in the input are changed to red pixels in the output.
    *   The change from white to red occurs specifically for white pixels that are directly adjacent (horizontally or vertically, not diagonally) to at least one azure pixel.
    *   White pixels not directly adjacent to any azure pixels remain white.

*   **Facts**:
    
```yaml
    task_elements:
      - element: grid
        description: A 2D array of pixels with values 0-9 representing colors.
      - element: pixel
        description: A single cell within the grid.
      - element: color
        description: Pixels have colors. Relevant colors are white (0), azure (8), and red (2).
    objects:
      - object: azure_shape
        description: Contiguous areas of azure (8) pixels. These shapes remain unchanged in the output.
      - object: white_pixel
        description: Pixels with the color white (0). Some of these change color.
      - object: red_pixel
        description: Pixels with the color red (2). These appear in the output grid.
    relationships:
      - relationship: adjacency
        description: Pixels can be adjacent horizontally, vertically, or diagonally. The transformation specifically considers horizontal and vertical adjacency (direct neighbors).
    transformation:
      - type: color_change
        input_color: white (0)
        output_color: red (2)
        condition: The white pixel must have at least one direct (horizontal or vertical) neighbor that is azure (8).
      - type: color_preservation
        input_color: azure (8)
        output_color: azure (8)
        condition: Always true for azure pixels.
      - type: color_preservation
        input_color: white (0)
        output_color: white (0)
        condition: The white pixel must NOT have any direct (horizontal or vertical) neighbors that are azure (8).
    grid_properties:
      - property: dimensions
        description: The output grid has the same height and width as the input grid.

    ```


*   **Natural Language Program**:
    1.  Create a new grid (the output grid) with the same dimensions as the input grid.
    2.  Iterate through each pixel of the input grid using its row and column index.
    3.  For each pixel, check its color.
    4.  If the input pixel's color is azure (8), set the corresponding pixel in the output grid to azure (8).
    5.  If the input pixel's color is white (0):
        a.  Examine its direct neighbors (the pixels directly above, below, left, and right, if they exist within the grid boundaries).
        b.  Check if any of these direct neighbors have the color azure (8).
        c.  If at least one direct neighbor is azure (8), set the corresponding pixel in the output grid to red (2).
        d.  If none of the direct neighbors are azure (8), set the corresponding pixel in the output grid to white (0).
    6.  Return the completed output grid.
