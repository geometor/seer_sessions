*   **Perception:**
    The input grids contain multiple distinct, non-overlapping objects composed of single, non-white colors, placed on a white background. Some of these objects form hollow rectangular frames. The transformation identifies these specific hollow rectangular frames and fills their interior (the white pixels enclosed by the frame) with the same color as the frame itself. Objects that are not complete hollow rectangles (e.g., U-shapes, solid shapes, lines, or shapes with internal structures other than just white) are left unchanged. The background remains white.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    objects:
      - type: background
        properties:
          color: white
          value: 0
          role: static_canvas
      - type: shape
        properties:
          color: non-white (blue, red, green, yellow, gray, magenta, orange, azure)
          value: 1-9
          connectivity: contiguous block of same-colored pixels
          form: variable (rectangles, lines, U-shapes, complex patterns)
    relationships:
      - type: spatial
        description: Shapes are placed on the background. Shapes do not overlap.
      - type: containment
        description: Some shapes form closed rectangular frames that enclose an area of white pixels.
    actions:
      - name: identify_hollow_rectangles
        input: shapes
        output: set of shapes that are complete, hollow rectangular frames
        criteria:
          - Closed perimeter of a single non-white color.
          - Rectangular shape.
          - Interior composed entirely of white pixels.
      - name: fill_interior
        input: identified hollow rectangles
        output: modified grid
        process: For each identified rectangle, change the color of all white pixels strictly inside its perimeter to the color of the rectangle's frame.
    transformation_scope: Applies only to pixels inside identified hollow rectangles. Other pixels remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify distinct objects (contiguous blocks of the same non-white color).
    2.  For each identified object:
        a.  Determine if it forms a perfect rectangular frame:
            i.  Check if it has a uniform thickness (likely 1 pixel thick based on examples).
            ii. Check if all pixels forming the object constitute the perimeter of a rectangle.
            iii. Check if all pixels immediately inside this perimeter are white (value 0).
        b.  If the object is confirmed to be a complete, hollow rectangular frame:
            i.  Note the color of the frame.
            ii. Identify the bounding box of the frame.
            iii. Change the color of all white pixels located strictly within this bounding box to the color of the frame.
    3.  Leave all other objects and background pixels unchanged.
    4.  Output the modified grid.