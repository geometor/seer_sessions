*   **Perception**: The task operates on a single row of pixels. The input contains segments of yellow pixels (4) separated by white pixels (0). The output modifies the input by changing the color of one specific yellow segment to magenta (6), while leaving other yellow segments and white pixels unchanged. The segment that changes color appears to be the longest continuous segment of yellow pixels in the input row.

*   **Facts**:
    
```yaml
    task_type: object_color_change
    grid_properties:
      dimensionality: 1D (represented as 1xN grid)
      size_constraints: Fixed size between input and output.
      colors_involved:
        - white (0)
        - yellow (4)
        - magenta (6)
    objects:
      definition: Contiguous horizontal segments of non-white pixels.
      input_objects:
        - type: segment
          color: yellow (4)
          properties: [length]
      output_objects:
        - type: segment
          color: yellow (4) or magenta (6)
          properties: [length]
    relationships:
      - type: comparison
        property: length
        between: yellow segments
        criterion: maximum
    actions:
      - type: conditional_color_change
        target: The single longest segment of yellow pixels.
        condition: Must be the unique longest segment.
        from_color: yellow (4)
        to_color: magenta (6)
        unchanged_elements: All other pixels (white pixels, shorter yellow segments).
    ```


*   **Natural Language Program**:
    1.  Scan the input grid row to identify all contiguous horizontal segments composed solely of yellow (4) pixels.
    2.  Calculate the length of each identified yellow segment.
    3.  Determine the maximum length found among all yellow segments.
    4.  Identify the yellow segment(s) possessing this maximum length.
    5.  If there is exactly one segment with the maximum length, change the color of every pixel within that specific segment from yellow (4) to magenta (6).
    6.  If there is no longest segment (e.g., no yellow pixels) or multiple segments share the same maximum length, make no changes to the grid.
    7.  All pixels not part of the uniquely longest yellow segment retain their original color.
    8.  Output the resulting grid.