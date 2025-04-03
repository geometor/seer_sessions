*   **Perception:** The task involves processing a single-row grid containing a background color (white, 0) and a foreground color (green, azure, or gray in the examples). The input grid features one large contiguous horizontal block of the foreground color and several isolated pixels or very small blocks of the same foreground color scattered around. The transformation isolates the largest contiguous block of the foreground color, removing all other instances of that color by changing them to the background color.

*   **YAML Facts:**
    
```yaml
    task_type: filtering
    grid_dimensionality: 1D (single row)
    background_color: white (0)
    foreground_colors: variable (green, azure, gray observed)
    objects:
      - type: contiguous_horizontal_block
        color: non-white
        properties:
          - size (length)
          - position
    input_features:
      - Multiple blocks of the foreground color.
      - One block is significantly larger than the others.
      - Smaller blocks are often single pixels.
    output_features:
      - Only the largest block from the input is retained.
      - All other foreground pixels are changed to the background color.
    transformation: object_selection based on size
    selection_criteria: largest_block
    action: keep_largest_block, remove_others
    ```


*   **Natural Language Program:**
    1.  Scan the input row to identify all contiguous horizontal segments (blocks) of non-white pixels. Record the start index, end index, and color of each block.
    2.  Calculate the length (size) of each identified block.
    3.  Determine the block with the maximum length.
    4.  Create a new output row of the same length as the input, initially filled with the background color (white, 0).
    5.  Copy the pixels corresponding to the largest block (identified in step 3) from the input row to the output row at the same positions.
    6.  Return the modified output row.