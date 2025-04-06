*   **Perception of Elements:** The task involves processing 2D grids containing numerical values (0-9). The number 0 appears to represent a background color. Non-zero numbers form distinct, contiguous shapes or objects within the grid. Some shapes are composed of a single non-zero number (uniform shapes), while others are composed of multiple different non-zero numbers (non-uniform shapes). The transformation modifies some shapes based on the pattern of another shape.

*   **YAML Facts:**
    
```yaml
    Grid:
      type: 2D array of integers
      properties:
        dimensions: [10, 10]
        value_range: [0, 9]
        background_color: 0
    Objects:
      - Shape:
          description: A contiguous area of non-zero grid cells.
          properties:
            pixels: list of (row, col) coordinates
            colors: set of unique non-zero integer values within the shape
            is_uniform: boolean (True if len(colors) == 1, False otherwise)
            bounding_box: (min_row, min_col, max_row, max_col)
    Identification:
      - TargetPatternShape:
          criteria: The first non-uniform Shape encountered when scanning the grid (e.g., top-to-bottom, left-to-right).
          properties:
            pattern: Relative arrangement and colors of pixels within its bounding box.
      - ShapesToModify:
          criteria: All Shapes where is_uniform is True and the single color is '5'.
    Action:
      - ReplaceContents:
          source: TargetPatternShape.pattern
          targets: ShapesToModify
          rule: For each ShapeToModify, map the TargetPatternShape.pattern onto the pixels within the ShapeToModify's boundary, preserving the shape's original extent. The color at a relative position (dr, dc) within the TargetPatternShape is placed at the corresponding position within the ShapeToModify.
    Output:
      description: A new grid where the contents of ShapesToModify have been replaced according to the ReplaceContents action. All other grid cells remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous shapes formed by non-zero numbers in the input grid.
    2.  For each shape, determine the set of unique non-zero colors it contains.
    3.  Find the first shape (scanning top-to-bottom, left-to-right) that contains *more than one* distinct non-zero color. Designate this as the "target pattern shape" and record its internal color pattern relative to its top-left corner.
    4.  Identify all shapes that are composed *exclusively* of the number 5.
    5.  Create a copy of the input grid to serve as the output grid.
    6.  For each shape identified in step 4 (composed only of 5s):
        a.  Determine its bounding box or the set of coordinates it occupies.
        b.  Iterate through the coordinates within this shape's boundary.
        c.  For each coordinate (r, c) within the shape, calculate its relative position (dr, dc) from the shape's top-left corner.
        d.  Find the color from the "target pattern shape" at the same relative position (dr, dc).
        e.  Update the output grid at coordinate (r, c) with this color from the target pattern.
    7.  Return the modified output grid.