*   **Perception:**
    The task involves transforming an input grid containing white (0) and blue (1) pixels into an output grid of the same dimensions. The transformation selectively changes the color of some blue pixels to magenta (6), while leaving white pixels and other blue pixels unchanged. The change appears targeted towards a specific region of blue pixels in each example. Observing the examples, the blue pixels that change to magenta consistently form a solid rectangular block. Comparing this block to other potential rectangular blocks of blue pixels within the input grid suggests a pattern based on size. In each case, the rectangle of blue pixels that changes to magenta is the one with the largest area (height times width) compared to all other possible solid blue rectangles in the input grid.

*   **Facts:**
    ```
yaml
    task_type: color_transformation
    input_colors: [white, blue]
    output_colors: [white, blue, magenta]
    background_color: white (0)
    target_color_input: blue (1)
    target_color_output: magenta (6)
    transformation_scope: subset_of_pixels
    object_focus: solid_rectangles
    object_property: color (must be blue)
    selection_criteria: largest_area (height * width)
    action: recolor_pixels
    unchanged_elements:
      - white pixels
      - blue pixels not part of the largest blue rectangle
    relationships:
      - Identify all maximal contiguous rectangular blocks composed solely of the target_color_input (blue).
      - Compare these blocks based on their area.
      - Select the block with the maximum area.
      - Recolor the pixels within the selected block to the target_color_output (magenta).
    ambiguity_note: The examples do not show cases where multiple blue rectangles share the same maximum area. The assumed behavior is that only one such rectangle exists or the rule applies to all if there's a tie (though recoloring overlapping areas twice with magenta has no effect).
    grid_size_invariant: Yes, the transformation logic does not depend on the grid dimensions, only on the relative shapes within it.
    