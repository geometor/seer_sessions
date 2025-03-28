*   **Perception**: The input grids contain a prominent dividing line (either a full row or a full column of a single non-background color) separating the grid into two main sections. Besides the dividing line, there are four distinct colored objects, typically two on each side of the line. The output grid is consistently a 6x6 grid, seemingly constructed by taking a representation of each of the four objects and arranging them in a 2x2 layout. The dividing line itself is absent in the output. The relative positioning of the objects in the output mirrors their relative positions (top/bottom, left/right) across the dividing line in the input. Specifically, the objects appear to be cropped to their top-left 3x3 portion and placed into corresponding 3x3 quadrants in the 6x6 output grid.

*   **Facts**:
    
```yaml
    task_type: object_manipulation
    grid_properties:
      - input_dimensions: variable (e.g., 15x13, 12x13, 16x12)
      - output_dimensions: fixed (6x6)
    elements:
      - type: background
        color: white (0)
      - type: divider
        description: A single complete row or column composed of a single non-white color. It separates the grid.
        properties:
          - orientation: horizontal or vertical
          - color: variable (blue, red, green in examples)
      - type: object
        description: Contiguous block of a single non-white color, excluding the divider color.
        properties:
          - color: variable (red, green, gray, azure, blue, yellow in examples)
          - count: 4 per input grid
          - position: Located on either side of the divider line.
    transformations:
      - action: identify
        target: divider line (orientation and position)
      - action: identify
        target: four distinct objects (excluding divider)
      - action: find_bounding_box
        target: each object
      - action: crop
        target: each object's bounding box
        details: Extract the top-left 3x3 subgrid from the bounding box.
      - action: determine_relative_position
        target: each object
        details: Categorize each object as Top-Left, Top-Right, Bottom-Left, or Bottom-Right based on its position relative to the divider line and other objects.
          - Vertical Divider: Top/Bottom based on row index, Left/Right based on column index relative to divider.
          - Horizontal Divider: Top/Bottom based on row index relative to divider, Left/Right based on column index.
      - action: construct_output
        details: Create a 6x6 grid.
      - action: place
        target: cropped 3x3 object grids
        destination: output grid quadrants
        details:
          - Top-Left object crop -> Output[0:3, 0:3]
          - Top-Right object crop -> Output[0:3, 3:6]
          - Bottom-Left object crop -> Output[3:6, 0:3]
          - Bottom-Right object crop -> Output[3:6, 3:6]
    relationships:
      - The output grid's structure (2x2 arrangement of 3x3 blocks) reflects the spatial relationship (quadrants) of the input objects relative to the dividing line.
      - The content of each 3x3 block in the output corresponds to the top-left 3x3 section of one specific input object.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a 6x6 grid filled with the background color (white, 0).
    2.  Scan the input grid to find a dividing line, defined as a complete row or column filled with a single color other than white. Record the divider's color, orientation (horizontal/vertical), and index (row or column number).
    3.  Identify all distinct contiguous objects in the input grid that are neither the background color nor the divider color. There should be exactly four such objects.
    4.  For each of the four objects:
        a.  Determine its minimal bounding box (minimum row, maximum row, minimum column, maximum column).
        b.  Extract the 3x3 subgrid from the top-left corner of its bounding box (using the minimum row and minimum column indices). This is the object's "crop".
    5.  Categorize the four objects based on their position relative to the dividing line:
        a.  If the divider is vertical at column `d`:
            i.  Identify the "Left" objects (bounding box entirely to the left of `d`).
            ii. Identify the "Right" objects (bounding box entirely to the right of `d`).
            iii.Among the "Left" objects, the one with the smaller minimum row index is "Top-Left", the other is "Bottom-Left".
            iv. Among the "Right" objects, the one with the smaller minimum row index is "Top-Right", the other is "Bottom-Right".
        b.  If the divider is horizontal at row `r`:
            i.  Identify the "Top" objects (bounding box entirely above `r`).
            ii. Identify the "Bottom" objects (bounding box entirely below `r`).
            iii.Among the "Top" objects, the one with the smaller minimum column index is "Top-Left", the other is "Top-Right".
            iv. Among the "Bottom" objects, the one with the smaller minimum column index is "Bottom-Left", the other is "Bottom-Right".
    6.  Place the 3x3 crops into the 6x6 output grid:
        a.  Copy the crop of the "Top-Left" object to the output grid region from row 0 to 2 and column 0 to 2.
        b.  Copy the crop of the "Top-Right" object to the output grid region from row 0 to 2 and column 3 to 5.
        c.  Copy the crop of the "Bottom-Left" object to the output grid region from row 3 to 5 and column 0 to 2.
        d.  Copy the crop of the "Bottom-Right" object to the output grid region from row 3 to 5 and column 3 to 5.
    7.  Return the completed 6x6 output grid.