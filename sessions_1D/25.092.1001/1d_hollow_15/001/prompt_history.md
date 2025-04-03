
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 7 0 0 0 7 0 0
```


## train_2

**input:**
```
0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0 0
```


**output:**
```
0 0 0 7 0 0 0 0 0 0 0 0 0 7 0 0 0
```


## train_3

**input:**
```
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0
```


**output:**
```
0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0
```

*   **Perception:**
    *   The input and output grids are single rows (1D arrays).
    *   Each input contains a single contiguous horizontal segment of a non-white color (orange or red in the examples) surrounded by white pixels.
    *   The output grids retain the same dimensions as the input grids.
    *   In the output, the contiguous non-white segment from the input is modified: only the pixels at the beginning and end of the segment retain their original color. All pixels *between* the start and end points of the segment are changed to white (0).
    *   The white pixels outside the original segment remain white.
    *   The specific non-white color used (orange or red) is preserved at the endpoints but does not affect the logic of *which* pixels change.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    input_dimensionality: 1D (represented as 1xN grid)
    output_dimensionality: 1D (same dimensions as input)
    objects:
      - type: segment
        count: 1 per input grid
        definition: A contiguous sequence of identical non-white pixels.
        properties:
          - color: The specific non-white color (e.g., orange, red).
          - start_index: The index of the first pixel in the segment.
          - end_index: The index of the last pixel in the segment.
          - length: The number of pixels in the segment.
    background_color: white (0)
    transformation:
      - action: identify_segment
        target: The non-white segment in the input grid.
        details: Find its start index, end index, and color.
      - action: modify_segment
        target: The identified segment within the grid.
        rule: Keep the original color at the start_index and end_index. Change all pixels between the start_index and end_index to the background_color (white).
        output_relation: The output grid retains the background pixels and the modified segment (endpoints only).
    invariance:
      - Grid dimensions remain constant.
      - The background color remains constant.
      - The color of the segment's endpoints remains constant.
      - The position of the segment's endpoints remains constant.
    variance:
      - The interior pixels of the segment change color (to white).
      - The specific non-white color of the segment can vary between examples (orange, red).
      - The length and position of the segment can vary between examples.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the basis for the output grid.
    2.  Iterate through the input grid to find the first non-white pixel. Record its index as `start_index` and its color as `segment_color`. If no non-white pixel is found, the input grid is the output grid, and the process stops.
    3.  Continue iterating from `start_index` to find the last consecutive pixel with the `segment_color`. Record its index as `end_index`.
    4.  Iterate through the output grid from the index `start_index + 1` up to (but not including) `end_index`.
    5.  For each index in this range, set the pixel value in the output grid to white (0).
    6.  The pixels at `start_index` and `end_index` in the output grid retain their original `segment_color`. Pixels outside this range also retain their original color (which is white in the examples).
    7.  Return the modified grid as the output.
