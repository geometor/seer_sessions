*   **Perception:**
    *   Each input grid contains two distinct non-white colored objects against a white background.
    *   One object appears somewhat "inside" or "central" relative to the other object.
    *   The transformation involves removing the "inner" object and modifying the "outer" object.
    *   The outer object seems to expand horizontally to fill the space left by the inner object, but only within the rows where the outer object was originally present.
    *   The final shape in the output grid consists only of the expanded outer object color against the white background.

*   **YAML Facts:**
    
```yaml
    task_description: Replace an inner colored shape with the color of an outer shape, expanding the outer shape horizontally within its original rows to fill the combined horizontal span.
    
    elements:
      - role: background
        color: white (0)
        description: The default color of the grid.
      - role: inner_object
        color: varies (red, yellow, magenta in examples)
        description: A contiguous object of a single color, relatively central.
        properties:
          - removed_in_output: true
      - role: outer_object
        color: varies (blue, green, orange in examples)
        description: An object of a single color, partially surrounding the inner_object.
        properties:
          - persists_in_output: true
          - expands_horizontally: true
          - expansion_limited_to_original_rows: true
    
    relationships:
      - type: spatial
        description: The outer_object partially surrounds or is adjacent to the inner_object.
      - type: transformation
        description: The inner_object is effectively replaced by white, while the outer_object expands horizontally into the space previously occupied by the inner_object, but only on rows where the outer_object existed. The expansion fills the horizontal extent defined by the combined original footprint of both objects within those specific rows.
    
    grid_properties:
      - size: 8x8 for all examples.
      - background_color: Always white (0).
    
    color_mapping:
      - input_inner: red(2), output_fills_with: blue(1)
      - input_inner: yellow(4), output_fills_with: green(3)
      - input_inner: magenta(6), output_fills_with: orange(7)
      - output_color: Is always the color of the input's outer_object.
    ```


*   **Natural Language Program:**
    1.  Identify the two non-background colors in the input grid. Let the color of the object that is more centrally located or enclosed be `inner_color`, and the color of the object partially surrounding it be `outer_color`. The background color is white (0).
    2.  Determine the overall horizontal span (minimum and maximum column index) occupied by *either* the `inner_color` or `outer_color` pixels across the entire grid.
    3.  Initialize the output grid with the background color (white).
    4.  Iterate through each row of the input grid.
    5.  For the current row, check if it contains any pixels of `outer_color`.
    6.  If the row contains `outer_color` pixels, fill the corresponding row in the output grid with `outer_color` from the minimum to the maximum column index determined in step 2.
    7.  If the row does *not* contain any `outer_color` pixels, leave the corresponding row in the output grid filled with the background color (white).