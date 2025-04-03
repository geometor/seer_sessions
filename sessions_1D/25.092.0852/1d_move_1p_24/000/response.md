**Perception:**

The input consists of a single row of pixels. Within this row, there is a contiguous block of a single non-white color, surrounded by white pixels (color 0). The output is also a single row of pixels of the same length. The transformation involves shifting the non-white block exactly one position to the right. The color and the length of the block remain unchanged. The pixel at the original starting position of the block becomes white, and the white pixel immediately following the original ending position of the block takes on the color of the block.

**Facts:**


```yaml
- task_type: array_manipulation
- grid_dimensionality: 1D (single row)
- elements:
    - type: pixel
      attributes:
        - color: integer (0-9)
        - position: index within the row
- objects:
    - type: contiguous_block
      description: A sequence of one or more adjacent pixels sharing the same non-white color.
      attributes:
        - color: The non-white color of the pixels in the block.
        - length: The number of pixels in the block.
        - start_index: The index of the first pixel in the block.
        - end_index: The index of the last pixel in the block.
      relationships:
        - Surrounded by white pixels (color 0).
      constraints:
        - Exactly one such block exists in the input.
- actions:
    - action: shift_right
      target: contiguous_block
      parameters:
        - amount: 1 position
      effects:
        - The start_index of the block increases by 1.
        - The end_index of the block increases by 1.
        - The pixel at the original start_index becomes white (0).
        - The pixel at the original end_index + 1 takes the color of the block.
- transformation_rule:
    - Find the contiguous block of non-white pixels.
    - Create an output row of the same length, initially all white.
    - Place the non-white block in the output row, shifted one position to the right compared to its input position.
```


**Natural Language Program:**

1.  Identify the single contiguous block of non-white pixels in the input row. Note its color, starting index, and length.
2.  Create a new row of the same length as the input, filled entirely with white pixels (0).
3.  Copy the identified non-white block into the new row, starting at an index one greater than its original starting index. The length and color of the block remain the same.