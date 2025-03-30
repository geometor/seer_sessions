## General Assessment

The provided code attempts to solve the task by identifying objects, classifying them as "sources" (containing multiple colors) or "targets" (containing a single color) based on a "primary color" derived from the object's pixels, and then copying a pattern from the source to the targets.

The code failed on all training examples. The results show that while the object identification and source/target classification might be conceptually correct, the specific definition of the "pattern" being copied and the method of placing it onto the target are flawed.

*   **Incorrect Pattern Extraction:** The code extracts the entire bounding box of the source object as the pattern. However, the expected outputs indicate that only the *internal* content of the source (pixels *different* from the primary/frame color) should be considered the pattern.
*   **Incorrect Pattern Placement:** The code places the extracted pattern by aligning the top-left corner of the pattern with the top-left corner of the target object's bounding box, overwriting whatever is there. The expected outputs show that the source's internal pattern should replace the *internal* content of the target, leaving the target's frame (pixels matching the primary color) intact.

**Strategy:**

1.  Refine the definition of the "source pattern": It consists only of the pixels within the source object's bounding box that *do not* match the object's primary/frame color.
2.  Refine the pattern application logic: For each target object, identify the area corresponding to its internal content. Copy the source pattern into this area, pixel by pixel, preserving the target's original frame pixels. The relative position of the pattern pixels within the source frame should be maintained when placing them inside the target frame.

## Metrics

| Example | Input Objects                                                                   | Output Objects                                                                       | Code Failure Analysis                                                                                                                               |
| :------ | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1       | Source: Green frame with Yellow/Blue/Azure inside. Target: Green frame.         | Source: Unchanged. Target: Green frame with Yellow/Blue/Azure pattern copied inside.   | Code copied the source's Green frame *and* its contents, overwriting the top-left part of the target frame and adjacent background.                  |
| 2       | Source: Red frame with Magenta/Azure inside. Targets: Two Red frames.           | Source: Unchanged. Targets: Both Red frames with Magenta/Azure pattern copied inside. | Code copied the source's Red frame *and* its contents onto the top-left of both target frames, overwriting parts of the target frames and background. |
| 3       | Source: Azure frame with Yellow/Red inside. Targets: Two Azure frames.          | Source: Unchanged. Targets: Both Azure frames with Yellow/Red pattern copied inside.   | Code copied the source's Azure frame *and* its contents onto the top-left of both target frames, overwriting parts of the target frames and background. |

## YAML Facts


```yaml
task_description: Copy the internal pattern from a 'source' object into one or more 'target' objects of the same primary color.

definitions:
  object: A connected component of non-background (non-white) pixels.
  primary_color: The color forming the outer frame or main body of an object. For multi-colored objects, it's typically the color of the outermost layer or the most frequent color connected to the background. For single-colored objects, it's simply that color. (Refinement: The code's method of using the first found pixel seems sufficient for these examples, as the frames are uniform).
  source_object: An object containing pixels of its primary color AND pixels of other color(s) internally.
  target_object: An object containing *only* pixels of its primary color.
  internal_pattern: The configuration of pixels within the source object's bounding box whose color is *different* from the source object's primary color.
  frame_pixels: Pixels within an object's bounding box whose color *matches* the object's primary color.

observations:
  - The grid contains one or more objects, identifiable by their color and connectivity.
  - Objects can be grouped by their primary color (e.g., all green-framed objects).
  - Within each color group, there is typically one source object and one or more target objects.
  - The source object contains an internal pattern composed of colors different from its primary color.
  - Target objects are composed solely of their primary color and share the same shape/size as the source object's frame in these examples.

actions:
  - Identify all objects and determine their primary color, bounding box, and pixel set.
  - Classify objects into sources and targets based on whether they contain colors other than their primary color.
  - Group objects by primary color.
  - For each group containing exactly one source and at least one target:
    - Define the source's internal pattern (pixels within the source bbox != primary color).
    - For each target object in the group:
      - Iterate through the positions within the source object's bounding box.
      - If a pixel at a relative position `(dr, dc)` within the source bounding box belongs to the *internal pattern* (i.e., its color is not the primary color):
        - Copy this pixel's color to the corresponding relative position `(dr, dc)` within the *target* object's bounding box in the output grid.
      - Pixels corresponding to the source's frame pixels are *not* copied; the target's frame pixels remain unchanged in the output grid.
  - The output grid starts as a copy of the input grid and is modified by these copy operations.

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected components (objects) of non-background (non-white) pixels in the input grid.
3.  For each object, determine its primary color (the color of its frame or main body, identifiable as the color of the first pixel encountered during object detection) and its bounding box.
4.  Classify each object:
    *   An object is a "source" if it contains at least one pixel whose color is different from its primary color.
    *   An object is a "target" if all its pixels have the same color (its primary color).
5.  Group the identified objects based on their primary color.
6.  Iterate through each group of objects sharing the same primary color.
7.  If a group contains exactly one source object and one or more target objects:
    a.  Let `S` be the source object and `P` be its primary color. Let `(min_r_src, min_c_src)` be the top-left corner of `S`'s bounding box.
    b.  For each target object `T` in the group:
        i.  Let `(min_r_tgt, min_c_tgt)` be the top-left corner of `T`'s bounding box.
        ii. Iterate through all relative coordinates `(dr, dc)` within the dimensions of the source object's bounding box.
        iii. Calculate the corresponding coordinates in the source: `sr = min_r_src + dr`, `sc = min_c_src + dc`.
        iv. Calculate the corresponding coordinates in the target: `tr = min_r_tgt + dr`, `tc = min_c_tgt + dc`.
        v.  Check if the pixel `input_grid[sr, sc]` is part of the source's *internal pattern* (i.e., `input_grid[sr, sc] != P`).
        vi. If it is part of the internal pattern AND the target coordinates `(tr, tc)` are within the grid bounds, update the output grid: `output_grid[tr, tc] = input_grid[sr, sc]`. (This overwrites the original content inside the target frame with the source's internal pattern).
8.  Return the modified output grid.