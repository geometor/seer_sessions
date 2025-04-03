
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
```


**output:**
```
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0
```


**output:**
```
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
```

*   **Perception:** The task operates on single-row grids. The core operation involves identifying contiguous horizontal segments of non-white pixels. For each identified segment, the transformation retains the first and last pixel of the segment while converting all the pixels located strictly between them to white (color 0). White pixels in the input remain white in the output. Segments of length 1 or 2 remain unchanged.

*   **Facts YAML:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (single row)
    background_color: white (0)
    objects:
      - name: colored_segment
        description: A contiguous horizontal sequence of non-white pixels.
        properties:
          - start_index: The column index of the first pixel in the segment.
          - end_index: The column index of the last pixel in the segment.
          - length: The number of pixels in the segment (end_index - start_index + 1).
          - color: The color value of the pixels in the segment (all pixels in a segment share the same non-white color in the examples, but the rule should apply even if colors mix within a segment, identifying the segment boundary by non-white vs white).
      - name: white_pixel
        description: A pixel with the background color (0).
    actions:
      - name: hollow_segment
        description: Modifies a colored_segment in the output grid.
        condition: Applies only if the segment length is greater than 2.
        steps:
          - Keep the pixel at the start_index unchanged.
          - Keep the pixel at the end_index unchanged.
          - Change all pixels from start_index + 1 to end_index - 1 to white (0).
    relationships:
      - The transformation is applied independently to each identified colored_segment.
      - White pixels in the input remain white in the output.
      - Colored segments of length 1 or 2 are unchanged in the output because there are no pixels strictly between the start and end indices.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input row to serve as the output row.
    2.  Iterate through the input row to find all contiguous horizontal segments of non-white pixels. For each segment, record its start index and end index.
    3.  For each identified segment:
        a.  Calculate the length of the segment.
        b.  If the length is greater than 2:
            i.  Iterate through the column indices from `start_index + 1` up to, but not including, `end_index`.
            ii. For each index in this range, set the corresponding pixel in the *output* row to white (0).
    4.  Return the modified output row.
