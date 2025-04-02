
## train_1

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
```

*   **Perception:** The task involves transforming a single row (a 1xN grid) containing one contiguous block of a non-white color surrounded by white pixels. The transformation shifts this non-white block horizontally to the right by a fixed amount, leaving the surrounding white pixels unchanged. The color and length of the block are preserved. By observing the examples, the shift amount is consistently 3 positions to the right.

*   **YAML Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (represented as 1xN 2D grid)
    input_features:
      - background_color: white (0)
      - objects:
          - count: 1
          - shape: contiguous horizontal block
          - color: non-white (variable, e.g., gray, blue, orange)
          - properties:
              - length: variable
              - position: variable
    transformation:
      - type: translation
      - object_involved: the single non-white block
      - direction: right
      - magnitude: 3 positions
      - preservation:
          - object_color
          - object_shape (length)
          - grid_size
          - background_color
    output_features:
      - background_color: white (0)
      - objects:
          - count: 1
          - shape: contiguous horizontal block (same as input)
          - color: same as input object
          - properties:
              - length: same as input object
              - position: input position shifted right by 3
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input row. Note its color, starting position, and ending position.
    2.  Create an output row of the same size as the input row, filled entirely with white pixels (0).
    3.  Calculate the new starting position by adding 3 to the original starting position.
    4.  Calculate the new ending position by adding 3 to the original ending position.
    5.  Fill the segment of the output row from the new starting position to the new ending position (inclusive) with the color of the original non-white block.
