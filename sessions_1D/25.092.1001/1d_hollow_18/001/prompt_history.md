
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```


## train_3

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on 1D arrays of integers (colors). The input arrays contain contiguous sequences (blocks) of a single non-white color, surrounded by white pixels (0). The transformation identifies these non-white blocks. For each block found, it preserves the first and last pixel of the block and replaces all the pixels *between* the first and the last with white (0). Pixels outside these blocks (the surrounding white pixels) are unchanged. The color of the block itself (azure, blue, orange in the examples) does not affect the logic, only its non-white status.

*   **Facts:**
    
```yaml
    task_type: array_transformation
    input_data: 1D array of integers (colors)
    output_data: 1D array of integers (colors) of the same length as the input
    elements:
      - element: pixel
        properties:
          - color: integer (0-9)
          - position: index in the array
      - element: block
        description: A contiguous sequence of one or more pixels of the same non-white color.
        properties:
          - color: The non-white color of the pixels in the block.
          - start_index: The index of the first pixel in the block.
          - end_index: The index of the last pixel in the block.
          - length: The number of pixels in the block (end_index - start_index + 1).
    transformation:
      action: hollow_block
      description: Modifies the pixels within identified blocks.
      target: Contiguous blocks of non-white pixels.
      rule:
        - Keep the pixel at the start_index of the block unchanged.
        - Keep the pixel at the end_index of the block unchanged.
        - Change the color of all pixels between the start_index and end_index (exclusive) to white (0).
      unaffected_elements: Pixels that are not part of a non-white block (i.e., white pixels) remain unchanged.
    relationships:
      - Pixels within a block are adjacent and share the same non-white color.
      - The transformation preserves the endpoints of the blocks while changing their interior.
    ```


*   **Natural Language Program:**
    1.  Initialize an output array as a copy of the input array.
    2.  Iterate through the input array to identify contiguous blocks of non-white pixels (pixels with value > 0).
    3.  For each identified block:
        a.  Determine the start index and end index of the block.
        b.  If the block has a length greater than 2 (i.e., start index is not equal to end index - 1), iterate from the index `start_index + 1` up to (but not including) `end_index`.
        c.  For each index in this range, set the corresponding value in the *output* array to 0 (white).
    4.  Return the modified output array.
