
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0
```

*   **Perception**: The input and output are both single rows of pixels. Each input contains a contiguous block of a single non-white color surrounded by white pixels. The output shows the same colored block shifted three positions to the right, with the rest of the row remaining white. The color and length of the block are preserved.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively a 1D array or list
    components:
      - object: colored_block
        count: 1
        properties:
          - color: non-white (red, orange, magenta in examples)
          - shape: contiguous horizontal segment
          - size: variable length (11, 10, 6 in examples)
          - location: variable start index within the row
      - object: background
        count: 1
        properties:
          - color: white (0)
          - location: fills the rest of the row
    actions:
      - name: shift_right
        target: colored_block
        parameters:
          - distance: 3 positions
    relationships:
      - type: embedding
        object1: colored_block
        object2: background
        details: The colored block is located within the background.
    constraints:
      - The color of the block remains unchanged.
      - The length of the block remains unchanged.
      - The length of the row remains unchanged.
      - There is only one colored block per input.
    ```


*   **Natural Language Program**:
    1.  Identify the single contiguous block of non-white pixels in the input row. Note its color, its starting index, and its length.
    2.  Create a new output row of the same length as the input row, initially filled entirely with white pixels (0).
    3.  Calculate the new starting index for the colored block by adding 3 to its original starting index.
    4.  Place the identified colored block (with its original color and length) into the output row starting at the calculated new index.
