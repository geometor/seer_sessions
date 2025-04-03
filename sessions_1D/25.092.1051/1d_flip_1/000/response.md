*   **Perception:**
    *   The input and output are both 1x10 grids (or lists) of colored pixels.
    *   Each example contains a contiguous segment of non-white pixels, surrounded by white pixels (color 0). The white pixels remain unchanged in their positions.
    *   Within the non-white segment, there is always one pixel of a unique color (let's call it the "singleton") and a contiguous block of pixels of another color (let's call it the "block").
    *   The singleton and the block are always adjacent to each other.
    *   The transformation involves swapping the positions of the singleton and the block within the non-white segment. The singleton moves to the opposite end of the combined region initially occupied by both objects, and the block shifts to fill the remaining space, starting where the singleton was.

*   **YAML Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensions:
      input: 1x10
      output: 1x10
    background_color: 0 (white)
    objects:
      - name: singleton
        description: A single pixel of a non-white color within the active segment.
        properties:
          color: varies (magenta, blue, orange in examples)
          size: 1 pixel
      - name: block
        description: A contiguous block of pixels of a single non-white color, different from the singleton's color.
        properties:
          color: varies (blue, azure, red in examples)
          size: variable (3, 4, 4 pixels in examples)
      - name: background
        description: Pixels outside the active segment.
        properties:
          color: 0 (white)
          size: variable
    relationships:
      - type: adjacency
        objects: [singleton, block]
        description: The singleton and the block are directly next to each other horizontally.
      - type: containment
        objects: [singleton, block]
        container: active_segment (the contiguous non-white part of the grid)
    actions:
      - name: swap_positions
        objects: [singleton, block]
        description: The relative positions of the singleton and the block within the active segment are swapped. If the singleton is on the left, it moves to the right end of the combined area, and the block shifts left. If the singleton is on the right, it moves to the left end, and the block shifts right.
      - name: preserve_position
        objects: [background]
        description: Background pixels remain in their original positions.

    ```


*   **Natural Language Program:**
    1.  Identify the contiguous segment of the input grid containing non-white pixels (colors other than 0). Note the start and end indices of this segment.
    2.  Within this segment, identify two distinct non-white objects:
        a.  A single pixel (the "singleton").
        b.  A contiguous block of pixels of another color (the "block").
    3.  Determine the relative positions of the singleton and the block (which one is to the left/right).
    4.  Create the output grid by first copying the input grid.
    5.  Modify the output grid within the identified segment's boundaries:
        a.  If the singleton was originally to the left of the block, place the block starting at the original singleton's position and place the singleton immediately after the block.
        b.  If the singleton was originally to the right of the block, place the singleton at the original start position of the block, and place the block immediately after the singleton.
    6.  Pixels outside the identified non-white segment remain unchanged.