*   **Perception of the Elements:**
    *   The input and output are 10x10 grids containing integer values.
    *   The integer 0 represents the background color.
    *   Each input grid contains a single contiguous shape composed of a non-zero integer (color). The color itself varies between examples (5 in train\_1, 7 in train\_2).
    *   The transformation involves moving (translating) the entire shape within the grid. The shape's structure and color remain identical.
    *   The direction of translation appears to depend on the shape's geometry. In train\_1, the shape is shifted horizontally to the right. In train\_2, the shape is shifted vertically downwards.
    *   The magnitude of the shift is 3 units in both examples, either horizontally or vertically.

*   **Facts:**
    
```yaml
    objects:
      - name: grid
        properties:
          - type: 2D array
          - size: 10x10
          - background_color: 0
      - name: shape
        properties:
          - composed_of: non-zero pixels (color)
          - contiguous: true
          - color: integer (e.g., 5, 7)
          - structure: collection of pixel coordinates
          - max_vertical_segment_length: integer
          - max_horizontal_segment_length: integer
    actions:
      - name: translate_shape
        parameters:
          - shape: the identified shape object
          - direction: horizontal (right) or vertical (down)
          - magnitude: 3 units
    relationships:
      - type: determines_direction
        subject: shape.max_horizontal_segment_length
        comparison: greater_than_or_equal_to
        object: shape.max_vertical_segment_length
        result: translate_shape.direction = horizontal (right)
      - type: determines_direction
        subject: shape.max_vertical_segment_length
        comparison: greater_than
        object: shape.max_horizontal_segment_length
        result: translate_shape.direction = vertical (down)
      - type: sets_magnitude
        value: 3
        result: translate_shape.magnitude = 3
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-zero pixels in the input grid; this is the 'shape'. Note its color.
    2.  Calculate the maximum length of any continuous vertical line segment within the shape.
    3.  Calculate the maximum length of any continuous horizontal line segment within the shape.
    4.  Compare the maximum horizontal length and the maximum vertical length:
        a.  If the maximum horizontal length is greater than or equal to the maximum vertical length, determine the translation direction as 'horizontal-right'.
        b.  Otherwise (if the maximum vertical length is greater), determine the translation direction as 'vertical-down'.
    5.  Set the translation magnitude to 3 units.
    6.  Create a new 10x10 output grid initialized with the background color (0).
    7.  For each pixel belonging to the original shape in the input grid, calculate its new position by adding the translation vector (either (0, 3) for horizontal-right or (3, 0) for vertical-down) to its original coordinates.
    8.  Place the shape's original color at these new coordinates in the output grid.