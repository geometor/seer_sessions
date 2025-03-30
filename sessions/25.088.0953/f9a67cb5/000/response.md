*   **Perception of Task Elements:**
    *   The input grids contain a background of `white` (0) pixels.
    *   There are `azure` (8) pixels, often forming lines or blocks that act as obstacles or boundaries.
    *   Each input grid contains exactly one `red` (2) pixel, which serves as a starting point.
    *   The output grids retain the original `azure` pixels and the initial `red` pixel.
    *   The key transformation is the addition of new `red` pixels. These new `red` pixels fill connected areas of `white` pixels originating from the initial `red` pixel.
    *   The filling process is constrained by the `azure` pixels, which act as impenetrable barriers. The fill does not cross or replace `azure` pixels.
    *   The fill seems to propagate in all four cardinal directions (up, down, left, right) through contiguous `white` pixels.

*   **YAML Facts:**
    
```yaml
    task_description: "Flood fill a connected area of white pixels starting from a single red pixel, treating azure pixels as barriers."
    elements:
      - object: grid
        description: "A 2D array of pixels with colors represented by integers 0-9."
      - object: pixels
        properties:
          - color: white (0)
            role: background, fillable area
          - color: red (2)
            role: starting point for fill, fill color
          - color: azure (8)
            role: barriers, obstacles
    initial_state:
      - grid: contains white, azure, and exactly one red pixel.
    actions:
      - action: find_start_pixel
        input: input_grid
        output: coordinates of the red (2) pixel
      - action: flood_fill
        parameters:
          - start_coordinates: location of the initial red pixel
          - fill_color: red (2)
          - target_color: white (0)
          - barrier_color: azure (8)
        description: "Starting from the start_coordinates, recursively or iteratively change the color of adjacent pixels from target_color to fill_color, stopping at grid boundaries or pixels with barrier_color."
      - action: copy_grid
        input: input_grid
        output: output_grid (initial copy)
      - action: apply_fill
        input: output_grid (copy), filled_pixels_coordinates
        output: modified output_grid
        description: "Update the pixel colors in the output grid based on the results of the flood fill."
    relationships:
      - type: connectivity
        description: "White pixels are connected if they are adjacent (up, down, left, right)."
      - type: barrier
        description: "Azure pixels block the flood fill process."
      - type: origin
        description: "The single red pixel is the origin point for the flood fill."
    final_state:
      - grid: The output grid shows the original azure pixels, the original red pixel, and the connected white area reachable from the red pixel filled with red.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Find the coordinates (row, column) of the single `red` (2) pixel in the input grid.
    3.  Initialize a queue or stack for a flood fill algorithm, adding the coordinates of the initial `red` pixel. Maintain a set of visited coordinates to avoid redundant processing, also adding the initial red pixel's coordinates.
    4.  While the queue/stack is not empty:
        a.  Dequeue/pop a coordinate (current_row, current_col).
        b.  Examine the four adjacent neighbors (up, down, left, right) of the current coordinate.
        c.  For each neighbor (neighbor_row, neighbor_col):
            i.  Check if the neighbor is within the grid boundaries.
            ii. Check if the neighbor has not already been visited.
            iii. Check if the neighbor's color in the input grid is `white` (0).
            iv. If all conditions (i, ii, iii) are met:
                1.  Change the color of the pixel at (neighbor_row, neighbor_col) in the output grid to `red` (2).
                2.  Mark the neighbor coordinate as visited.
                3.  Enqueue/push the neighbor coordinate.
    5.  Return the modified output grid.