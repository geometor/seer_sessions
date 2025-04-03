**Perception**

1.  **Input/Output Structure:** Both input and output are single-row grids (1D arrays) of the same length.
2.  **Background Preservation:** The white pixels (color 0) remain unchanged in their positions from input to output.
3.  **Target Objects:** The input grids contain contiguous horizontal segments (blocks) of azure pixels (color 8). These are the objects being transformed.
4.  **Transformation:** Each azure block in the input is replaced entirely by a block of a single *different* color in the output. The surrounding white pixels are unaffected.
5.  **Color Mapping Rule:** The color used for replacement depends on the *length* (number of pixels) of the original azure block.
    *   Observing the examples:
        *   `train_1`: Length 5 -> red (2), Length 4 -> maroon (9), Length 4 -> maroon (9)
        *   `train_2`: Length 2 -> maroon (9), Length 3 -> red (2), Length 4 -> maroon (9), Length 3 -> red (2)
        *   `train_3`: Length 3 -> red (2), Length 6 -> maroon (9), Length 5 -> red (2)
    *   Synthesizing: Blocks with an *odd* length (3, 5) are replaced with red (2). Blocks with an *even* length (2, 4, 6) are replaced with maroon (9).

**Facts**


```yaml
task_type: object_transformation
grid_dimensionality: 1D
background_color: 0  # white
objects:
  - type: contiguous_horizontal_segment
    input_color: 8  # azure
    properties:
      - length: integer # number of pixels in the segment
actions:
  - name: conditional_color_replacement
    input_object: azure_segment
    output_object: segment_of_same_length_and_position
    condition: based_on_length_parity
    rules:
      - if: length is odd
        output_color: 2 # red
      - if: length is even
        output_color: 9 # maroon
preservation:
  - background_pixels (color 0) remain unchanged
```


**Natural Language Program**

1.  Identify all contiguous horizontal segments (blocks) of azure pixels (color 8) in the input grid.
2.  For each identified azure block:
    a.  Determine its length (number of pixels).
    b.  Check if the length is odd or even.
    c.  If the length is odd, replace all pixels in that block with red (color 2) in the output grid.
    d.  If the length is even, replace all pixels in that block with maroon (color 9) in the output grid.
3.  Keep all other pixels (white, color 0) in their original positions in the output grid.