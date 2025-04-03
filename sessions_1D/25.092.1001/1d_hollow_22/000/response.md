*   **Perception:** The input and output are 1D arrays (or single rows/columns of a 2D grid) of pixels. Each input contains a single contiguous block of non-white pixels (yellow or green) surrounded by white pixels. The transformation modifies this block. Specifically, it keeps the first and last pixel of the block unchanged, while changing all the pixels *between* the first and last pixels to white (0). Pixels outside the original block remain white.

*   **YAML Facts:**
    
```yaml
    task_type: array_transformation_1d
    input_features:
      - description: A 1D array of pixels.
      - properties:
          - contains a single contiguous block of non-white pixels.
          - non-white block is surrounded by white pixels (0).
    output_features:
      - description: A 1D array of pixels, same length as the input.
      - properties:
          - derived from the input array.
          - the non-white block from the input is modified.
    transformation:
      - description: Modifies the contiguous non-white block.
      - steps:
          - Identify the start and end indices of the non-white block.
          - Keep the pixel at the start index (color and position).
          - Keep the pixel at the end index (color and position).
          - Replace all pixels strictly between the start and end indices with white (0).
          - Pixels outside the original block remain unchanged (white).
    objects:
      - id: background
        color: white (0)
        role: static background
      - id: block
        color: non-white (e.g., yellow (4), green (3))
        shape: contiguous horizontal segment
        role: object being modified
    relationships:
      - type: spatial
        description: The non-white block is embedded within the white background.
    actions:
      - action: identify_block
        target: input array
        output: start index, end index, color of the block
      - action: modify_block
        target: block identified in the input
        result: A new block where only the first and last pixels retain the original color, and the intermediate pixels become white (0).
      - action: construct_output
        input: original array, identified block info, modification rule
        output: the final output array
    constraints:
      - Only one non-white block per input array in the examples.
      - Block length must be at least 2 for modification to have an effect (a block of length 1 would remain unchanged). If the block length is 2, it also remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Scan the input array to find the first and last indices of the contiguous sequence of non-white pixels (the "block"). Note the color of this block.
    2.  Create a new output array of the same size as the input, initially filled with white pixels (0).
    3.  Copy all white pixels from the input array to the corresponding positions in the output array.
    4.  If a non-white block was found:
        a.  Place the block's original color at the starting index of the block in the output array.
        b.  Place the block's original color at the ending index of the block in the output array.
        c.  Ensure all positions in the output array strictly between the starting and ending indices of the block are filled with white pixels (0).