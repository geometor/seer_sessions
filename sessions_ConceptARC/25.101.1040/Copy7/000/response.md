*   **Perception:** The task involves identifying two primary non-background objects in the input grid. One object contains an internal pattern, specifically a diagonal line of a distinct color. The other object is typically a solid color block. The transformation consists of copying the internal diagonal pattern from the first object ("source") into the second object ("target"), preserving the pattern's color and its relative position within the bounds of the target object. The original objects and the background remain otherwise unchanged.

*   **Facts YAML:**
    
```yaml
    task_type: pattern_transfer
    components:
      - role: background
        properties:
          color: white (0)
      - role: source_object
        properties:
          shape: variable (rectangle, irregular)
          main_color: variable (magenta, yellow in examples)
          contains_pattern: true
          pattern:
            shape: diagonal_line
            color: variable (green, blue in examples)
            orientation: variable (top-left to bottom-right, top-right to bottom-left)
            position: relative to source_object boundaries
      - role: target_object
        properties:
          shape: variable (rectangle)
          main_color: variable (orange, red in examples)
          contains_pattern: false (initially)
      - role: separator (optional)
        properties:
          color: white (0)
          shape: vertical_line (example 1)
    actions:
      - type: identify
        target: source_object
        criteria: non-background object containing an internal pattern (pixels of a different color within its bounds)
      - type: extract
        source: source_object
        details: pattern color, relative coordinates of pattern pixels within source bounds
      - type: identify
        target: target_object
        criteria: non-background object without an internal pattern
      - type: apply_pattern
        target: target_object
        details:
          pattern_color: extracted from source_object
          pattern_coordinates: calculated by adding relative pattern coordinates (from source) to target_object's top-left corner coordinate
    relationships:
      - type: spatial
        between: source_object, target_object
        details: usually spatially separated, relative positions can vary
      - type: pattern_correspondence
        between: source_pattern, target_pattern (created)
        details: relative position and orientation within object bounds are identical
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, contiguous non-background objects in the input grid.
    2.  For each object, determine its bounding box and primary color (most frequent color within the box).
    3.  Locate the "source object": the object containing pixels within its bounding box that are neither the background color nor its own primary color. These differing pixels constitute the "internal pattern".
    4.  Record the color of the internal pattern pixels and their coordinates relative to the top-left corner of the source object's bounding box.
    5.  Locate the "target object": a distinct non-background object that does not contain an internal pattern. Determine its bounding box.
    6.  Initialize the output grid as a copy of the input grid.
    7.  Iterate through the recorded relative coordinates of the source object's internal pattern. For each relative coordinate `(dr, dc)`:
        a.  Calculate the corresponding absolute coordinate `(r, c)` within the output grid by adding the relative coordinate `(dr, dc)` to the top-left coordinate of the target object's bounding box.
        b.  Change the color of the pixel at `(r, c)` in the output grid to the recorded pattern color.
    8.  Return the modified output grid.