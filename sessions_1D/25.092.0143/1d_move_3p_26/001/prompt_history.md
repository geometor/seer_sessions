
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** Each task example consists of a single row (1D grid). The input row contains a contiguous horizontal segment of a single non-white color (azure, orange, or blue) surrounded by white pixels. The output row shows this same colored segment shifted three positions to the right, maintaining its color and length, with the surrounding pixels remaining white.

*   **YAML Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D # Represented as a single row
    input_characteristics:
      - background_color: white (0)
      - contains_single_object: true
      - object_type: contiguous_horizontal_segment
      - object_properties:
          - color: non-white (varies: azure, orange, blue)
          - length: variable (15, 11, 8 in examples)
          - surrounded_by: background_color
    output_characteristics:
      - background_color: white (0)
      - contains_single_object: true
      - object_type: contiguous_horizontal_segment
      - object_properties:
          - color: same_as_input_object
          - length: same_as_input_object
          - surrounded_by: background_color
    transformation:
      - action: horizontal_shift
      - target: the_non_white_segment
      - direction: right
      - distance: 3_pixels
      - preserves:
          - object_color
          - object_length
          - grid_dimensions
    relationship:
      - The output object's start position is the input object's start position plus 3.
      - The output grid is identical to the input grid, except the non-white segment is moved 3 positions to the right.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous horizontal segment of non-white pixels in the input row. Note its color, length, and starting position.
    2.  Create an output row of the same length as the input row, filled entirely with the background color (white, 0).
    3.  Determine the new starting position for the segment by adding 3 to its original starting position.
    4.  Place the identified segment (with its original color and length) into the output row starting at the calculated new position.
