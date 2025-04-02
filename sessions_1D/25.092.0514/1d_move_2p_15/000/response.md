*   **Perception:** The inputs and outputs are single-row grids. Each input contains a contiguous horizontal block of a single non-white color, surrounded by white pixels. The corresponding output shows the same block of non-white pixels shifted two positions to the right within the row. The color and length of the block remain unchanged. The background remains white.

*   **Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (single row)
    input_elements:
      - type: background
        color: white (0)
      - type: object
        description: A contiguous horizontal block of a single non-white color.
        properties:
          - color: variable (blue, azure, gray in examples)
          - length: variable (4 or 5 in examples)
          - position: variable start index
    output_elements:
      - type: background
        color: white (0)
      - type: object
        description: The same contiguous block from the input.
        properties:
          - color: same as input block
          - length: same as input block
          - position: input start index + 2
    transformation:
      action: horizontal_shift
      parameters:
        - object_to_shift: the non-white block
        - direction: right
        - distance: 2 positions
        - constraints: background remains white, object properties (color, length) preserved.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input row. Note its color, length, and starting position (index of the leftmost pixel of the block).
    2.  Create an output row of the same length as the input row, initially filled with white pixels (0).
    3.  Place the identified block (with its original color and length) into the output row, starting at the position corresponding to the input starting position plus 2.