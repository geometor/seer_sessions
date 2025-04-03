*   **Perception**: The input grids are single rows containing primarily white pixels (0). Within each row, there are two distinct non-white colors. One color appears as a single pixel (the "singleton"), and the other color forms a contiguous horizontal block (the "block"). The singleton pixel is always adjacent to one end of the block. The transformation swaps the position of the singleton pixel and the entire block. The internal arrangement of pixels within the block remains unchanged, and the surrounding white pixels are unaffected.

*   **YAML Facts**:
    
```yaml
    task_description: Swap the positions of a single non-white pixel and an adjacent contiguous block of another non-white color within a single row grid.
    grid_properties:
      - shape: Single row (1xN)
      - background_color: white (0)
    objects:
      - name: singleton
        description: A single pixel of a non-white color.
        properties:
          - count: 1
          - color: Varies (azure, magenta, orange in examples)
          - relation_to_block: Adjacent to one end
      - name: block
        description: A contiguous horizontal sequence of pixels of the same non-white color.
        properties:
          - count: >1
          - color: Varies (green, azure in examples), distinct from the singleton color.
          - shape: Horizontal line segment
      - name: background
        description: White pixels surrounding the singleton and the block.
        properties:
          - color: white (0)
          - location: Fills the rest of the row.
    actions:
      - name: identify_objects
        description: Locate the singleton pixel and the contiguous block based on their colors and counts within the row.
      - name: swap_positions
        description: Exchange the position occupied by the singleton pixel with the sequence of positions occupied by the block.
        constraints:
          - Preserve the internal order of pixels within the block.
          - Do not alter the background pixels.
    relationships:
      - type: adjacency
        object1: singleton
        object2: block
        details: The singleton pixel is immediately to the left or right of the block.
    ```


*   **Natural Language Program**:
    1.  Identify all non-white pixels in the input row.
    2.  Determine the two distinct non-white colors present.
    3.  Count the occurrences of each non-white color. Identify the color that appears exactly once; this is the color of the "singleton" pixel. The other non-white color belongs to the "block".
    4.  Find the index (position) of the singleton pixel.
    5.  Find the start and end indices of the contiguous block of the other non-white color.
    6.  Create a new output row, initially identical to the input row.
    7.  Determine the starting index for the swapped placement. If the singleton was originally to the left of the block, the block's new starting index is the original singleton index. If the singleton was to the right, the block's new starting index is the original block's starting index.
    8.  Place the pixels corresponding to the block into the output row starting at the calculated new index.
    9.  Place the singleton pixel into the output row at the position immediately following the newly placed block (if the singleton was originally left) or immediately preceding it (if the singleton was originally right). Specifically, its new index will be the original end index of the block (if singleton was left) or the original start index of the block (if singleton was right).