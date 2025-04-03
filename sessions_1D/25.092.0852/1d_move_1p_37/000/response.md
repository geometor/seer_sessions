*   **Perception:** The input consists of a single row (1D grid) of pixels. Within this row, there is a contiguous block of non-white pixels surrounded by white pixels. The output is a row of the same size where the non-white block has been shifted one position to the right. The pixels vacated by the block become white, and the pixels the block moves into adopt the block's color.

*   **Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (represented as 1xN grid)
    grid_size_input: [1, 9]
    grid_size_output: [1, 9]
    objects:
      - type: contiguous_block
        color: non-white (green, magenta, blue in examples)
        background_color: white (0)
        count_per_example: 1
    actions:
      - type: shift
        direction: right
        distance: 1 pixel
        target: the contiguous_block of non-white pixels
    relationships:
      - The size of the grid remains constant.
      - The color and length of the non-white block remain constant.
      - The block is always surrounded by white pixels before and after the shift.
      - The shift moves the entire block uniformly.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous segment of non-white pixels in the input row.
    2.  Determine the starting index and the color of this segment.
    3.  Create a new output row of the same length as the input row, initialized entirely with white pixels (color 0).
    4.  Copy the identified non-white segment into the new output row, starting at an index that is one greater than the original starting index.