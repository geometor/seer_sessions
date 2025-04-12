
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0 0 0 0 0 0 4 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input grids contain distinct, non-background colored objects (or groups of pixels of the same color). In the first example, these are solid rectangles (red and blue). In the second example, they are patterns of individual pixels (green and yellow). The background is uniformly white (0).

The transformation involves moving these colored objects horizontally across the grid. The direction of movement appears to depend on the color of the object. Objects move until they reach the corresponding edge (left or right) of the grid. Their vertical position and internal structure (shape or relative pixel arrangement) are preserved.

Specifically:
- Red (2) objects move left.
- Blue (1) objects move right.
- Green (3) objects move left.
- Yellow (4) objects move right.

The background remains unchanged.

## Facts


```yaml
task_context:
  grid_size: Variable dimensions for both input and output.
  background_color: White (0).
  num_examples: 2 provided for analysis.

objects:
  - type: contiguous_group
    color: Non-white (1-9)
    properties:
      - shape: Variable (rectangle in ex1, dispersed pixels in ex2)
      - color: Determines movement direction (Red/Green left, Blue/Yellow right)
      - position: Initial coordinates in the input grid.

actions:
  - name: identify_objects
    inputs: input_grid
    outputs: list_of_objects (with color, pixels, bounding_box)
    description: Find all contiguous groups of non-white pixels.
  - name: determine_movement_direction
    inputs: object_color
    outputs: direction (left or right)
    rules:
      - if color is Red (2) or Green (3), direction is left.
      - if color is Blue (1) or Yellow (4), direction is right.
  - name: translate_object_horizontally
    inputs: object, direction, grid_width
    outputs: new_object_position
    description: |
      Move the object horizontally in the specified direction until any part
      of the object reaches the corresponding grid boundary (column 0 for left,
      last column for right). The vertical position remains unchanged.
  - name: reconstruct_output_grid
    inputs: list_of_translated_objects, grid_dimensions, background_color
    outputs: output_grid
    description: Create a new grid of the original dimensions, filled with the background color, and place the translated objects at their new positions.

relationships:
  - type: movement_constraint
    elements: [object, grid_boundary]
    description: Objects stop moving when they reach the edge of the grid corresponding to their movement direction.
  - type: color_direction_mapping
    elements: [object_color, movement_direction]
    description: The color of an object dictates whether it moves left or right.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
2.  Identify all distinct contiguous objects (groups of connected pixels of the same color) in the input grid, excluding the background color. For each object, record its color and the coordinates of all its pixels.
3.  For each identified object:
    a.  Determine its horizontal movement direction based on its color:
        *   If the color is Red (2) or Green (3), the direction is 'left'.
        *   If the color is Blue (1) or Yellow (4), the direction is 'right'.
    b.  Calculate the target horizontal position:
        *   If the direction is 'left', determine the minimum column index occupied by the object's pixels. Calculate the horizontal shift required to move this minimum column index to 0.
        *   If the direction is 'right', determine the maximum column index occupied by the object's pixels. Calculate the horizontal shift required to move this maximum column index to the last column index of the grid.
    c.  Calculate the new coordinates for each pixel of the object by applying the calculated horizontal shift. The vertical coordinates remain unchanged.
    d.  Place the object (using its original color) onto the output grid at its new coordinates.
4.  Return the final output grid.
