*   **Perception:** The input grids contain hollow rectangular or square shapes made of red pixels (2) on a white background (0). Some inputs may contain multiple shapes, and some shapes might be solid (not hollow). The output grids replace the hollow red shapes with green pixels (3) that fill the area previously enclosed by the red shape. Solid red shapes are removed entirely without leaving any green pixels. The background remains white.

*   **YAML Facts:**
    
```yaml
    task_description: "Identify hollow red shapes in the input grid, fill the enclosed area with green in the output grid, and remove all red shapes."
    
    elements:
      - element: "grid"
        description: "A 2D array of pixels representing colors."
        properties:
          - size: Variable height and width (up to 30x30).
          - background_color: white (0)
    
      - element: "shape"
        description: "A contiguous object made of pixels of the same color."
        properties:
          - color: red (2) in input
          - form: Rectangular or square, can be hollow or solid.
    
      - element: "enclosed_area"
        description: "A region of white pixels (0) completely surrounded by red pixels (2)."
        relationship: "Located inside a hollow red shape."
    
      - element: "output_fill"
        description: "A solid shape made of green pixels (3) in the output grid."
        properties:
          - color: green (3)
          - location: Corresponds exactly to the 'enclosed_area' of a hollow red shape from the input.
          - size_and_shape: Identical to the 'enclosed_area'.
    
    transformations:
      - action: "identify_hollow_shapes"
        input: "Input grid with red (2) shapes."
        output: "Coordinates defining the boundaries of hollow red shapes."
        condition: "A shape is hollow if it encloses a region of white (0) pixels."
    
      - action: "find_enclosed_area"
        input: "A hollow red shape boundary and the input grid."
        output: "Coordinates of the white (0) pixels enclosed by the shape."
    
      - action: "fill_enclosed_area"
        input: "Coordinates of an enclosed area."
        output: "Output grid with the corresponding area filled with green (3)."
    
      - action: "remove_red_shapes"
        input: "Input grid with red (2) shapes."
        output: "Output grid with all red (2) pixels removed (replaced with white (0) if not filled with green)."
        condition: "Applies to both hollow and solid red shapes."
    
    relationships:
      - type: "mapping"
        description: "Each hollow red shape in the input maps to a corresponding green filled area in the output."
        from: "hollow red shape"
        to: "green filled area"
      - type: "removal"
        description: "All red shapes (hollow or solid) in the input are absent in the output."
        from: "red shape"
        to: "white background (or green fill)"
    ```


*   **Natural Language Program:**
    1.  Create a new grid (the output grid) with the same dimensions as the input grid, initially filled entirely with white pixels (0).
    2.  Identify all white pixels (0) in the *input* grid that are on the border (top/bottom row, first/last column).
    3.  Starting from these border white pixels, perform a flood fill (or similar connected components search) on the *input* grid, marking all reachable white pixels as "external". Only travel through white pixels during this search.
    4.  Iterate through every pixel (row `r`, column `c`) in the *input* grid.
    5.  If the pixel at (`r`, `c`) in the *input* grid is white (0) and has *not* been marked as "external" during the flood fill, it means this pixel is part of an area enclosed by red pixels.
    6.  Set the corresponding pixel at (`r`, `c`) in the *output* grid to green (3).
    7.  Return the final output grid. (Note: This process implicitly handles the removal of red shapes as the output grid starts white and only enclosed areas are turned green).