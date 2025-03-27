*   **Perception:**
    The input grids contain a background of white pixels and several objects composed of colored pixels. One distinct object is a straight line (either horizontal or vertical) made of red pixels, always located along one of the grid edges. The other objects are composed of various non-white, non-red colors. The transformation involves moving these non-red objects towards the red line until they become adjacent to it. The red line itself remains stationary. The space vacated by the moving objects becomes white.

*   **YAML Facts:**
    
```yaml
    task_description: Move colored objects towards a fixed red boundary line.
    elements:
      - element: grid
        properties:
          - dimensions: variable height and width (up to 30x30)
          - background_color: white (0)
      - element: barrier_object
        properties:
          - color: red (2)
          - shape: straight line (horizontal or vertical)
          - location: fixed along one edge of the grid (left, right, top, or bottom)
          - role: stationary boundary
      - element: movable_objects
        properties:
          - color: any non-white (0) and non-red (2) color (1, 3, 4, 5, 6, 7, 8, 9)
          - shape: contiguous blocks of one or more pixels of the same movable color
          - initial_location: scattered within the grid
          - role: dynamic elements that change position
    actions:
      - action: identify_barrier
        input: input_grid
        output: location (edge) and orientation (horizontal/vertical) of the red line
      - action: identify_movable_objects
        input: input_grid
        output: list of all contiguous non-white, non-red objects (pixels, color, shape, location)
      - action: determine_movement_direction
        input: barrier location/orientation
        output: direction (left, right, up, or down) towards the barrier
      - action: calculate_final_position
        input:
          - movable_object (shape, initial_location)
          - barrier_location/orientation
          - movement_direction
        process: Shift the object in the specified direction until one of its pixels is directly adjacent (sharing an edge) to a pixel of the red barrier line.
        output: final_location of the movable_object
      - action: construct_output_grid
        input:
          - grid_dimensions
          - barrier_object (color, location)
          - all movable_objects (color, final_location)
        process: Create a new grid of the original dimensions, filled with the background color. Place the barrier object. Place all movable objects in their calculated final positions.
        output: output_grid
    relationships:
      - Movable objects are translated towards the barrier object.
      - The movement stops based on adjacency to the barrier object.
      - The barrier object's position determines the direction of movement for all movable objects.
      - Movable objects retain their shape and color during the transformation.
    ```


*   **Natural Language Program:**
    1.  Identify the red (color 2) line object. Note its location (which edge it lies on: top, bottom, left, or right) and orientation (horizontal or vertical). This line acts as a fixed barrier.
    2.  Identify all other distinct objects composed of contiguous pixels that are not white (color 0) and not red (color 2).
    3.  Determine the direction of movement based on the barrier's location:
        *   If the barrier is on the left edge, the direction is left.
        *   If the barrier is on the right edge, the direction is right.
        *   If the barrier is on the top edge, the direction is up.
        *   If the barrier is on the bottom edge, the direction is down.
    4.  For each identified movable object:
        *   Calculate its final position by shifting it purely in the determined direction (horizontally or vertically) until one of its pixels is directly adjacent (shares an edge, not just a corner) to any pixel of the red barrier line. The object's shape and color remain unchanged.
    5.  Create the output grid, having the same dimensions as the input grid and initially filled with white pixels (color 0).
    6.  Place the red barrier line onto the output grid in its original position.
    7.  Place each movable object onto the output grid in its calculated final position.