
## train_1

**input:**
```
3 0 0 0 3
0 3 0 3 0
0 0 3 0 0
```


**output:**
```
3 0 0 0 3 3 0 0 0 3
0 3 0 3 0 0 3 0 3 0
0 0 3 0 0 0 0 3 0 0
```


## train_2

**input:**
```
2 0 2
2 0 2
2 2 2
```


**output:**
```
2 0 2 2 0 2
2 0 2 2 0 2
2 2 2 2 2 2
```


## train_3

**input:**
```
4 4 4
4 0 4
4 0 4
4 0 4
4 0 4
4 4 4
```


**output:**
```
4 4 4 4 4 4
4 0 4 4 0 4
4 0 4 4 0 4
4 0 4 4 0 4
4 0 4 4 0 4
4 4 4 4 4 4
```

*   **Perception:** The task involves manipulating the entire input grid as a single object. In each example, the output grid is formed by duplicating the input grid and placing the copy directly to the right of the original. The height of the grid remains unchanged, while the width is doubled. The colors and arrangement of pixels within the original grid are preserved in both the left and right halves of the output grid.

*   **Facts:**
    
```yaml
    task_type: grid_manipulation
    transformation: duplication_concatenation
    objects:
      - type: input_grid
        attributes:
          - height: H
          - width: W
      - type: output_grid
        attributes:
          - height: H # Same as input
          - width: 2 * W # Double the input width
    relationship:
      - type: spatial_arrangement
        description: The output grid is formed by concatenating the input grid horizontally with an identical copy of itself.
        details:
          - The left half (columns 0 to W-1) of the output grid is identical to the input grid.
          - The right half (columns W to 2*W-1) of the output grid is identical to the input grid.
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Create a new output grid with height H and width 2*W.
    3.  Copy the pixel values from the input grid (row r, column c) to the corresponding positions in the left half of the output grid (row r, column c) for all rows r from 0 to H-1 and columns c from 0 to W-1.
    4.  Copy the pixel values from the input grid (row r, column c) to the corresponding positions in the right half of the output grid (row r, column c + W) for all rows r from 0 to H-1 and columns c from 0 to W-1.
    5.  Return the newly created output grid.
