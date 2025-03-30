*   **Perception:** The task involves identifying closed shapes formed by red (2) pixels within the input grid. These shapes resemble either a digit '5' or a letter 'H'. The transformation consists of filling the area enclosed by these red shapes with a specific color, while leaving the red outline and the exterior background (white - 0) unchanged. The fill color depends on the type of shape ('5' or 'H') and whether the shape contains an internal red pixel in the input grid. Multiple shapes can exist within a single grid, and each is processed independently.

*   **YAML Facts:**
    
```yaml
    elements:
      - object: grid
        description: A 2D array of pixels with colors 0-9.
      - object: shape
        description: A closed loop formed by contiguous red (2) pixels.
        properties:
          - boundary_color: red (2)
          - interior_pixels: pixels enclosed by the boundary. Initially white (0), but may contain isolated red (2) pixels.
          - shape_type: Identifiable as resembling '5' or 'H'.
          - has_internal_red: Boolean indicating if any red (2) pixel exists within the enclosed area in the input.
      - object: background
        description: Pixels outside any red shape, typically white (0). Remains unchanged.
    actions:
      - action: identify_shapes
        description: Locate all closed loops of red (2) pixels in the input grid.
      - action: determine_shape_type
        description: Classify each identified shape as either '5' or 'H'.
      - action: check_internal_red
        description: For each shape, determine if its enclosed area contains any red (2) pixels in the input.
      - action: fill_interior
        description: Change the color of the white (0) pixels inside each shape based on specific rules.
    rules:
      - rule: fill_color_determination
        conditions:
          - Shape type is '5'.
        result: Fill interior white (0) pixels with azure (8), regardless of internal red pixels.
      - rule: fill_color_determination
        conditions:
          - Shape type is 'H'.
          - Shape has internal red (2) pixel(s) in the input.
        result: Fill interior white (0) pixels with yellow (4).
      - rule: fill_color_determination
        conditions:
          - Shape type is 'H'.
          - Shape does not have internal red (2) pixel(s) in the input.
        result: Fill interior white (0) pixels with green (3).
      - rule: preservation
        description: Red (2) boundary pixels and background (0) pixels remain unchanged in the output. Any internal red (2) pixels within a shape also remain unchanged. Only interior white (0) pixels are modified.

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through the input grid to find connected components (objects) made of red (2) pixels that form closed loops (shapes).
    3.  For each identified red shape:
        a.  Determine the set of pixels enclosed by the shape's boundary.
        b.  Analyze the pattern of the red boundary pixels to classify the shape type as either '5' or 'H'.
        c.  Check if any pixel within the enclosed area *in the input grid* is red (2). Note this as `has_internal_red`.
        d.  Determine the fill color based on the shape type and `has_internal_red`:
            i.  If the shape type is '5', the fill color is azure (8).
            ii. If the shape type is 'H' and `has_internal_red` is true, the fill color is yellow (4).
            iii. If the shape type is 'H' and `has_internal_red` is false, the fill color is green (3).
        e.  Iterate through all pixels within the enclosed area of the current shape *in the output grid*. If a pixel's color is white (0), change it to the determined fill color. Leave existing red (2) pixels within the interior unchanged.
    4.  Return the modified output grid.