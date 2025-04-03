*   **Perception:**
    The input and output are single rows of pixels. Each input contains a single contiguous horizontal block of a non-white color (blue '1' or red '2'), surrounded by white pixels ('0'). The transformation involves shifting this colored block one position to the right. The length of the block and its color remain the same. The pixel that was originally the leftmost pixel of the block becomes white, and the white pixel immediately to the right of the original block takes on the block's color.

*   **Facts:**
    
```yaml
    task_type: array_manipulation
    dimensionality: 1D # Effectively 1D, presented as 1xN grid
    input_features:
      - single_row: true
      - contains_object: true
        object_description: A contiguous block of a single non-white color.
      - background_color: 0 (white)
      - object_color: variable (1 or 2 in examples)
      - object_shape: horizontal segment
      - object_count: 1
    output_features:
      - single_row: true
      - same_dimensions_as_input: true
      - contains_object: true
        object_description: Same object as input, shifted.
      - background_color: 0 (white)
      - object_color: Same as input object color.
      - object_shape: horizontal segment (same length as input object)
      - object_count: 1
    transformation:
      - type: translation
      - description: The non-white block is shifted one position to the right.
      - details:
        - Find the contiguous block of non-white color C.
        - Let its starting index be 'start' and ending index be 'end'.
        - In the output, the pixel at 'start' becomes white (0).
        - In the output, the pixel at 'end + 1' becomes color C.
        - All other pixels retain their original color.
    relationships:
      - The non-white block is always surrounded by white pixels in the input.
      - The length and color of the block are preserved in the output.
      - The grid size remains constant.
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous block of non-white pixels in the input row. Note its color (let's call it `C`) and its starting and ending indices (let's call them `start_index` and `end_index`).
    2.  Create a new row of the same size as the input, initially filled with the same pixel values as the input row.
    3.  Change the pixel value at `start_index` in the new row to white (0).
    4.  Change the pixel value at `end_index + 1` in the new row to the color `C`.
    5.  The resulting new row is the output.