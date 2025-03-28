*   **Perception:**
    *   Each input grid contains a larger contiguous object of one color (the "container") and a single pixel of a different color (the "source") located strictly inside the container object. The rest of the grid is background (white).
    *   The container objects have varied shapes (cloud/mountain-like, L-shape, irregular blob).
    *   The source pixel's color is different in each example (green, blue, red).
    *   The container object's color is also different (azure, red, green).
    *   In the output grid, the source pixel's color is extended in a straight line (up, down, or right in the examples) from the source pixel's original position.
    *   This line of color fills the pixels within the container object along that path, stopping at the boundary of the container object. The original container object and source pixel remain otherwise unchanged.
    *   The direction of the line seems to be determined by the position of the source pixel relative to the container's boundaries. Specifically, the line extends in the direction *opposite* to the nearest boundary of the container object from the source pixel.

*   **Facts:**
    
```yaml
    task_elements:
      - object: container
        description: The largest contiguous block of non-background pixels.
        properties:
          - color: Varies (azure, red, green in examples).
          - shape: Irregular, defines boundaries.
      - object: source_pixel
        description: A single pixel located strictly inside the container object with a different color.
        properties:
          - color: Varies (green, blue, red in examples).
          - count: Always 1 in examples.
          - location: Strictly within the bounds of the container object.
      - object: background
        description: The area outside the container object.
        properties:
          - color: white (0).
      - object: projection_line
        description: A line of pixels created in the output.
        properties:
          - color: Same as the source_pixel color.
          - shape: Straight line (vertical or horizontal).
          - start_location: Adjacent to the source_pixel.
          - end_location: The boundary of the container object.
          - extent: Fills the space between the start and end locations within the container.
    relationships:
      - type: containment
        subject: source_pixel
        object: container
        details: The source_pixel is located inside the container.
      - type: spatial_proximity
        subject: source_pixel
        object: container_boundary
        details: The distance from the source_pixel to the container boundary in each cardinal direction (up, down, left, right) determines the projection direction.
    actions:
      - action: identify_objects
        actor: system
        details: Find the container object and the source_pixel within it.
      - action: determine_shortest_distance_to_boundary
        actor: system
        input: source_pixel position, container object boundaries
        output: The cardinal direction (up, down, left, right) corresponding to the shortest distance from the source_pixel to a pixel outside the container.
      - action: determine_projection_direction
        actor: system
        input: Shortest distance direction
        output: The cardinal direction opposite to the shortest distance direction.
      - action: project_color
        actor: system
        input: source_pixel color, projection_direction, source_pixel position, container object
        output: A modified grid where pixels along the projection_direction, starting from the source_pixel position, are changed to the source_pixel color until the container boundary is reached.
        details: The projection fills the path within the container.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the largest contiguous object of non-white pixels; this is the "container". If no such object exists or it fills the entire grid, return the copied input grid.
    3.  Identify all pixels within the container object that have a different color than the container itself.
    4.  If exactly one such pixel exists, designate it as the "source pixel". If zero or more than one such pixel exists, return the copied input grid.
    5.  Determine the coordinates (row, col) of the source pixel.
    6.  Calculate the distance from the source pixel to the nearest non-container pixel (either background or a different object) in each of the four cardinal directions (up, down, left, right), staying within the grid boundaries.
        *   Distance Up: Number of container-colored pixels directly above the source pixel.
        *   Distance Down: Number of container-colored pixels directly below the source pixel.
        *   Distance Left: Number of container-colored pixels directly to the left of the source pixel.
        *   Distance Right: Number of container-colored pixels directly to the right of the source pixel.
    7.  Find the direction(s) with the minimum distance. (Assume based on examples there will be only one minimum direction).
    8.  Determine the projection direction, which is the cardinal direction opposite to the minimum distance direction (Up -> Down, Down -> Up, Left -> Right, Right -> Left).
    9.  Starting from the pixel adjacent to the source pixel in the projection direction, change the color of pixels in that direction to the source pixel's color.
    10. Continue this color change along the projection direction until a pixel belonging to the container boundary (i.e., a non-container colored pixel) is encountered or the grid edge is reached. Do not change the boundary pixel itself.
    11. Return the modified output grid.