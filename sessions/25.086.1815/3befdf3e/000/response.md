*   **Perception:** The input grid contains a single, relatively small, rectangular object composed of two colors against a white background. This object consists of an outer frame of one color and an inner rectangular region of another color. The output grid is the same size as the input grid but contains a larger version of the object. The output object is constructed by expanding the original object outwards by one pixel layer. The colors within this expanded object are derived from the input object's colors, but their positions are swapped: the area corresponding to the original inner content now takes the original frame's color, and the area corresponding to the original frame now takes the original inner content's color. A new frame, using the original frame's color, is added around this transformed inner region.

*   **YAML Facts:**
    
```yaml
    task_description: Expands a two-color framed object, swaps the inner/outer colors, and adds a new outer frame.

    elements:
      - object: input_object
        description: A rectangular structure composed of non-white pixels found in the input grid.
        properties:
          - bounding_box: The minimum rectangle enclosing all non-white pixels.
          - frame_color: The color of the single-pixel-thick outer border of the input_object.
          - content_color: The color filling the rectangular region inside the frame.
          - content_bounding_box: The bounding box of the inner content region.
      - object: output_object
        description: The transformed object in the output grid.
        properties:
          - bounding_box: A rectangle 2 pixels wider and 2 pixels taller than the input_object's bounding_box.
          - frame_color: Same as the input_object's frame_color.
          - inner_region: The area inside the output_object's frame.
            properties:
              - dimensions: Same as the input_object's bounding_box dimensions.
              - color_pattern: Colors are swapped relative to the input; area corresponding to original content uses original frame_color, area corresponding to original frame uses original content_color.
      - background_color: white (0)

    actions:
      - action: find_input_object
        description: Locate the contiguous block of non-white pixels and determine its bounding_box.
      - action: identify_colors
        description: Determine the frame_color and content_color within the input_object's bounding_box.
      - action: calculate_output_dimensions
        description: Determine the bounding_box for the output_object by expanding the input_object's bounding_box by 1 pixel in each direction (top, bottom, left, right).
      - action: construct_inner_region
        description: Create a new region with the same dimensions as the input_object's bounding_box. Fill the area corresponding to the original content_bounding_box with the input frame_color. Fill the remaining area (corresponding to the original frame) with the input content_color.
      - action: construct_outer_frame
        description: Create a 1-pixel thick frame using the input frame_color around the region constructed in the previous step.
      - action: assemble_output
        description: Create an output grid of the same dimensions as the input grid, filled with the background_color. Place the combined outer frame and inner region (the output_object) into the output grid, maintaining the relative position based on the input object's top-left corner adjusted by the expansion (shifted up and left by 1 pixel).

    relationships:
      - relationship: color_swap
        description: The color placement within the core of the output object is inverted relative to the input object. The input frame color moves to the center, and the input content color moves to where the frame was.
      - relationship: expansion
        description: The output object is a 1-pixel expansion of the input object's bounding box.
      - relationship: frame_persistence
        description: The color of the input object's frame is reused as the color of the new, larger frame in the output object.
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous non-white object in the input grid.
    2.  Determine the bounding box of this object.
    3.  Identify the color of the object's outer frame (frame\_color) and the color of its inner content (content\_color).
    4.  Determine the bounding box of the inner content region.
    5.  Calculate the dimensions and position for the core part of the output object: it will be 2 pixels taller and 2 pixels wider than the input object's bounding box, starting 1 pixel above and 1 pixel to the left of the input object's top-left corner.
    6.  Construct the inner region of the output object (which has the same dimensions as the input object's bounding box):
        a.  Fill the area corresponding to the original *inner content's bounding box* with the original *frame\_color*.
        b.  Fill the remaining area within this region (corresponding to the original *frame*) with the original *content\_color*.
    7.  Construct a new 1-pixel thick outer frame around this inner region using the original *frame\_color*.
    8.  Create the final output grid, initially filled with white. Place the combined structure (new outer frame + constructed inner region) onto the output grid at the calculated position (step 5).