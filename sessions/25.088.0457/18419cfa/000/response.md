*   **Perception:** The input grids contain one or more hollow rectangular frames constructed from azure (8) pixels, set against a white (0) background. Inside each azure frame, there is at least one object composed of red (2) pixels. The transformation modifies the content *within* each azure frame, specifically affecting the white pixels located near the red pixels. The azure frames themselves and the areas outside them remain unchanged. The modification appears to be a "fill" operation, converting specific white pixels inside the frame to red, based on the existing red pattern.

*   **Facts:**
    
```yaml
    objects:
      - type: frame
        color: azure (8)
        shape: hollow rectangle
        role: container
      - type: pattern
        color: red (2)
        shape: variable, composed of discrete pixels or connected components
        location: strictly inside an azure frame
      - type: background
        color: white (0)
        location: everywhere else, including inside frames initially
    actions:
      - name: identify_frames
        input: grid
        output: list of azure frame objects (location, boundaries)
      - name: identify_internal_patterns
        input: grid, frame
        output: list of red pattern pixels within the frame
      - name: calculate_bounding_box
        input: list of red pattern pixels
        output: bounding box coordinates (min_row, min_col, max_row, max_col)
      - name: fill_area
        input: grid, frame, bounding_box
        output: modified grid
        details: Changes white (0) pixels to red (2) if they fall within both the calculated bounding box and the inner area of the azure frame.
    relationships:
      - The red patterns are always contained entirely within the hollow space of an azure frame.
      - The transformation targets only the white pixels located inside a frame and within the bounding box defined by the red pattern(s) inside that same frame.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct hollow rectangular frames made of azure (8) pixels in the input grid.
    3.  For each identified azure frame:
        a.  Define the inner area of the frame (the region enclosed by the azure pixels).
        b.  Find all red (2) pixels located within this inner area.
        c.  If no red pixels are found within the frame, proceed to the next frame.
        d.  Determine the minimum bounding box (smallest rectangle) that encloses all the identified red pixels within this frame.
        e.  Iterate through all pixel coordinates within this bounding box.
        f.  For each pixel within the bounding box, check if its location is also within the inner area of the current azure frame and if its current color in the output grid is white (0).
        g.  If both conditions are true, change the color of that pixel in the output grid to red (2).
    4.  Return the final modified output grid.