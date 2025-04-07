*   **Perception:**
    The input grids contain complex background patterns and one or more distinct rectangular regions embedded within them. These regions are defined by a perimeter or "frame" of one or more specific colors, distinct from both the background and the pixels enclosed within the frame. The task requires identifying these framed rectangular regions, ordering them (likely by their top-left corner's position), selecting the second region found, and extracting the complete rectangular area defined by this second frame's bounding box as the output.

*   **Facts (YAML):**
    
```yaml
    task_type: object_extraction
    objects:
      - type: background
        description: A pattern filling most of the grid, potentially complex (repeating columns, horizontal stripes). Varies between examples.
      - type: framed_rectangle
        description: Rectangular areas embedded in the background, defined by a perimeter border of one or more specific, non-background colors. The content inside the frame differs from the frame color(s) and the background.
        properties:
          - border_color(s): The color(s) forming the perimeter (e.g., green, blue, magenta, orange). Can be a single color or specific combination (like green on 3 sides, blue on 1).
          - bounding_box: The coordinates defining the rectangle (min_row, min_col, max_row, max_col).
          - content: The pixels enclosed within the border.
          - order: Position relative to other framed_rectangles when ordered by top-left corner (row-major).
    actions:
      - identify: Locate all distinct framed_rectangle objects within the input grid.
      - order: Arrange the identified framed_rectangles based on their top-left corner coordinates (first by row, then by column).
      - select: Choose the second framed_rectangle from the ordered list.
      - extract: Copy the subgrid corresponding to the bounding box of the selected framed_rectangle.
    relationships:
      - framed_rectangles are embedded within the background.
      - framed_rectangles are distinct from each other.
      - the output corresponds exactly to the bounding box of the *second* identified and ordered framed_rectangle.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all distinct rectangular regions that are enclosed by a frame (a perimeter of one or more specific colors distinct from the immediate background and the region's interior content).
    2.  For each identified framed region, determine its bounding box (top-most row, left-most column, bottom-most row, right-most column).
    3.  Create a list of these identified framed regions.
    4.  Sort the list of regions based on their top-left corner coordinates, primarily by row index (ascending) and secondarily by column index (ascending).
    5.  Select the second region from the sorted list.
    6.  Extract the subgrid from the input grid corresponding exactly to the bounding box coordinates of the selected second region. This extracted subgrid is the output.