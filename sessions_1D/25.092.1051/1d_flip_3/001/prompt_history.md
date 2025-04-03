
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 4 4 4 4 4 4 4 4 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 3 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 7 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 1 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 1 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are 1D arrays (or single rows of a grid) of integers representing colors.
    *   Each array primarily consists of white (0) pixels.
    *   Within the white background, there is a single contiguous block of non-white pixels.
    *   This non-white block is composed of two distinct colors: one color appears only once (let's call it the "marker" color), and the other color fills the rest of the block (the "body" color).
    *   In all examples, the marker pixel is located at the leftmost position of the non-white block in the input.
    *   The transformation involves moving the marker pixel to the rightmost position of the non-white block in the output, while the body pixels shift accordingly to fill the space.
    *   The colors themselves, the length of the non-white block, and the position of the block within the overall array remain unchanged.

*   **YAML Facts:**
    
```yaml
    task: Move a unique 'marker' pixel from one end of a colored block to the other.
    elements:
      - type: background
        color: white (0)
        description: Fills the array outside the main object. Remains unchanged.
      - type: colored_block
        description: A contiguous sequence of non-white pixels.
        properties:
          - composition: Contains two distinct colors.
          - structure: One 'marker' pixel and multiple 'body' pixels.
          - invariant: Total length and constituent colors remain the same. Position within the array remains the same.
      - type: marker_pixel
        description: The single pixel within the colored_block with a unique color.
        properties:
          - color: variable (green, orange, blue in examples)
          - initial_position: Leftmost end of the colored_block in the input.
          - final_position: Rightmost end of the colored_block in the output.
      - type: body_pixels
        description: The pixels within the colored_block that share the same color, distinct from the marker.
        properties:
          - color: variable (yellow, gray, yellow in examples)
          - quantity: Fills the rest of the colored_block.
          - relative_position: Shifts to accommodate the marker's movement but maintain contiguity.
    transformation:
      action: Relocate the marker_pixel within the colored_block.
      details: Move the marker_pixel from the leftmost position to the rightmost position of the block.
      constraints: Preserve the colors, length, and overall position of the colored_block.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sequence of non-white pixels (the "colored block") in the input array.
    2.  Within this colored block, distinguish the single "marker" pixel (which has a unique color within the block) from the "body" pixels (which all share a different, single color).
    3.  Determine the current position of the marker pixel within the block (it will be at one end - in the examples, the left end).
    4.  Create the output array by keeping all background (white) pixels the same.
    5.  Reconstruct the colored block in the output by placing the marker pixel at the opposite end of the block from where it was found in the input (e.g., if it was at the left end, move it to the right end).
    6.  Fill the remaining positions of the block with the body pixels, maintaining their color and count.
