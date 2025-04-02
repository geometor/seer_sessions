*   **Perception:** The task involves transforming a single, primary colored object within a white background grid. The transformation depends on the initial state of the object: if it's hollow (an outline with a white interior), it gets filled; if it's solid, it gets hollowed out (only the perimeter remains). The color of the object and the background pixels outside the object's bounding box remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: object_transformation
    objects:
      - role: primary_object
        count: 1
        properties:
          - color: non-white (e.g., green, red)
          - connectivity: connected_component
          - state: either 'hollow' or 'solid'
            definition:
              hollow: contains background_color pixels fully enclosed by object_color pixels (orthogonal adjacency).
              solid: does not contain enclosed background_color pixels.
          - bounding_box: defines the spatial extent.
      - role: background
        properties:
          - color: white (0)
    transformation:
      type: conditional_state_toggle
      input_state: primary_object.state
      output_state: opposite of input_state (hollow -> solid, solid -> hollow)
      details:
        - condition: input_state is 'hollow'
          action: fill_interior
          parameters:
            fill_color: primary_object.color
            target_pixels: enclosed background_color pixels within bounding_box
        - condition: input_state is 'solid'
          action: hollow_object
          parameters:
            keep_color: primary_object.color
            change_color: background.color (white)
            target_pixels: interior object_color pixels (not adjacent orthogonally to background pixels outside the object)
            keep_pixels: perimeter object_color pixels (adjacent orthogonally to background pixels outside the object)
    constraints:
      - The bounding box of the primary object remains the same.
      - The color of the primary object's pixels (in its final state) remains the same as its initial color.
      - Background pixels outside the bounding box are unchanged.

    ```


*   **Natural Language Program:**
    1.  Identify the single connected non-white object in the input grid. Note its color (C) and determine its bounding box.
    2.  Determine if the object is 'hollow' or 'solid':
        *   Check if there are any white pixels within the object's bounding box that are completely surrounded (only have orthogonal neighbors of color C). If yes, the object is 'hollow'.
        *   Otherwise, the object is 'solid'.
    3.  If the object is 'hollow': Create the output grid by copying the input grid and changing all the enclosed white pixels (identified in step 2) within the bounding box to color C.
    4.  If the object is 'solid': Create the output grid by copying the input grid. Then, identify all pixels of color C that are *not* on the perimeter. Change these interior pixels to white (0). A pixel is on the perimeter if it has at least one orthogonal neighbor that is a white pixel lying outside the connected component of the object. Keep the perimeter pixels with color C.