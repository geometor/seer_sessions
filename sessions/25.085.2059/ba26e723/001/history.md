
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

*   **Perception:** The task involves transforming a 3-row grid containing white (0) and yellow (4) pixels into a grid of the same dimensions. The output grid introduces magenta (6) pixels. The transformation appears to be column-based. By observing the examples, it becomes clear that yellow pixels located in specific columns are changed to magenta, while all other pixels retain their original color. These specific columns correspond to indices that are multiples of 3 (0, 3, 6, 9, 12, ...).

*   **Facts:**
    
```yaml
    task_type: color_transformation
    grid_properties:
      - height: 3 (constant across examples)
      - width: variable
    objects:
      - type: pixel
        colors_input: [white (0), yellow (4)]
        colors_output: [white (0), yellow (4), magenta (6)]
    relationships:
      - type: position
        property: column_index
    actions:
      - type: conditional_color_change
        condition:
          - pixel_color == yellow (4)
          - column_index % 3 == 0
        result:
          - change_pixel_color: magenta (6)
        otherwise:
          - keep_original_color
    ```


*   **Natural Language Program:**
    1.  Iterate through each column of the input grid, identified by its column index (starting from 0).
    2.  Check if the column index is exactly divisible by 3 (i.e., the remainder of the division `column_index / 3` is 0).
    3.  If the column index is a multiple of 3, then iterate through each pixel within that column.
    4.  If a pixel in this column has the color yellow (4), change its color to magenta (6).
    5.  If the column index is not a multiple of 3, or if a pixel in a multiple-of-3 column is not yellow, keep the pixel's original color.
    6.  Construct the output grid with the potentially modified pixel colors.
