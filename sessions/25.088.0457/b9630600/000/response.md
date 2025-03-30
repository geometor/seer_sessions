*   **Perception**: The input and output grids are 30x30. The primary color used besides the white background (0) is green (3). The input grids contain multiple hollow rectangular or square shapes constructed from green pixels. The output grids show the same shapes, but the hollow interiors (originally white) have been filled with the same green color as the outlines. The outlines themselves remain unchanged. The transformation seems to be a "fill" operation applied to enclosed regions defined by green boundaries.

*   **Facts**:
    
```yaml
    grid_properties:
      size: 30x30
      background_color: 0 # white
    
    objects:
      - type: closed_shape # specifically hollow rectangles/squares in examples
        color: 3 # green
        properties:
          - forms a boundary enclosing a region of background_color pixels
    
    actions:
      - name: fill_interior
        target_objects: objects identified as closed_shape
        target_pixels: background_color pixels enclosed by the target_object's boundary
        fill_color: the color of the target_object's boundary (3, green)
    
    relationships:
      - type: spatial
        description: The transformation focuses on identifying enclosed regions (interiors) within shapes.
      - type: color
        description: The fill color is determined by the color of the enclosing shape.
    ```


*   **Natural Language Program**:
    1.  Identify all distinct, contiguous green shapes (color 3) in the input grid.
    2.  For each green shape, determine if it forms a closed boundary enclosing a region of white pixels (color 0).
    3.  Locate all white pixels that are inside the enclosed region of each identified closed boundary shape. A pixel is considered "inside" if it is white and cannot reach the edge of the grid by moving horizontally or vertically through only white pixels without crossing the green boundary of the shape.
    4.  Create the output grid by copying the input grid.
    5.  Modify the output grid by changing the color of all identified interior white pixels to green (color 3).