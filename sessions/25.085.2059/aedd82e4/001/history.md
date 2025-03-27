
## train_1

**input:**
```
2 2 0 0
0 2 0 0
2 2 0 2
0 0 0 0
0 2 2 2
```


**output:**
```
2 2 0 0
0 2 0 0
2 2 0 1
0 0 0 0
0 2 2 2
```


## train_2

**input:**
```
2 2 2 0
0 2 0 0
0 0 0 2
0 2 0 0
```


**output:**
```
2 2 2 0
0 2 0 0
0 0 0 1
0 1 0 0
```


## train_3

**input:**
```
2 2 0
2 0 2
0 2 0
```


**output:**
```
2 2 0
2 0 1
0 1 0
```


## train_4

**input:**
```
0 2 2
0 2 2
2 0 0
```


**output:**
```
0 2 2
0 2 2
1 0 0
```

*   **Perception:**
    *   The input and output are grids of pixels with different colors.
    *   The primary colors involved are red (`2`), white (`0`), and blue (`1`).
    *   The transformation seems to involve changing the color of specific pixels based on their neighborhood context.
    *   Comparing the input and output grids, only one pixel changes color: the red pixel at row 2, column 3 (0-indexed) becomes blue.
    *   Examining the neighborhood (8 adjacent cells, including diagonals) of the changed pixel in the input grid reveals that all its neighbors are white (`0`).
    *   Other red pixels in the input grid have at least one non-white neighbor and remain unchanged in the output grid.
    *   The transformation rule appears to target isolated red pixels.

*   **Facts:**
    
```yaml
    task_type: pixel_transformation
    elements:
      - type: grid
        properties:
          - colors: [white, blue, red] # 0, 1, 2
      - type: pixel
        properties:
          - color: red (value 2)
          - location: coordinates (row, column)
          - neighborhood: 8 adjacent pixels (including diagonals)
    actions:
      - name: change_color
        target: pixel
        condition:
          - type: color_is
            value: red (2)
          - type: neighborhood_check
            property: all_neighbors_are_color
            value: white (0)
        result:
          - property: color
            new_value: blue (1)
    relationships:
      - type: spatial
        description: Adjacency (8 neighbors) determines if a pixel is isolated.
    output_rule: Pixels that do not meet the condition remain unchanged.

    ```


*   **Natural Language Program:**
    1.  Iterate through each pixel in the input grid.
    2.  For each pixel, check if its color is red (`2`).
    3.  If the pixel is red, examine its 8 neighboring pixels (up, down, left, right, and diagonals). Handle boundary conditions where neighbors might not exist (consider non-existent neighbors as not being white).
    4.  Count how many of the existing neighbors are white (`0`).
    5.  Determine the total number of existing neighbors for the current pixel.
    6.  If the count of white neighbors equals the total number of existing neighbors (meaning all existing neighbors are white), change the color of the current pixel to blue (`1`) in the output grid.
    7.  If the pixel is not red, or if it is red but does not have all white neighbors, keep its original color in the output grid.
    8.  The output grid has the same dimensions as the input grid.
