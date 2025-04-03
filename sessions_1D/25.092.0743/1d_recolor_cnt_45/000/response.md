*   **Perception:** The input consists of a one-dimensional array containing primarily white pixels (0) and some azure pixels (8). The azure pixels form contiguous segments of varying lengths (1, 2, or 3 pixels). The output preserves the white pixels but replaces the azure segments with segments of the same length but different colors. The replacement color depends solely on the length of the original azure segment.

*   **YAML Facts:**
    
```yaml
    task_description: Replace contiguous segments of a specific color (azure) with segments of the same size but a different color, determined by the segment's length.
    input_features:
      - grid_representation: 1D array
      - background_color: white (0)
      - object_color: azure (8)
      - object_definition: Contiguous horizontal segments of azure pixels.
    output_features:
      - grid_representation: 1D array (same dimensions as input)
      - background_color_preservation: white (0) pixels remain unchanged.
      - segment_transformation:
          rule: The color of the output segment depends on the length of the corresponding input azure segment.
          mapping:
            - input_segment_length: 1
              output_color: orange (7)
            - input_segment_length: 2
              output_color: green (3)
            - input_segment_length: 3
              output_color: red (2)
          segment_size_preservation: The length of the output segment is the same as the input segment.
    relationships:
      - The transformation is local to the identified azure segments.
      - The mapping between segment length and output color is consistent across examples.
    ```


*   **Natural Language Program:**
    1.  Iterate through the input array from left to right.
    2.  Identify contiguous segments of azure (8) pixels. Keep track of the start index and length of each segment.
    3.  For each identified azure segment:
        a.  Determine the length of the segment.
        b.  Select the replacement color based on the length:
            *   If the length is 1, use orange (7).
            *   If the length is 2, use green (3).
            *   If the length is 3, use red (2).
        c.  Replace the pixels corresponding to the identified segment in the input array (or a copy) with the selected replacement color.
    4.  Pixels that were originally white (0) remain white (0).
    5.  The resulting array is the output.