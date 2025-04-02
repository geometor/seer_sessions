*   **Perception of Elements:**
    *   The input and output are single rows (1D arrays) of pixels.
    *   Each input contains a single contiguous block of non-white pixels (azure, yellow, or magenta in the examples) surrounded by white pixels (0).
    *   The output contains the same contiguous block of non-white pixels, but its position is shifted horizontally compared to the input.
    *   The overall length of the row remains the same between input and output.
    *   The block of non-white pixels is always shifted exactly 3 positions to the right.
    *   The pixels that were occupied by the block in the input become white in the output (unless they are re-occupied by the shifted block).
    *   The pixels to the left of the shifted block become white.

*   **YAML Facts:**
    
```yaml
    task_type: object_transformation
    input_dimensionality: 1D (single row)
    output_dimensionality: 1D (single row)
    objects:
      - type: contiguous_block
        properties:
          color: non-white (variable, e.g., azure, yellow, magenta)
          shape: horizontal segment
          count: 1 per input
      - type: background
        properties:
          color: white (0)
    actions:
      - name: identify
        target: contiguous_block (non-white)
        details: Find the start index, end index, color, and length of the block.
      - name: shift
        target: contiguous_block (non-white)
        details: Move the block horizontally to the right by a fixed amount.
        parameters:
          shift_amount: 3 positions
      - name: fill
        target: background
        details: Ensure the output array has the same length as the input, filling positions not occupied by the shifted block with white pixels.
    relationships:
      - type: relative_position
        between: [contiguous_block, background]
        details: The non-white block is embedded within the white background.
      - type: transformation
        input: contiguous_block (at original position)
        output: contiguous_block (at shifted position)
        rule: output_start_index = input_start_index + 3
    constraints:
      - The length of the input and output rows are identical.
      - There is exactly one contiguous block of non-white pixels in the input.
      - The shift amount is constant (3 positions to the right).
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous block of non-white pixels within the input row. Note its color, its starting position (index), and its length.
    2.  Create a new output row of the same length as the input row, initially filled entirely with white pixels (0).
    3.  Calculate the new starting position for the block by adding 3 to its original starting position.
    4.  Place the identified block (with its original color and length) into the new output row, starting at the calculated new position.