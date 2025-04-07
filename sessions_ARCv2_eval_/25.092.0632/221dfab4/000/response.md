*   **Perception:** The task involves pattern replacement and insertion based on a template object found at the bottom of the input grid. The input grid has a background color, multiple objects of a "main" color, and a single "template" object of a specific shape and color located at the bottom. The output grid modifies the main objects and the template object, and inserts new objects based on adjacency rules.

*   **Analysis:**
    1.  **Background Identification:** The background color (blue=1 in example 1, azure=8 in example 2) is the most prevalent color, often filling the grid borders.
    2.  **Template Object Identification:** A unique, non-background object exists along the bottom row. This is the template object. Its shape (4x1 horizontal in example 1, 3x1 horizontal in example 2) and color (yellow=4 in both examples) are crucial.
    3.  **Main Object Identification:** Other non-background objects exist in the grid, composed of a "main" color (azure=8 in example 1, red=2 in example 2).
    4.  **Transformation Rules:**
        *   A specific color mapping exists: the template color (yellow=4) maps to a replacement color (green=3).
        *   Instances of the template shape composed entirely of the main object color in the input are replaced by the replacement color (green=3) in the output.
        *   The original template object itself is also replaced by the replacement color (green=3) in the output.
        *   Instances of the template shape composed entirely of the background color, which are adjacent (sharing an edge) to any pixel of the main object color in the input, are filled with the original template color (yellow=4) in the output.
        *   All other pixels (background, parts of the main object not matching the template shape) retain their original color.

*   **YAML Facts:**
    
```yaml
    elements:
      - element: grid
        properties:
          - background_color: dominant color, often at borders (blue=1 or azure=8)
      - element: object
        properties:
          - type: main_object
          - color: color different from background and template (azure=8 or red=2)
          - shape: variable, often complex clusters
      - element: object
        properties:
          - type: template_object
          - color: specific color (yellow=4)
          - shape: simple rectangle (e.g., 4x1 or 3x1 horizontal)
          - location: unique instance located on the bottom row of the input grid
      - element: color_mapping
        properties:
          - input_color: yellow=4 (from template_object)
          - output_color: green=3 (replacement_color)
    actions:
      - action: identify
        actor: agent
        inputs:
          - grid
        outputs:
          - background_color
          - main_object_color
          - template_object (shape, color, location)
          - replacement_color (based on template_object color via mapping)
      - action: find_and_replace
        actor: agent
        inputs:
          - grid
          - template_object_shape
          - main_object_color
          - replacement_color
        description: Find all occurrences of the template_object_shape composed solely of main_object_color pixels in the input grid. Replace these areas with the replacement_color in the output grid.
      - action: replace_template
        actor: agent
        inputs:
          - grid
          - template_object_location
          - template_object_shape
          - replacement_color
        description: Replace the original template_object area with the replacement_color in the output grid.
      - action: find_and_fill_adjacent
        actor: agent
        inputs:
          - grid
          - template_object_shape
          - background_color
          - main_object_color
          - template_object_color
        description: Find all occurrences of the template_object_shape composed solely of background_color pixels in the input grid that are edge-adjacent to at least one main_object_color pixel. Fill these areas with the template_object_color in the output grid.
      - action: copy_remaining
        actor: agent
        inputs:
          - input_grid
          - output_grid
        description: Copy all pixels from the input_grid to the output_grid that were not modified by the previous actions.
    relationships:
      - relationship: adjacency
        between: [template_object_shape (background color instance), main_object_color pixel]
        property: edge_adjacent
        condition: Required for the find_and_fill_adjacent action.
      - relationship: color_transformation
        between: [template_object_color, replacement_color]
        property: specific_mapping (yellow=4 -> green=3)
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid with the same dimensions as the input grid.
    2.  Identify the background color (B) by finding the most frequent color in the input grid.
    3.  Identify the "template object" by finding the unique, contiguous non-background object located entirely within the bottom row of the input grid. Record its shape (S) and color (C_template).
    4.  Identify the primary "main object color" (C_main) which constitutes the other non-background, non-template objects in the grid.
    5.  Determine the "replacement color" (C_replace) based on the template color. If C_template is yellow (4), set C_replace to green (3). (Assume default behavior or identity transformation if template color is not yellow).
    6.  Fill the output grid initially with the background color (B).
    7.  Iterate through all pixels (r, c) in the input grid:
        a.  Check if the pixel at (r, c) is the top-left corner of an instance of the template shape S.
        b.  **Rule 1 (Main Object Match):** If the area covered by S starting at (r, c) in the *input* grid consists *only* of pixels with color C_main, then fill the corresponding area in the *output* grid with C_replace.
        c.  **Rule 2 (Template Object Match):** If the area covered by S starting at (r, c) in the *input* grid consists *only* of pixels with color C_template (matching the original template object), then fill the corresponding area in the *output* grid with C_replace.
        d.  **Rule 3 (Adjacent Background Match):** If the area covered by S starting at (r, c) in the *input* grid consists *only* of pixels with color B, AND this area in the *input* grid shares at least one edge with a pixel of color C_main, then fill the corresponding area in the *output* grid with C_template.
    8.  After checking all possible locations for Rules 1, 2, and 3: Iterate through all pixels (r, c) in the input grid *again*. If the pixel at (r, c) in the *output* grid is still the background color (B), and the corresponding pixel in the *input* grid was *not* the background color (B), copy the color from the input grid pixel at (r, c) to the output grid pixel at (r, c). (This copies over parts of the main object and any other objects that were not affected by the replacement rules).