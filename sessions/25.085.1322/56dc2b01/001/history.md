
## train_1

**input:**
```
0 0 0 0 0
3 3 0 0 0
3 0 0 0 0
3 3 0 3 3
0 3 3 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
3 3 0 0 0
3 0 0 0 0
3 3 0 3 3
0 3 3 3 0
2 2 2 2 2
0 0 0 0 0
```


## train_2

**input:**
```
0 3 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 0 3 0 0 2 0 0 0 0 0
0 0 0 0 0 8 0 3 3 3 2 0 0 0 0 0
0 0 0 0 0 8 3 3 0 0 2 0 0 0 0 0
0 0 0 0 0 8 0 3 3 3 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
3 3 3 3 0
3 0 0 3 0
3 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
3 3 3 3 0
3 0 0 3 0
3 3 0 3 0
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Task Elements**

1.  **Input/Output Grids:** Both input and output are 2D grids of pixels with colors represented by integers 0-9. The background is white (0).
2.  **Key Objects:**
    *   **Movable Object(s):** Green pixels (color 3). These objects appear to change position from input to output. There can be one or multiple disconnected green objects, but they seem to move together as a single unit based on their collective bounding box.
    *   **Barrier Object:** Red pixels (color 2). This object appears stationary and acts as a boundary or stopping point for the green object(s). In the examples, it's always a straight horizontal or vertical line.
    *   **Marker Object:** Azure pixels (color 8). This object does not exist in the input but is created in the output. It appears as a straight line (horizontal or vertical) adjacent to the final position of the green object(s).
3.  **Transformation/Action:**
    *   **Movement:** The green object(s) move towards the red barrier. The direction of movement (up, down, left, or right) is determined by the initial relative positions of the green object(s) and the red barrier.
    *   **Stopping Condition:** The movement stops when the green object(s) become adjacent (touching) to the red barrier.
    *   **Marker Creation:** An azure line or column is created in the output. Its position is directly adjacent to the *final* position of the green object(s), on the side opposite the red barrier (i.e., the side from which the green object(s) approached). The marker spans the full width or height of the grid.

**Detailed Analysis of Examples**

*   **Train 1:** Green objects are above the red line. They move down until they are just above the red line. An azure line appears one row above the highest green pixel in its final position, spanning the grid's width.
*   **Train 2:** The green object is to the left of the red line. It moves right until it is just to the left of the red line. An azure column appears one column to the left of the leftmost green pixel in its final position, spanning the grid's height.
*   **Train 3:** The green object is below the red line. It moves up until it is just below the red line. An azure line appears one row below the lowest green pixel in its final position, spanning the grid's width.

**YAML Fact Sheet**


```yaml
task_description: "Move green object(s) towards a stationary red barrier until adjacent, then place an azure marker line/column adjacent to the moved green object(s) on the side opposite the barrier."

elements:
  - object: background
    color_code: 0
    color_name: white
    properties: [stationary, occupies_empty_space]
  - object: movable_unit
    color_code: 3
    color_name: green
    properties: [moves_towards_barrier, can_be_multiple_disconnected_parts, treated_as_single_unit_for_movement]
  - object: barrier
    color_code: 2
    color_name: red
    properties: [stationary, stops_movable_unit, typically_a_line]
  - object: marker
    color_code: 8
    color_name: azure
    properties: [created_in_output, always_a_line_or_column, adjacent_to_moved_unit, position_relative_to_movement_direction, spans_full_grid_dimension]

relationships_and_actions:
  - action: identify_objects
    actor: system
    inputs: [input_grid]
    outputs: [movable_unit_pixels, barrier_pixels]
  - action: determine_movement_direction
    actor: system
    inputs: [movable_unit_pixels, barrier_pixels]
    outputs: [direction]
    logic: "Determine if the movable unit is primarily above, below, left, or right of the barrier based on bounding boxes."
  - action: calculate_translation
    actor: system
    inputs: [movable_unit_pixels, barrier_pixels, direction]
    outputs: [translation_vector]
    logic: "Calculate distance needed to move the movable unit until it is exactly one pixel away from the barrier in the specified direction."
  - action: apply_translation
    actor: system
    inputs: [movable_unit_pixels, translation_vector]
    outputs: [moved_unit_pixels]
  - action: determine_marker_position_and_orientation
    actor: system
    inputs: [moved_unit_pixels, direction, grid_dimensions]
    outputs: [marker_pixels]
    logic: |
      - If moved DOWN, marker is a horizontal line one row ABOVE the min_row of moved_unit_pixels, spanning grid width.
      - If moved UP, marker is a horizontal line one row BELOW the max_row of moved_unit_pixels, spanning grid width.
      - If moved RIGHT, marker is a vertical column one column LEFT of the min_col of moved_unit_pixels, spanning grid height.
      - If moved LEFT, marker is a vertical column one column RIGHT of the max_col of moved_unit_pixels, spanning grid height.
  - action: construct_output_grid
    actor: system
    inputs: [grid_dimensions, background_pixel, barrier_pixels, moved_unit_pixels, marker_pixels]
    outputs: [output_grid]
    logic: "Initialize grid with background, place barrier pixels (original position), place moved unit pixels, place marker pixels."

grid_properties:
  - background_color: 0 (white)
  - dynamic_dimensions: true
```


**Natural Language Program**

1.  Identify all green pixels (color 3) which form the "movable unit" and all red pixels (color 2) which form the "barrier".
2.  Determine the bounding boxes for the movable unit and the barrier.
3.  Compare the bounding boxes to determine the primary relative direction (is the movable unit above, below, left, or right of the barrier?). This is the direction of movement.
4.  Calculate the distance required to move the movable unit along this direction so that its edge is exactly one pixel away from the nearest edge of the barrier.
5.  Create a new grid of the same dimensions as the input, filled with the background color (white, 0).
6.  Copy the barrier (red pixels) to the new grid in their original positions.
7.  Calculate the new coordinates for each pixel of the movable unit by applying the calculated translation (distance and direction). Place these translated green pixels onto the new grid.
8.  Determine the position and orientation of the azure marker (color 8):
    *   If the movement was DOWN, create a horizontal azure line one row *above* the top edge (minimum row) of the moved green unit, spanning the full width of the grid.
    *   If the movement was UP, create a horizontal azure line one row *below* the bottom edge (maximum row) of the moved green unit, spanning the full width of the grid.
    *   If the movement was RIGHT, create a vertical azure column one column *to the left* of the left edge (minimum column) of the moved green unit, spanning the full height of the grid.
    *   If the movement was LEFT, create a vertical azure column one column *to the right* of the right edge (maximum column) of the moved green unit, spanning the full height of the grid.
9.  Draw the determined azure marker onto the new grid.
10. The resulting grid is the output.
