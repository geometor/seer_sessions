
## train_1

**input:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 1 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 0 0
```

*   **Perception:**
    The input and output are 1D arrays (representing rows of a grid) containing integer values representing colors. Each input contains exactly one contiguous block of a single color (magenta, yellow, or red in the examples, but generally non-white and non-blue) and exactly one 'blue' pixel (value 1). The rest of the pixels are 'white' (value 0). The 'blue' pixel always appears to the right of the colored block. The transformation involves shifting the colored block to the right so that it becomes adjacent to the 'blue' pixel, effectively closing the gap of 'white' pixels that existed between them in the input. The 'blue' pixel itself does not move.

*   **Facts:**
    
```yaml
    task_description: Shift a colored block rightwards to abut a stationary blue marker.

    elements:
      - object: colored_block
        description: A contiguous sequence of pixels with the same color, where the color is not white (0) and not blue (1). There is exactly one such block per input.
        properties:
          - color: The color value (e.g., 6, 4, 2).
          - start_index: The starting position (0-based index) of the block in the input array.
          - end_index: The ending position (0-based index) of the block in the input array.
          - length: The number of pixels in the block (end_index - start_index + 1).
      - object: blue_marker
        description: A single pixel with the color blue (1). There is exactly one such pixel per input.
        properties:
          - index: The position (0-based index) of the blue pixel in the input array.
      - object: white_space
        description: Pixels with the color white (0).
        properties:
          - location: Specifically refers to the white pixels located between the 'colored_block' and the 'blue_marker'.
          - gap_length: The count of white pixels between the end of the 'colored_block' and the 'blue_marker' (blue_marker.index - colored_block.end_index - 1).

    relationships:
      - The 'colored_block' always appears to the left of the 'blue_marker' in the input.
      - There is always at least one 'white_space' pixel between the 'colored_block' and the 'blue_marker' in the input.

    actions:
      - Identify the 'colored_block' (its color, start_index, end_index).
      - Identify the 'blue_marker' (its index).
      - Calculate the 'gap_length' of the 'white_space' between them.
      - Determine the shift amount: shift_amount = gap_length.
      - Create the output array (same size as input, initially all white).
      - Place the 'colored_block' into the output array, shifted right by 'shift_amount'. Its new start index will be (colored_block.start_index + shift_amount).
      - Place the 'blue_marker' into the output array at its original index.
    ```


*   **Natural Language Program:**
    1.  Initialize the output array as a copy of the input array, filled entirely with white (0) pixels.
    2.  Scan the input array to find the contiguous block of non-white, non-blue pixels (the "colored block"). Record its color, start index, and end index.
    3.  Scan the input array to find the index of the blue (1) pixel (the "blue marker").
    4.  Calculate the number of white (0) pixels strictly between the end index of the colored block and the index of the blue marker. This is the shift distance.
    5.  Determine the new start index for the colored block in the output array by adding the shift distance to its original start index.
    6.  Fill the corresponding segment in the output array with the color of the colored block, starting at the new start index and having the same length as the original block.
    7.  Place the blue marker (1) in the output array at its original index.
