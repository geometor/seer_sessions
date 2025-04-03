
## train_1

**input:**
```
0 0 0 0 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 4 0 0 0 4 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 8 8 8 8 8 8 0 0 0
```


**output:**
```
0 0 0 0 8 0 0 0 0 8 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 8 8 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 8 0 0 8 0 0
```

*   **Perception**: The task operates on a single row (1D grid). Each input row contains a single contiguous horizontal segment of a non-white color, surrounded by white pixels (color 0). The transformation modifies this non-white segment. Specifically, it retains the first and the last pixel of the segment in their original positions and color, while changing all the pixels *between* the first and last pixel to white (color 0). The surrounding white pixels remain unchanged.

*   **Facts**:
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (single row)
    input_features:
      - background_color: white (0)
      - object:
          type: contiguous_horizontal_segment
          color: non-white (e.g., yellow(4), azure(8))
          properties:
            - start_index
            - end_index
            - length: (end_index - start_index + 1) >= 1
    output_features:
      - background_color: white (0)
      - modified_object:
          based_on: input_object
          pixels_at_start_index: unchanged (same color and position as input)
          pixels_at_end_index: unchanged (same color and position as input)
          pixels_between_start_and_end: changed to white (0)
    relationships:
      - The output grid dimensions are identical to the input grid dimensions.
      - The transformation preserves the locations and colors of the segment's endpoints.
      - The transformation replaces the interior pixels of the segment with the background color.
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous horizontal segment of non-white pixels in the input row. Determine its start index and end index.
    2.  Create an output row of the same size as the input row, initially filled with the background color (white, 0).
    3.  Copy the pixel value from the input row at the start index to the output row at the start index.
    4.  If the start index and end index are different (i.e., the segment length is greater than 1), copy the pixel value from the input row at the end index to the output row at the end index.
    5.  All other pixels in the output row remain white (0).
