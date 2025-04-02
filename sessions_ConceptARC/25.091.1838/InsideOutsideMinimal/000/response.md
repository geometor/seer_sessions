*   **Perception:**
    *   Each input grid contains multiple distinct objects composed of colored pixels on a white background.
    *   One prominent object in each input is a large, hollow rectangle (the "frame"). This frame has a different color in each example (green, red, orange).
    *   Other, smaller objects exist, some located spatially within the boundaries of the frame, and others outside the frame. These smaller objects have a distinct color from the frame (yellow, blue, azure).
    *   Comparing input and output grids reveals that the frame object and any objects located entirely outside the frame remain unchanged.
    *   The key transformation is the removal (replacement with the white background color) of all objects that are entirely contained *within* the hollow space of the frame object.

*   **Facts:**
    
```yaml
    elements:
      - type: grid
        description: Input and output are 2D grids of pixels with colors 0-9.
      - type: background
        color: white (0)
      - type: object
        description: Contiguous block of non-background pixels of the same color.
      - type: frame_object
        description: The largest, hollow, rectangular object in the input grid. Its color varies (green, red, orange). It remains unchanged in the output.
        properties:
          - hollow
          - rectangular
          - largest_contiguous_object
      - type: contained_object
        description: Objects located entirely within the inner boundary defined by the frame_object. Their color differs from the frame_object. These are removed in the output.
        properties:
          - color_different_from_frame
          - location: inside_frame
      - type: external_object
        description: Objects located entirely outside the boundary of the frame_object. Their color differs from the frame_object. These remain unchanged in the output.
        properties:
          - color_different_from_frame
          - location: outside_frame
    relationships:
      - type: spatial_containment
        description: Smaller objects can be either entirely inside or entirely outside the area enclosed by the frame_object.
    actions:
      - type: identify
        target: frame_object
        criteria: Largest contiguous hollow rectangle.
      - type: identify
        target: other_objects
        criteria: All objects that are not the frame_object.
      - type: filter
        target: contained_object
        criteria: Objects entirely within the inner boundaries of the frame_object.
      - type: remove
        target: contained_object
        effect: Pixels of contained_objects are changed to the background color (white, 0).
      - type: preserve
        target: frame_object
        effect: Pixels of the frame_object remain unchanged.
      - type: preserve
        target: external_object
        effect: Pixels of external_objects remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the largest, hollow, rectangular object in the input grid; this is the "frame".
    2.  Identify all other distinct objects in the grid (non-frame, non-background).
    3.  For each of these other objects, determine if all of its constituent pixels lie strictly within the inner boundaries defined by the frame (i.e., not touching the frame itself and located within the rows and columns spanned by the frame's hollow interior).
    4.  Create the output grid by copying the input grid.
    5.  In the output grid, change the color of all pixels belonging to objects identified in step 3 (those entirely inside the frame) to the background color (white, 0).
    6.  Leave the frame object and all objects located outside the frame unchanged.