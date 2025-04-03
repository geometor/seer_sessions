
## train_1

**input:**
```
2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   The inputs and outputs are single rows (1D grids).
    *   Each input row contains a single contiguous horizontal segment of a non-white color, surrounded by white pixels (0).
    *   The non-white colors are different in each example: red (2), azure (8), and orange (7).
    *   The length of the non-white segment varies: 8 pixels, 8 pixels, and 10 pixels.
    *   The position of the non-white segment also varies.
    *   In the output, the non-white segment is modified: only the first and the last pixel of the original segment retain their color. All pixels that were originally *between* the first and last pixel of the segment are changed to white (0).
    *   The white pixels outside the original segment remain unchanged.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D (single row)
    background_color: white (0)
    objects:
      - type: contiguous_horizontal_segment
        properties:
          color: non-white (variable, e.g., red, azure, orange)
          length: variable (>= 2)
          position: variable (start_index, end_index)
    actions:
      - name: modify_segment
        target: the non-white segment
        effect: keep the color of the first and last pixel of the segment, change all pixels between them to the background color (white).
    relationships:
      - The position and color of the first pixel of the output segment match the first pixel of the input segment.
      - The position and color of the last pixel of the output segment match the last pixel of the input segment.
      - All other pixels in the output grid are white (background color).
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous horizontal segment of non-white pixels in the input row. Note its color, starting index, and ending index.
    2.  Create an output row of the same dimensions as the input row, initially filled with the background color (white, 0).
    3.  Copy the pixel from the starting index of the identified segment in the input to the same index in the output row.
    4.  If the starting index is different from the ending index (i.e., the segment length is greater than 1), copy the pixel from the ending index of the identified segment in the input to the same index in the output row.
    5.  The resulting output row contains the transformed segment (only endpoints visible) against a white background.
