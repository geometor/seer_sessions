*   **Perception of Elements:**
    *   The task operates on 1-dimensional grids (single rows).
    *   Each input contains a contiguous sequence of non-white pixels, potentially flanked by white pixels (0).
    *   Within this non-white sequence, there are exactly two distinct colors present.
    *   One color appears as a single pixel (the "singleton").
    *   The other color appears as a contiguous sequence of multiple pixels (the "sequence").
    *   The singleton pixel is always located at one end of the non-white sequence, adjacent to the start or end of the multi-pixel sequence.
    *   The transformation modifies only the non-white sequence. The surrounding white pixels remain unchanged.
    *   The transformation moves the singleton pixel to the opposite end of the multi-pixel sequence.

*   **YAML Facts:**
    
```yaml
    task_type: array_manipulation_1d
    grid_dimensionality: 1
    background_color: white (0)
    objects:
      - name: non_white_block
        description: A contiguous sequence of non-white pixels.
        properties:
          colors: Contains exactly two distinct non-white colors.
          location: Can be anywhere within the row, possibly touching the edges.
      - name: singleton_pixel
        description: A single pixel within the non_white_block whose color appears only once in the block.
        properties:
          color: Any non-white color.
          count: 1 within the non_white_block.
          location: Always at one of the two ends of the non_white_block.
      - name: sequence_pixels
        description: A contiguous sequence of pixels within the non_white_block, all having the same color, which is different from the singleton_pixel's color.
        properties:
          color: Any non-white color, different from singleton_pixel color.
          count: > 1 within the non_white_block.
          location: Forms the rest of the non_white_block adjacent to the singleton_pixel.
    relationships:
      - type: adjacency
        object1: singleton_pixel
        object2: sequence_pixels
        details: The singleton_pixel is directly adjacent to one end of the sequence_pixels.
    action:
      - type: move
        object: singleton_pixel
        details: The singleton_pixel is moved from its original end of the non_white_block to the opposite end. The relative order of the sequence_pixels remains unchanged.
    invariants:
      - The background white pixels remain unchanged.
      - The colors and number of pixels within the non_white_block remain the same, only their order changes.
      - The length of the grid remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels within the input row. If no such block exists or the block contains fewer than two pixels or more than two distinct colors, return the input unchanged (though this case is not shown in examples).
    2.  Within this non-white block, identify the color that appears only once (the singleton color) and the color that appears multiple times (the sequence color). Determine the single pixel with the singleton color and the sequence of pixels with the sequence color.
    3.  Determine the position of the singleton pixel relative to the sequence pixels (i.e., is it at the start or the end of the combined non-white block?).
    4.  Construct the new non-white block by placing the sequence of pixels first, followed by the singleton pixel, if the singleton was originally at the start.
    5.  Construct the new non-white block by placing the singleton pixel first, followed by the sequence of pixels, if the singleton was originally at the end. (This case doesn't appear in the examples but follows the observed "move to other end" logic).
    6.  Reconstruct the output row by replacing the original non-white block with the newly constructed block, keeping all surrounding white pixels in their original positions.