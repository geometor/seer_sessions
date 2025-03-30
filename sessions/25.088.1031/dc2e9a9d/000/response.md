*   **Perception:** The task involves identifying distinct green objects within the input grid and creating a corresponding copy for each. The color and relative position (either below or to the right) of the copy depend on specific geometric properties of the original green object. The background remains unchanged.

*   **YAML Facts:**
    
```yaml
    task_description: Copy green objects with modifications based on shape properties.
    background_color: white (0)
    input_objects:
      - color: green (3)
      - description: Multiple distinct contiguous shapes made of green pixels. Shapes resemble numbers or letters ('0', 'T', 'G', 'C', '4').
    output_objects:
      - color: green (3)
        source: Identical to input green objects.
      - color: blue (1)
        source: Copies of some green objects.
      - color: azure (8)
        source: Copies of other green objects.
    transformations:
      - action: identify_objects
        input: green (3) pixels
        output: list of distinct green objects
      - action: analyze_object_properties
        for_each: green object
        properties:
          - bounding_box: Minimum rectangle containing the object.
          - bottom_heavy: Does the object touch the bottom edge of its bounding box but not the top edge?
          - has_hole: Does the object contain enclosed white (0) pixels?
          - has_stem: Does the object touch the bottom edge of its bounding box with only 1 or 2 green pixels in that bottom row?
      - action: determine_copy_placement
        based_on: bottom_heavy property
        rule: If bottom_heavy, place copy below. Otherwise, place copy to the right.
        details: Maintain a 1-pixel gap (white) between original and copy bounding boxes.
      - action: determine_copy_color
        based_on: placement and object properties (has_hole, has_stem)
        rule:
          - If placed to the Right: Use blue (1).
          - If placed Below:
            - If object has_hole AND has_stem: Use blue (1).
            - Otherwise: Use azure (8).
      - action: create_copy
        for_each: green object
        output: A new object identical in shape to the original, but colored and positioned according to the determined rules.
    grid_properties:
      - size: Varies between examples.
      - background: Remains white (0). Original objects persist.
    relationships:
      - Each green object maps to exactly one new copied object (either blue or azure).
      - The position of the copy (Right or Below) is determined by the 'bottom_heavy' property.
      - The color of the copy (Blue or Azure) is determined by the placement and potentially the 'has_hole' and 'has_stem' properties.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all separate connected components (objects) consisting of green (3) pixels in the input grid.
    3.  For each identified green object:
        a.  Determine the object's bounding box (minimum row/col, maximum row/col).
        b.  Analyze the object's properties within its bounding box:
            i.  Check if it's "bottom-heavy": It touches the bottom edge (`max_row`) of its bounding box but does not touch the top edge (`min_row`).
            ii. Check if it "has a hole": It encloses one or more white (0) pixels within its shape.
            iii.Check if it "has a stem": The number of green pixels belonging to the object in the bottom row (`max_row`) of its bounding box is exactly 1 or 2.
        c.  Determine the placement for the copy:
            i.  If the object is "bottom-heavy", the copy location starts 1 row below the object's bounding box (`max_row + 2`).
            ii. Otherwise (not "bottom-heavy"), the copy location starts 1 column to the right of the object's bounding box (`max_col + 2`).
        d.  Determine the color for the copy:
            i.  If the placement is to the Right: The copy color is blue (1).
            ii. If the placement is Below:
                1.  If the object "has a hole" AND "has a stem": The copy color is blue (1).
                2.  Otherwise (placed Below, but doesn't have both hole and stem): The copy color is azure (8).
        e.  Create the copy: Iterate through the original object's pixels relative to its top-left corner. For each green pixel in the original object, draw a pixel of the determined copy color at the corresponding relative position offset by the calculated copy start location (determined in step 3c) onto the output grid. Ensure not to overwrite existing green pixels.