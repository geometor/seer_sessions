
## train_1

**input:**
```
0 2 2 2 0 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 0 2 2 2 0 0 0 2 2 2 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 9 9 9 0 0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 9 9 9 0 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of task elements:**
    *   The input and output are 1D arrays or single-row grids of pixels.
    *   The primary elements are horizontal sequences (contiguous blocks) of identical non-white pixels, separated by white pixels (0).
    *   Each example contains at least one sequence longer than one pixel and one or more sequences of exactly one pixel.
    *   The transformation involves identifying a "pattern" sequence (the first encountered sequence longer than one pixel) and replacing single-pixel sequences of the *same color* with a copy of this pattern sequence.
    *   The replacement starts at the position of the single pixel and extends to the right, overwriting any existing pixels in that range.
    *   Pixels not part of a single-pixel sequence being replaced are copied directly from the input to the output.

*   **YAML Facts:**
    
```yaml
    task_type: pattern_replacement
    grid_dimensionality: 1D (or single row 2D)
    objects:
      - type: sequence
        description: Contiguous horizontal block of identical non-white pixels.
        properties:
          - color: The color (1-9) of the pixels in the sequence.
          - length: The number of pixels in the sequence.
          - position: The starting index (column) of the sequence.
    pattern_object:
      description: The first identified sequence with length > 1.
      identified_by: Scanning left-to-right.
      properties:
        - pattern_color: The color of the pattern object.
        - pattern_length: The length of the pattern object.
    target_objects:
      description: Sequences with length = 1.
      identified_by: Scanning the entire input.
    action:
      type: replace
      condition: A target object's color matches the pattern_color.
      mechanism: Replace the target object (single pixel) with a sequence identical to the pattern object (same color, same length), starting at the target object's position and extending rightwards.
    background:
      color: white (0)
      behavior: Generally preserved, unless overwritten by a replacement action.
    output_generation:
      - Initialize output as a copy of the input.
      - Identify the pattern object (color C, length L).
      - Iterate through the input grid.
      - If a single pixel of color C is found at index i:
          - Replace pixels in the output grid from index i to i + L - 1 with color C.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the initial output grid.
    2.  Scan the input grid from left to right to find the first contiguous horizontal sequence of identical non-white pixels with a length greater than 1. Store the color (C) and length (L) of this sequence as the "pattern". If no such sequence exists, the output is identical to the input.
    3.  Iterate through each pixel position (index `i`) in the input grid.
    4.  Check if the pixel at index `i` in the input grid meets the following criteria:
        *   It is a non-white pixel.
        *   Its color matches the pattern color C.
        *   It forms a sequence of length 1 (i.e., the pixel to its left, if it exists, is different, and the pixel to its right, if it exists, is different or the grid ends).
    5.  If all criteria are met, modify the output grid by placing the pattern sequence (color C, length L) starting at index `i` and extending to index `i + L - 1`. These pixels in the output grid are set to color C, overwriting their previous values.
    6.  After checking all pixel positions, the modified output grid is the final result.
