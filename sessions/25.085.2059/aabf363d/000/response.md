*   **Perception of the elements:**
    *   Each input grid contains two distinct non-white elements against a white background.
    *   One element is a larger, contiguous shape composed of multiple pixels of the same color (green in train\_1, red in train\_2).
    *   The second element is a single pixel of a different color, located at the bottom-left corner (magenta in train\_1, yellow in train\_2).
    *   In the output grid, the larger shape from the input has been recolored to match the color of the single pixel from the input.
    *   The original location of the single pixel in the input grid becomes white in the output grid.
    *   The overall structure and position of the larger shape remain unchanged, only its color changes.

*   **Facts:**
    
```yaml
    task_type: object_recoloring
    elements:
      - type: grid
        properties:
          background_color: white (0)
      - type: object
        id: main_shape
        description: The largest contiguous block of non-white pixels.
        properties:
          input_color: variable (green in train_1, red in train_2)
          output_color: determined by target_pixel
          location: preserved from input
          size: >1 pixel
      - type: object
        id: target_pixel
        description: A single non-white pixel, distinct in color from the main_shape.
        properties:
          input_color: variable (magenta in train_1, yellow in train_2)
          location: fixed (bottom-left corner in examples, potentially elsewhere)
          size: 1 pixel
        role: defines the target color for main_shape
    actions:
      - action: find_objects
        description: Identify the main_shape and the target_pixel based on color, contiguity, and size.
      - action: get_target_color
        input: target_pixel
        output: target_color (color of target_pixel)
      - action: get_target_pixel_location
        input: target_pixel
        output: target_pixel_loc (coordinates of target_pixel)
      - action: recolor_object
        target: main_shape
        using: target_color
      - action: change_pixel_color
        target_location: target_pixel_loc
        new_color: white (0)
    relationships:
      - The color of the target_pixel in the input determines the color of the main_shape in the output.
      - The original location of the target_pixel is made white in the output.
    ```


*   **Natural Language Program:**
    1.  Identify all contiguous non-white objects in the input grid.
    2.  Determine the largest object (by pixel count). This is the "primary object".
    3.  Identify any other non-white pixel(s). Assume there is exactly one such pixel, the "color source pixel".
    4.  Record the color of the "color source pixel" (this is the "target color").
    5.  Record the coordinates of the "color source pixel".
    6.  Create a new grid, initially identical to the input grid.
    7.  Iterate through all pixels of the "primary object" in the input grid and change their color to the "target color" in the new grid.
    8.  Change the color of the pixel at the recorded coordinates of the "color source pixel" to white (0) in the new grid.
    9.  The resulting grid is the output.