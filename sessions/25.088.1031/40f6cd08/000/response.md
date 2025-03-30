*   **Perception**: The input grids contain multiple rectangular objects. For each training pair, there are several rectangles sharing the same primary "outline" or "base" color (e.g., green in train_1, red in train_2, azure in train_3). One of these rectangles has an internal pattern composed of different colors, while the others are initially solid blocks of the base color. The transformation involves identifying the patterned rectangle and copying its internal pattern onto all the solid rectangles of the same base color. The original patterned rectangle and the background remain unchanged. The copying preserves the relative positioning of the pattern within the rectangle's boundaries.

*   **Facts**:
    
```yaml
    elements:
      - type: grid
        description: A 2D array of pixels with integer values representing colors.
      - type: background
        color: white (0)
        description: The default color filling most of the grid.
      - type: object
        subtype: rectangle
        description: Contiguous blocks of non-white pixels forming rectangular shapes.
    properties:
      - object: rectangle
        attributes:
          - color: The primary color forming the solid fill or the outermost layer.
          - internal_pattern: Some rectangles have a nested structure of different colors within their bounds.
          - solid_fill: Some rectangles are filled entirely with their primary color.
          - bounding_box: Defined by minimum and maximum row and column indices.
          - size: height and width derived from the bounding box.
    relationships:
      - type: grouping
        description: Rectangles can be grouped based on their primary color.
      - type: source-target
        description: Within a color group, one rectangle acts as the 'pattern source' (contains an internal pattern), and others act as 'targets' (initially solid).
    actions:
      - name: identify_objects
        description: Locate all contiguous non-white shapes.
      - name: group_by_color
        description: Group identified objects based on their primary color.
      - name: find_pattern_source
        description: Within each color group, find the unique object containing an internal pattern (colors different from its primary color).
      - name: find_solid_targets
        description: Within each color group, find the objects that are solidly filled with the primary color.
      - name: copy_pattern
        description: For each target object, replicate the internal pattern from the corresponding source object, aligning based on relative position within their respective bounding boxes.
        input: pattern_source_object, target_object
        output: modified_target_object_area_in_grid
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct non-white rectangular objects in the input grid.
    3.  Group these objects based on their primary color (the color of their border or solid fill).
    4.  For each group of objects sharing the same primary color:
        a.  Search for a unique object within the group that contains pixels of colors *other* than its primary color (and not white). This is the 'pattern source' object for this group.
        b.  Identify all other objects in the group that are filled *only* with the primary color. These are the 'target' objects for this group.
        c.  If both a unique 'pattern source' and one or more 'target' objects are found:
            i.  Determine the bounding box (top-left corner coordinates `min_r_src`, `min_c_src`) of the 'pattern source'.
            ii. For each 'target' object:
                1.  Determine its bounding box (top-left corner `min_r_tgt`, `min_c_tgt`).
                2.  Iterate through all pixel coordinates (`r_tgt`, `c_tgt`) within the bounds of the target object.
                3.  Calculate the relative offset within the target: `offset_r = r_tgt - min_r_tgt`, `offset_c = c_tgt - min_c_tgt`.
                4.  Determine the corresponding coordinates in the source pattern: `r_src = min_r_src + offset_r`, `c_src = min_c_src + offset_c`.
                5.  Get the color value from the input grid at `(r_src, c_src)`.
                6.  Update the pixel at `(r_tgt, c_tgt)` in the output grid with this color value.
    5.  Return the final output grid.