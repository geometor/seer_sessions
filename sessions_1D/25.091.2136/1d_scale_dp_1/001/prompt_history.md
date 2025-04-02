
## train_1

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 2 0 0 0
```


**output:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 2 0 0 0 0
```

*   **Perception**:
    *   The input and output data are presented as single rows (1D arrays or vectors).
    *   Each input contains a contiguous sequence of a specific color (gray, blue, or orange in the examples) and a single red pixel.
    *   These two elements (the sequence and the red pixel) are separated by one or more white pixels.
    *   The transformation involves extending the colored sequence to the right.
    *   The sequence extension stops immediately before the red pixel.
    *   The white pixels between the original end of the sequence and the red pixel are filled with the color of the sequence.
    *   The red pixel acts as a boundary or stopping point for the expansion.
    *   All other pixels, including the red pixel and white pixels outside the expansion zone, remain unchanged.

*   **YAML Facts**:
    
```yaml
    task_type: sequence_manipulation
    representation: 1D_array
    elements:
      - object: fill_sequence
        description: A contiguous sequence of pixels of a single color (not white or red).
        properties:
          - color: Variable (e.g., gray, blue, orange)
          - start_index: The index of the first pixel in the sequence.
          - end_index: The index of the last pixel in the sequence.
      - object: boundary_pixel
        description: A single red pixel (color 2).
        properties:
          - color: red (2)
          - index: The position of the red pixel.
      - object: background
        description: White pixels (color 0).
    relationships:
      - type: spatial
        description: The fill_sequence appears to the left of the boundary_pixel.
      - type: spatial
        description: There are one or more white pixels between the end of the fill_sequence and the boundary_pixel in the input.
    action:
      - name: expand_sequence
        actor: fill_sequence
        target: white pixels between fill_sequence and boundary_pixel
        effect: Changes the color of the target white pixels to the color of the fill_sequence.
        constraint: Expansion stops at the index immediately preceding the boundary_pixel's index.
    ```


*   **Natural Language Program**:
    1.  Identify the main contiguous sequence of pixels whose color is not white (0) and not red (2). Record its color (let's call it `fill_color`) and the index of its last pixel (`end_index`).
    2.  Identify the index of the single red pixel (color 2) (`boundary_index`).
    3.  Iterate through the indices from `end_index + 1` up to (but not including) `boundary_index`.
    4.  For each index in this range, change the color of the pixel at that index to `fill_color`.
    5.  Leave all other pixels unchanged. The resulting sequence is the output.
