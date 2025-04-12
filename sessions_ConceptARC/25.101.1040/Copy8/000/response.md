Okay, let's analyze the provided examples.

**Perception of Elements:**

*   **Example 1:**
    *   Input contains a red shape above a blue rectangle on the left, and just a blue rectangle on the right. The blue rectangles appear identical in shape and size. The background is white.
    *   Output retains all elements from the input and adds a copy of the red shape above the right blue rectangle. The position of the copied red shape relative to the right blue rectangle mirrors the position of the original red shape relative to the left blue rectangle.
*   **Example 2:**
    *   Input contains a yellow '8' shape above a green 'T' shape on the left, and just a yellow '8' shape on the right. The yellow '8' shapes appear identical. The background is white.
    *   Output retains all elements from the input and adds a copy of the green 'T' shape below the right yellow '8'. The position of the copied green shape relative to the right yellow '8' mirrors the position of the original green shape relative to the left yellow '8'.

**Common Pattern:**
The core idea seems to be pattern completion based on symmetry or repetition. The grid contains pairs of identical "anchor" objects (blue rectangles in Ex1, yellow '8's in Ex2). One anchor object has an associated object ("source" object - red shape in Ex1, green shape in Ex2) positioned vertically relative to it. If the other anchor object ("target" anchor) is missing this associated object in the same relative position, the source object is copied and placed there. The relative vertical and horizontal positioning between the source and anchor is preserved during the copy operation relative to the target anchor.

**YAML Fact Document:**


```yaml
task_description: Complete vertical patterns based on paired anchor objects.

elements:
  - type: grid
    description: A 2D array of pixels with integer values 0-9 representing colors.
  - type: background
    color: white (0)
    description: The default color filling empty space.
  - type: object
    description: A contiguous block of non-background colored pixels.
    properties:
      - color: The integer value (1-9) of the pixels.
      - shape: The spatial arrangement of the pixels.
      - size: The height and width of the object's bounding box.
      - position: The row and column coordinates of the object (e.g., top-left corner or bounding box).

relationships:
  - type: spatial
    description: Relative positioning between objects.
    properties:
      - above: Object A is vertically higher than Object B.
      - below: Object A is vertically lower than Object B.
      - aligned: Objects share some vertical or horizontal coordinates.
      - vertical_offset: The difference in row indices between two objects.
      - horizontal_offset: The difference in column indices between two objects.
  - type: identity
    description: Two objects being identical.
    properties:
      - same_color: Objects have the same color value.
      - same_shape: Objects have the same pixel arrangement relative to their top-left corners.
      - same_size: Objects have the same bounding box dimensions.

actions:
  - type: identify_objects
    description: Find all contiguous blocks of non-background colors.
  - type: find_pairs
    description: Identify pairs of objects that are identical (same color, shape, size) but in different locations. These are 'anchor' pairs.
  - type: find_associated_object
    description: For one anchor ('reference'), find another object ('source') positioned directly above or below it.
  - type: calculate_relative_position
    description: Determine the row and column offset between the source object and the reference anchor (e.g., top-left to top-left).
  - type: check_completion
    description: Verify if the other anchor ('target') already has an identical object in the same relative position.
  - type: copy_object
    description: Create a duplicate of the source object's pixels.
  - type: place_object
    description: Position the copied object relative to the target anchor using the calculated relative position, overwriting only background pixels.

example_1_specifics:
  - anchor_pair: Blue rectangles (color 1).
  - reference_anchor: Left blue rectangle.
  - target_anchor: Right blue rectangle.
  - source_object: Red shape (color 2).
  - relative_position: Source is above reference.
  - completion_check: Target does not have a red shape above it.
  - action: Copy red shape and place it above the target anchor.

example_2_specifics:
  - anchor_pair: Yellow '8' shapes (color 4).
  - reference_anchor: Left yellow '8'.
  - target_anchor: Right yellow '8'.
  - source_object: Green 'T' shape (color 3).
  - relative_position: Source is below reference.
  - completion_check: Target does not have a green shape below it.
  - action: Copy green shape and place it below the target anchor.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct non-background colored objects in the input grid, noting their color, shape, size, and bounding box position.
3.  Search for pairs of objects ("anchor pairs") that are identical in color, shape, and size but are located at different positions within the grid.
4.  For each identified anchor pair:
    a.  Designate one anchor as the "reference anchor" and the other as the "target anchor". (Consistency is needed, e.g., always pick the top-most or left-most as reference).
    b.  Search for a "source object" that is located immediately above or immediately below the reference anchor (potentially separated by background pixels, but vertically aligned).
    c.  If a source object is found:
        i.  Calculate the relative position (row offset, column offset) between the top-left corner of the source object's bounding box and the top-left corner of the reference anchor's bounding box.
        ii. Check if an object identical to the source object already exists in the output grid at the calculated relative position with respect to the *target* anchor's top-left corner.
        iii. If no such object exists at the target location, copy the source object's pixels and paste them onto the output grid at the calculated relative position with respect to the target anchor's top-left corner. Ensure pasting only overwrites background (white) pixels in the target area.
5.  Repeat step 4 for all identified anchor pairs and their associated source objects.
6.  Return the modified output grid.