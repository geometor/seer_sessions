Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

*   **Example 1:**
    *   Input: Contains two main visual elements separated by white pixels.
        *   Left element: A magenta (6) square frame containing a diagonal line of green (3) pixels.
        *   Right element: An orange (7) square frame containing only white (0) pixels internally.
    *   Output: The overall structure is preserved. The left element is unchanged. The right element now has a green (3) diagonal line inside it, mirroring the pattern from the left element. The green pixels replace the original white pixels at those locations.
*   **Example 2:**
    *   Input: Also contains two main visual elements separated by white pixels.
        *   Left element: A larger, irregular shape made of yellow (4) pixels, containing an anti-diagonal line of blue (1) pixels.
        *   Right element: A smaller solid rectangle made of red (2) pixels.
    *   Output: The overall structure is preserved. The left element is unchanged. The right element now has an anti-diagonal line of blue (1) pixels inside it, mirroring the pattern from the left element. The blue pixels replace the original red pixels at those locations.

**General Observations:**

1.  **Object Identification:** The grids contain distinct non-white objects, often separated by white space.
2.  **Pattern Source and Target:** There seem to be two primary objects involved. One acts as a 'source' containing an internal pattern (a different color), and the other acts as a 'target' where this pattern is copied or imprinted.
3.  **Pattern Extraction:** The pattern consists of pixels of a specific color located *within* the bounding box of the source object, but differing from the source object's main color.
4.  **Pattern Transfer:** The relative positions of the pattern pixels within the source object's bounding box are calculated. These relative positions are then applied to the target object's bounding box to determine where the pattern color should be placed in the output.
5.  **Imprinting:** The pattern color replaces the existing color at the target locations.
6.  **Preservation:** Pixels not part of the transferred pattern generally retain their original color from the input.

**YAML Facts:**


```yaml
task_description: Copy an internal color pattern from a source object to a target object based on relative positions within their bounding boxes.

definitions:
  - object: A connected component of non-white pixels.
  - bounding_box: The smallest rectangle enclosing all pixels of an object.
  - primary_color: The most frequent non-white color constituting an object's main structure (e.g., the frame color).
  - pattern_color: A color found within the bounding box of the source object that is different from its primary_color and also not white.
  - source_object: The object containing the pattern_color pixels within its bounding box.
  - target_object: The object onto which the pattern is copied.

actions:
  - identify_objects: Find all distinct non-white connected components.
  - determine_largest_objects: Select the two most prominent objects (e.g., by bounding box size or pixel count).
  - identify_source_target_pattern:
      - For each prominent object:
        - Check if its bounding box contains pixels of a color different from its primary color and white.
        - If yes, designate this object as 'source', the other prominent object as 'target', and the differing color as 'pattern_color'.
  - extract_pattern_relative_coords: Find all pixels of 'pattern_color' within the 'source_object's bounding box and calculate their coordinates relative to the top-left corner of this bounding box.
  - apply_pattern_to_target:
      - For each relative coordinate (dr, dc) from the source pattern:
        - Calculate the absolute coordinate (target_row, target_col) by adding (dr, dc) to the top-left coordinate of the 'target_object's bounding box.
        - If the calculated coordinate is within the grid bounds, update the pixel at (target_row, target_col) in the output grid to the 'pattern_color'.
  - copy_unchanged_pixels: Ensure all pixels not modified by the pattern transfer retain their original input color.

example_1:
  objects:
    - Magenta (6) frame object (source)
    - Orange (7) frame object (target)
  pattern_color: Green (3)
  source_pattern_relative_coords: [(0,1), (1,2), (2,3), (3,4), (4,5)] (relative to magenta box top-left)
  target_application: The green pattern is imprinted onto the orange object's area.

example_2:
  objects:
    - Yellow (4) shape object (source)
    - Red (2) rectangle object (target)
  pattern_color: Blue (1)
  source_pattern_relative_coords: [(0,4), (1,3), (2,2), (3,1), (4,0)] (relative to yellow box top-left)
  target_application: The blue anti-diagonal pattern is imprinted onto the red object's area.

```


**Natural Language Program:**

1.  **Initialize:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Objects:** Find all connected components (objects) of non-white pixels in the input grid.
3.  **Select Main Objects:** Identify the two largest objects (e.g., by bounding box area). Label them Object A and Object B. If fewer than two objects exist, stop and return the copied input grid.
4.  **Find Source, Target, and Pattern:**
    a.  Determine the primary color and bounding box of Object A. Check if any pixels *within* Object A's bounding box have a color that is *not* white and *not* Object A's primary color. If such a pixel exists, designate Object A as the `source_object`, Object B as the `target_object`, and the color of this pixel as the `pattern_color`. Proceed to step 5.
    b.  If no pattern was found in Object A, perform the same check for Object B: Determine its primary color and bounding box. Check if any pixels *within* Object B's bounding box have a color that is *not* white and *not* Object B's primary color. If found, designate Object B as `source_object`, Object A as `target_object`, and this color as `pattern_color`. Proceed to step 5.
    c.  If neither object contains a pattern according to these rules, stop and return the copied input grid.
5.  **Extract Relative Pattern:**
    a.  Get the top-left coordinates (`source_r0`, `source_c0`) of the `source_object`'s bounding box.
    b.  Create a list of relative coordinates `pattern_coords`.
    c.  Iterate through all pixels (`r`, `c`) within the `source_object`'s bounding box.
    d.  If the pixel at (`r`, `c`) has the `pattern_color`, add its relative coordinates (`r - source_r0`, `c - source_c0`) to the `pattern_coords` list.
6.  **Apply Pattern to Target:**
    a.  Get the top-left coordinates (`target_r0`, `target_c0`) of the `target_object`'s bounding box.
    b.  For each relative coordinate (`dr`, `dc`) in `pattern_coords`:
        i.  Calculate the target absolute coordinates: `target_r = target_r0 + dr`, `target_c = target_c0 + dc`.
        ii. Check if `target_r` and `target_c` are valid coordinates within the dimensions of the output grid.
        iii. If the coordinates are valid, update the pixel at (`target_r`, `target_c`) in the output grid to the `pattern_color`.
7.  **Finalize:** Return the modified output grid.