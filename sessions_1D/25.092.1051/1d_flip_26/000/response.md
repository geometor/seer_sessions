*   **Perception**: The input and output are single rows of pixels. Each input row contains a sequence of non-background pixels consisting of a single pixel of one color (let's call it the 'marker') immediately followed by a contiguous block of pixels of another color (let's call it the 'block'). The background is white (0). The transformation involves moving the marker pixel from the position *before* the block to the position immediately *after* the block. The pixels within the block shift one position to the left to fill the gap left by the marker.

*   **YAML Facts**:
    
```yaml
    task_description: Move a single 'marker' pixel across an adjacent 'block' of pixels in a 1D grid.

    elements:
      - object: marker_pixel
        description: A single pixel with a color different from the background (white) and the adjacent block.
        properties:
          - color: unique_color_1 (e.g., magenta in ex1, yellow in ex2, blue in ex3)
          - position: index `i`
      - object: pixel_block
        description: A contiguous sequence of one or more pixels, all having the same color, different from the background and the marker pixel.
        properties:
          - color: unique_color_2 (e.g., red in ex1, gray in ex2, yellow in ex3)
          - position: starts at index `i+1`
          - length: `L` (number of pixels in the block)
      - object: background
        description: Pixels representing the empty space.
        properties:
          - color: white (0)

    relationships:
      - type: adjacency
        objects: [marker_pixel, pixel_block]
        details: The marker_pixel is immediately to the left of the first pixel of the pixel_block.

    actions:
      - action: move
        object: marker_pixel
        from_position: index `i`
        to_position: index `i + L` (immediately after the original block)
      - action: shift
        object: pixel_block
        direction: left
        distance: 1 position (occupying indices `i` to `i + L - 1`)
    ```


*   **Natural Language Program**:
    1.  Identify the sequence of non-background pixels in the input row.
    2.  Find the first pixel in this sequence (the 'marker pixel').
    3.  Identify the contiguous block of pixels of a single, different color that immediately follows the marker pixel (the 'pixel block'). Let the length of this block be `L`.
    4.  Create the output row by copying the input row.
    5.  Move the marker pixel from its original position (`i`) to the position immediately following the end of the pixel block (position `i + L`).
    6.  Shift all pixels of the pixel block one position to the left, so they now occupy the original position of the marker pixel and the subsequent `L-1` positions (positions `i` through `i + L - 1`).
    7.  Leave all other pixels (background) unchanged.