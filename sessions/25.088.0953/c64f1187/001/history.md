
## train_1

**input:**
```
2 0 0 0 0 3 0 0 0 0 4 0 0 0 0 8 0 0 0 0
0 1 1 0 0 0 1 1 0 0 0 1 1 0 0 0 1 0 0 0
0 1 0 0 0 0 0 1 0 0 0 1 1 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 5 5 0 5 5 0 5 5 0 0 0 0 0
0 0 0 0 5 2 0 5 5 0 5 5 0 5 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 5 5 0 5 5 0 5 5 0 0 0 0 0
0 0 0 0 5 3 0 5 2 0 5 3 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 5 5 0 5 5 0 5 5 0 0 0 0 0
0 0 0 0 5 3 0 5 5 0 5 5 0 5 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 0 0 0 0 0 0 0 4 4
2 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0 0
3 3 0 2 2 0 3 3 0 0 0
0 3 0 2 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 8 0
0 3 0 0 0 0 0 0 0 8 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 3 0 0 0 7 0 0 0 0 0 0 0
0 0 0 1 1 0 0 1 1 0 0 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 1 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 0 5 5 0 5 5 0 0
0 0 5 3 0 5 3 0 5 7 0 5 5 0 5 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 0 5 5 0 5 5 0 0
0 0 5 2 0 5 5 0 5 5 0 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 0 5 5 0 5 5 0 0
0 0 5 2 0 5 2 0 5 3 0 5 3 0 5 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 0 3 3 0 7 7 0 0 0 0 2 2
0 3 0 0 3 0 7 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 2 2 0 3 3 0 3 3 0 7 7
2 2 0 2 2 0 0 3 0 0 3 0 7 0
```

*   **Perception of the Elements:**
    The input grid is divided into two main conceptual areas.
    1.  **Definition Area (Top):** This area, located near the top of the input grid, defines associations between specific "key" colors and "shape" patterns. A single pixel of a key color (e.g., red, green, yellow, azure) appears in one row, and directly below it in subsequent rows is a small shape constructed from blue pixels. Each key color corresponds to a unique blue shape pattern.
    2.  **Instance Area (Bottom):** This area, towards the bottom, contains a grid-like structure built from gray frames (typically 2x2 gray pixels separated by white space). Inside some of these gray frames, single pixels matching the key colors from the Definition Area appear. These are instances of the keys.

    The output grid is constructed by:
    1.  Identifying the key-color-to-blue-shape mappings from the Definition Area.
    2.  Locating each key color instance within the gray frame grid in the Instance Area.
    3.  Determining the position of each instance within the frame grid (e.g., row 0, col 0; row 1, col 2, etc.).
    4.  Mapping these frame grid positions to coordinates on the output grid using a scaling factor (multiplying frame row and column by 3).
    5.  Drawing the shape associated with the key color (from step 1) at the corresponding mapped position in the output grid, using the key color itself instead of blue. The output grid's size is determined by the extent of the drawn shapes.

*   **Facts:**
    
```yaml
    perception:
      input_structure:
        - section: definition_area (top)
          content: Key colors and associated blue shapes.
          purpose: Defines a mapping from a color to a 2D pattern.
        - section: instance_area (bottom)
          content: Grid of gray frames containing instances of key colors.
          purpose: Specifies which shapes to draw and where they relate in a grid structure.
      output_structure:
        content: A grid composed of shapes placed according to instance locations.
        colors: Uses the key colors from the input's definition area.
        background: white(0).
        size: Determined by the placement and extent of the drawn shapes.

    elements:
      - element: key_color
        description: A single non-blue, non-gray, non-white pixel in the definition area.
        examples: [red(2), green(3), yellow(4), azure(8), orange(7)]
      - element: blue_shape
        description: A pattern of connected blue(1) pixels located below a key_color. Represents the shape associated with the key_color.
        properties:
          - relative_position: Below the key_color pixel.
          - size: Typically small (e.g., fits within 2x2 or 3x3).
      - element: gray_frame
        description: A structure (often 2x2) of gray(5) pixels in the instance area, forming a larger grid layout.
        properties:
          - arrangement: Regularly spaced with gaps (usually white pixels).
      - element: key_instance
        description: A pixel matching a key_color found inside a gray_frame in the instance area.
      - element: output_shape
        description: The shape pattern placed on the output grid.
        properties:
          - color: Same as the key_color of the corresponding instance.
          - pattern: Same as the blue_shape associated with the key_color.

    relationships_and_rules:
      - rule: key_shape_mapping
        description: Each key_color in the definition area is uniquely associated with the blue_shape pattern below it.
      - rule: instance_location
        description: Each key_instance is located within a specific gray_frame, defining its position in the frame grid (frame_row, frame_col).
      - rule: output_placement
        description: The output_shape corresponding to a key_instance at (frame_row, frame_col) is placed on the output grid.
        details: The top-left corner of the shape is positioned at output coordinates (row = frame_row * 3, col = frame_col * 3).
      - rule: output_coloring
        description: The output_shape is drawn using the key_color, not blue.
      - rule: output_size
        description: The output grid dimensions are determined by the minimum bounding box required to contain all placed output_shapes, based on their top-left position (frame_row*3, frame_col*3) and their dimensions.
    ```


*   **Natural Language Program:**
    1.  **Identify Key-Shape Mappings:**
        a. Scan the input grid, starting from the top row, to find isolated non-white, non-blue, non-gray pixels ("key colors").
        b. For each key color found at position `(r_key, c_key)`, examine the rows directly below it (`r_key + 1`, `r_key + 2`, ...) to find connected components of blue(1) pixels ("blue shapes").
        c. Determine the relative coordinates of the blue pixels comprising the shape with respect to a reference point (e.g., the top-leftmost blue pixel of the shape).
        d. Store a mapping for each key color to its corresponding relative blue shape pattern.
    2.  **Identify Instances and Frame Grid Positions:**
        a. Scan the input grid, focusing on the area containing gray(5) pixels, to locate the grid structure formed by gray frames.
        b. Identify the top-left corner coordinates of each potential or actual gray frame location. This defines a conceptual "frame grid".
        c. Find all non-white, non-gray pixels located *inside* these gray frame areas ("key instances"). These pixels must match one of the key colors identified in step 1a.
        d. For each key instance found, determine which gray frame it belongs to and record the frame's row (`fr`) and column (`fc`) index within the conceptual frame grid. Store the key color (`C`), frame row (`fr`), and frame column (`fc`) for each instance.
    3.  **Determine Output Grid Size:**
        a. Find the maximum `fr` (`max_fr`) and maximum `fc` (`max_fc`) among all identified instances.
        b. For each instance (`C`, `fr`, `fc`), retrieve its associated shape pattern `S` (from step 1d).
        c. Calculate the required dimensions for each shape when placed at `(fr*3, fc*3)`. The maximum row index needed will be `max(fr*3 + shape_height - 1)` over all instances, and the maximum column index needed will be `max(fc*3 + shape_width - 1)`.
        d. The output grid height is `max_row_index + 1`, and the width is `max_col_index + 1`.
    4.  **Construct the Output Grid:**
        a. Create a new grid of the determined size, initialized with the background color white(0).
        b. Iterate through each identified key instance (`C`, `fr`, `fc`).
        c. Retrieve the relative shape pattern `S` associated with the key color `C`.
        d. Calculate the top-left anchor position for drawing in the output grid: `output_row = fr * 3`, `output_col = fc * 3`.
        e. For each relative coordinate `(dr, dc)` in the shape pattern `S`, color the pixel at `(output_row + dr, output_col + dc)` in the output grid with the key color `C`.
