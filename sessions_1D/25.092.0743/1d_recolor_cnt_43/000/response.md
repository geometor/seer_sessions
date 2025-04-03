*   **Perception of Task Elements:**
    *   The input grids consist of a white background (0) and several distinct objects composed of azure pixels (8).
    *   The output grids maintain the exact same structure (size, background color, object positions and shapes) as the input grids.
    *   The only change between input and output is the color of the azure objects.
    *   The new color of each object in the output depends solely on the number of pixels (size) of the corresponding azure object in the input.
    *   Across all examples, a consistent mapping exists:
        *   Azure objects of size 1 become red (2).
        *   Azure objects of size 2 become blue (1).
        *   Azure objects of size 3 become magenta (6).
    *   Objects are defined as contiguous groups of azure pixels (sharing a side, not just a corner).

*   **YAML Documentation:**
    
```yaml
    task_context:
      grid_properties:
        - background_color: white (0)
        - constant_size_and_shape: true
      input_objects:
        - type: contiguous_pixels
        - color: azure (8)
        - property_measured: size (pixel_count)
      output_objects:
        - type: contiguous_pixels
        - color_determined_by: input_object_size
        - source_color: azure (8)
      transformation:
        - type: object_recoloring
        - based_on: object_size
        - mapping:
            - size: 1
              input_color: azure (8)
              output_color: red (2)
            - size: 2
              input_color: azure (8)
              output_color: blue (1)
            - size: 3
              input_color: azure (8)
              output_color: magenta (6)
        - preserves:
            - object_shape
            - object_position
            - background
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct contiguous objects composed of azure (8) pixels in the input grid. Treat pixels sharing a side (horizontally or vertically) as part of the same object.
    3.  For each identified azure object:
        a.  Count the number of pixels that constitute the object (determine its size).
        b.  Determine the target color based on the object's size using the following rules:
            *   If the size is 1, the target color is red (2).
            *   If the size is 2, the target color is blue (1).
            *   If the size is 3, the target color is magenta (6).
        c.  In the output grid, change the color of all pixels belonging to this object from azure (8) to the determined target color.
    4.  Return the modified output grid.