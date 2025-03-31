
## train_1

**input:**
```
7 5 7 7 5 5 7 7 5 7
0 0 0 7 7 5 5 7 7 5
0 0 0 7 5 5 7 5 7 7
0 0 0 5 7 5 7 5 7 7
7 7 5 5 5 5 7 5 5 5
7 5 7 5 7 7 5 5 7 5
7 5 7 7 5 5 5 7 7 7
7 0 0 5 5 5 7 5 7 5
5 0 0 7 5 0 0 7 5 7
7 0 0 5 5 0 0 5 7 7
```


**output:**
```
7 0 0 7 5 0 0 7 5 7
7 0 0 7 7 0 0 0 0 0
7 0 0 7 7 7 7 0 0 0
7 7 7 7 7 7 7 0 0 0
7 7 7 5 5 7 7 5 5 5
7 7 7 5 7 7 7 5 7 5
7 7 7 7 5 7 7 7 7 7
7 7 7 5 5 7 7 5 7 5
5 7 7 7 5 7 7 7 5 7
7 7 7 5 5 7 7 5 7 7
```


## train_2

**input:**
```
7 7 5 7 5 7 5 7
7 5 7 7 5 7 7 7
7 7 5 7 7 0 0 0
5 7 7 5 7 0 0 0
7 7 7 7 7 0 0 0
5 7 5 7 5 5 7 7
```


**output:**
```
7 7 5 7 5 7 5 7
7 5 7 7 5 7 7 7
0 0 0 7 7 7 7 7
0 0 0 7 7 7 7 7
0 0 0 7 7 7 7 7
5 7 5 7 5 5 7 7
```


## train_3

**input:**
```
5 5 5 7 0 0 0 0 5 5 5 7
5 7 5 5 0 0 0 0 7 5 5 5
5 7 7 7 0 0 0 0 7 5 7 7
5 7 7 5 5 7 5 5 5 7 7 5
7 7 5 7 5 5 7 5 5 7 7 5
7 5 7 5 5 5 5 5 5 7 7 5
7 5 7 7 5 5 5 5 0 0 0 0
7 7 7 5 7 7 5 5 0 0 0 0
5 7 7 7 7 7 5 7 5 7 5 5
7 5 5 5 7 5 5 7 5 5 7 5
7 5 0 5 7 5 7 7 5 7 5 5
7 5 0 7 5 5 5 5 5 7 5 5
```


**output:**
```
5 5 0 7 7 7 7 7 5 5 5 7
5 7 0 5 7 7 7 7 7 5 5 5
5 7 7 7 7 7 7 7 7 5 7 7
5 7 7 5 7 7 7 7 5 7 7 5
7 7 7 7 7 7 7 7 5 7 7 5
7 5 7 5 7 7 7 7 5 7 7 5
0 0 0 0 7 7 7 7 7 7 7 7
0 0 0 0 7 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7 5 7 5 5
7 5 7 5 0 0 0 0 5 5 7 5
7 5 7 5 0 0 0 0 5 7 5 5
7 5 7 7 0 0 0 0 5 7 5 5
```

*   **Perception:**
    The task involves transforming pixels in a grid based on their local neighborhood. The transformation logic centers around the interaction between three specific colors: white (0), gray (5), and orange (7). The core rule depends on whether a pixel has *both* a gray neighbor and an orange neighbor within its 3x3 Moore neighborhood (including diagonals). The pixel's own color determines the outcome of the transformation when this neighborhood condition is met. Other colors and pixels not meeting the neighborhood condition remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: pixel_transformation
    transformation_scope: local_neighborhood
    neighborhood_type: Moore (3x3 including diagonals)
    key_colors:
      - name: white
        value: 0
      - name: gray
        value: 5
      - name: orange
        value: 7
    conditions:
      - name: neighbor_check
        description: Check if a pixel has at least one gray (5) neighbor AND at least one orange (7) neighbor.
        applies_to: all pixels
      - name: white_pixel_rule
        description: If neighbor_check is true AND the pixel's color is white (0), change the pixel's color to orange (7).
        input_color: 0
        output_color: 7
      - name: non_white_pixel_rule
        description: If neighbor_check is true AND the pixel's color is NOT white (0), change the pixel's color to white (0).
        input_color: non-0
        output_color: 0
      - name: default_rule
        description: If neighbor_check is false, the pixel's color remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Create a new grid with the same dimensions as the input grid, initially copying all pixel values from the input.
    2.  Iterate through each pixel (cell) of the input grid using its row and column index.
    3.  For the current pixel, examine its 8 neighbors (Moore neighborhood: adjacent horizontally, vertically, and diagonally).
    4.  Determine if at least one neighbor has the color gray (5) AND at least one neighbor has the color orange (7).
    5.  **If** this neighborhood condition (having both a gray and an orange neighbor) is **true**:
        *   Check the color of the current pixel in the *input* grid.
        *   **If** the current pixel's color is white (0), set the corresponding pixel in the *output* grid to orange (7).
        *   **Else if** the current pixel's color is *not* white (0), set the corresponding pixel in the *output* grid to white (0).
    6.  **Else if** the neighborhood condition (having both a gray and an orange neighbor) is **false**:
        *   The corresponding pixel in the *output* grid keeps its original color (copied in step 1).
    7.  After iterating through all pixels, the new grid represents the final output.
