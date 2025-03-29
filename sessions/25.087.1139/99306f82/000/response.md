*   **Perception of Task Elements:**
    *   The input grids contain a prominent hollow rectangular frame made of a single color (blue in all examples).
    *   Outside this frame, there are a few scattered single pixels of different colors. The background is white (0).
    *   The output grids retain the original frame and the external colored pixels.
    *   The key transformation happens *inside* the frame: the white area within the frame is filled with colors.
    *   The filling pattern consists of concentric rectangular layers, shrinking inwards.
    *   The colors used for filling correspond exactly to the colors of the scattered pixels outside the frame.
    *   The order of the colored layers (from outermost inwards) is determined by the position of the corresponding external pixels. Specifically, pixels closer to the top-left corner (based on row + column index) provide the colors for the outer layers.

*   **YAML Facts:**
    
```yaml
    task_description: Fill the interior of a hollow rectangular frame with concentric layers of colors derived from external 'source' pixels.

    elements:
      - object: frame
        description: A hollow rectangle made of a single color.
        properties:
          - color: The color of the frame pixels (e.g., blue).
          - boundary: Defines the outer edge of the rectangle.
          - interior: The area enclosed by the frame, initially white.
      - object: source_pixel
        description: Single non-white pixels located outside the frame.
        properties:
          - color: The color of the pixel.
          - position: Row and column index (r, c).
          - sort_key: r + c (Manhattan distance from origin).
      - object: background
        description: The background color, typically white (0).

    actions:
      - action: identify_frame
        description: Locate the largest hollow rectangular object. Determine its color and bounding box.
      - action: identify_source_pixels
        description: Find all non-white pixels outside the frame's bounding box.
      - action: sort_source_pixels
        description: Order the source pixels based on their sort_key (r + c) in ascending order. Extract their colors into a sorted list.
      - action: fill_interior
        description: Fill the white interior of the frame with concentric rectangular layers, moving inwards.
        details:
          - Layer 1 uses the first color from the sorted list and fills pixels adjacent to the inner boundary of the frame.
          - Layer 2 uses the second color and fills pixels adjacent to Layer 1.
          - This continues sequentially using colors from the sorted list until the center of the frame's interior is filled.

    relationships:
      - relationship: color_mapping
        description: The colors of the source pixels determine the colors used to fill the frame's interior.
      - relationship: order_mapping
        description: The order of source pixels (sorted by r + c) determines the order of colored layers applied during filling (outermost layer corresponds to the smallest r + c).

    output_specification:
      - The output grid has the same dimensions as the input.
      - The frame object remains unchanged.
      - The source pixels outside the frame remain unchanged.
      - The interior of the frame is filled according to the fill_interior action using the sorted colors.
    ```


*   **Natural Language Program:**
    1.  Identify the largest hollow rectangular frame in the input grid. Note its color and determine the bounding box of its interior (the area originally filled with the background color, white).
    2.  Identify all non-white pixels located outside this frame's bounding box. These are the 'source' pixels.
    3.  Create a list of the colors of these source pixels.
    4.  Sort this list of colors based on the position of their corresponding source pixels: order them by the sum of the row and column index (r + c) of each source pixel, from smallest sum to largest.
    5.  Initialize the output grid as a copy of the input grid.
    6.  Iteratively fill the white interior of the frame, layer by layer, starting from the outermost layer adjacent to the frame itself and moving inwards.
    7.  For each layer, use the next color from the sorted list created in step 4. The first color in the list fills the first (outermost) layer, the second color fills the second layer, and so on.
    8.  Continue filling layers inwards until all white pixels within the frame's interior bounding box have been colored.
    9.  The final grid with the filled frame is the output.