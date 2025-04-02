
## train_1

**input:**
```
0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0 0
```

*   **Perception of Task Elements**:
    *   The inputs and outputs are 1-dimensional arrays (or single-row grids).
    *   Each input grid contains a single contiguous block of a non-white color (magenta, azure, orange) surrounded by white pixels (color 0).
    *   The output grid contains the same block of non-white color, but its position is shifted horizontally.
    *   The size of the grid and the size of the non-white block remain unchanged between input and output.
    *   In all examples, the shift is consistently 3 positions to the right.
    *   The pixels vacated by the shift on the left become white (0).

*   **Facts YAML**:
    
```yaml
    task_type: array_manipulation
    dimensionality: 1D
    grid_properties:
      size_preserved: true
    objects:
      - object_type: contiguous_block
        color: non-white (variable: magenta, azure, orange in examples)
        count: 1 per grid
        properties:
          - size_preserved: true
      - object_type: background
        color: white (0)
    actions:
      - action_type: horizontal_shift
        target_object: non-white contiguous_block
        direction: right
        magnitude: 3 positions
        effect:
          - vacated positions are filled with the background color (white)
    relationships:
      - The non-white block is embedded within the white background.
      - The position of the non-white block changes relative to the grid boundaries.
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous sequence (block) of non-white pixels in the input 1D array. Note its color, starting position (index), and length.
    2.  Create a new 1D array of the same length as the input array, and initialize all its elements to white (0).
    3.  Calculate the new starting position for the non-white block by adding 3 to its original starting position.
    4.  Copy the identified non-white block into the new array, starting at the calculated new position.
    5.  The resulting array is the output.
