*   **Perception:**
    The task involves identifying different regions within the input grid based on pixel colors and connectivity, and then performing a fill operation on specific regions. Key elements are the background color, boundary-forming objects, potential fill colors derived from other objects, and determining whether the fill occurs in regions connected to the grid edge ("outside") or regions enclosed by boundaries ("inside").

    1.  **Background Identification:** The most frequent color in the grid typically serves as the background.
    2.  **Boundary Identification:** Contiguous shapes of non-background colors act as boundaries that constrain the fill operation. Often, one main boundary shape can be identified (e.g., the largest non-background object).
    3.  **Fill Color Determination:** The color used for filling is derived from specific, often unique or small, non-background, non-boundary objects present in the input grid.
    4.  **Fill Region Determination:** The core logic distinguishes between two types of fill regions:
        *   **Outside Fill:** Targets background pixels that are connected to the grid's edge. This occurs when the main boundary shape does *not* completely enclose any background region. The fill color is typically taken from the smallest non-background, non-boundary object.
        *   **Inside Fill:** Targets background pixels that are completely enclosed by the main boundary shape (cannot reach the grid edge via background pixels). This occurs when such enclosed regions exist. The fill color is determined by the color(s) found within the enclosed region in the input grid (often the most frequent non-background color within that region).
    5.  **Transformation:** The final output grid is created by replacing the pixels in the determined fill region (either inside or outside) with the determined fill color, while leaving all other pixels (boundary objects, other objects) unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    transformation_name: conditional_region_fill
    elements:
      - role: background
        property: most_frequent_color
        value: color_code
      - role: boundary
        property: forms_shapes
        value: color_code(s)
        relationship: constrains_fill
        identification: largest_contiguous_non_background_object
      - role: fill_source
        property: provides_fill_color
        value: color_code
        identification:
          if_outside_fill: color_of_smallest_non_background_non_boundary_object
          if_inside_fill: most_frequent_non_background_color_within_enclosed_region
      - role: fill_target
        property: pixels_to_be_replaced
        value: background_color_pixels
        location:
          conditional:
            if_enclosed_region_exists: background_pixels_within_enclosed_region
            else: background_pixels_connected_to_grid_edge
    actions:
      - name: identify_background_color
      - name: identify_objects
      - name: identify_main_boundary_object
      - name: identify_other_objects
      - name: check_for_enclosed_background_regions
        using: flood_fill_from_edge
      - name: determine_fill_type
        based_on: existence_of_enclosed_regions
      - name: determine_fill_color
        based_on: fill_type_and_fill_source_identification_rules
      - name: determine_fill_region
        based_on: fill_type_and_background_connectivity
      - name: apply_fill
        inputs:
          - original_grid
          - fill_region_coordinates
          - fill_color
        output: modified_grid
    relationships:
      - type: containment
        description: Boundary objects can enclose background regions.
      - type: connectivity
        description: Background pixels can be connected to the grid edge or isolated within enclosures.
      - type: derivation
        description: Fill color is derived from specific objects in the input.
      - type: constraint
        description: Boundary objects prevent the fill operation from crossing them.
    ```


*   **Natural Language Program:**
    1.  Identify the background color, which is the most frequent color in the input grid.
    2.  Identify all contiguous objects (shapes) formed by non-background colors.
    3.  Determine the main boundary object, typically the largest non-background object by pixel count. Note its color(s).
    4.  Identify all other non-background, non-boundary objects and their colors.
    5.  Check if the main boundary object fully encloses any regions of the background color. This can be done by performing a flood fill starting from all background pixels on the grid edges; any background pixels not reached by this fill are considered enclosed.
    6.  **If** enclosed background regions exist:
        a.  The fill operation targets these enclosed background pixels.
        b.  Examine the pixels within these enclosed regions in the original input grid. Identify the most frequent color present there, excluding the background color itself. This is the fill color.
    7.  **Else (if no enclosed background regions exist):**
        a.  The fill operation targets the background pixels that *are* reachable from the grid edge (identified in step 5).
        b.  Find the smallest object (by pixel count) among the 'other objects' identified in step 4. Its color is the fill color.
    8.  Create the output grid by copying the input grid, then changing the color of the pixels in the target fill region (determined in step 6a or 7a) to the determined fill color (determined in step 6b or 7b).