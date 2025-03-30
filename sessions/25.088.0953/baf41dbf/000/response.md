*   **Perception:**
    The task involves modifying input grids containing green shapes (often hollow rectangles) and magenta "marker" pixels. The transformation fills the area adjacent to the green shapes, using the magenta pixels as guides to determine the direction and extent of the fill. Each green shape seems associated with a specific magenta marker. If a marker is horizontally aligned with a shape (within its vertical bounds) and located to the right or left, the fill extends horizontally from the shape's edge towards the marker's column. If a marker is vertically aligned with a shape (within its horizontal bounds) and located above or below, the fill extends vertically from the shape's edge towards the marker's row. The fill color is always green. Multiple shapes and markers can exist in a single grid, and each shape is filled independently based on its associated marker.

*   **Facts:**
    
```yaml
    objects:
      - type: shape
        color: green (3)
        description: Contiguous areas of green pixels, often forming hollow rectangular structures.
        properties:
          - bounding_box: The minimum rectangle enclosing the shape.
          - hollow: Often contains non-green pixels inside its boundary.
      - type: marker
        color: magenta (6)
        description: Single pixels acting as reference points.
        properties:
          - position: Coordinates (row, column) within the grid.

    relationships:
      - type: association
        from: shape (green)
        to: marker (magenta)
        description: >
          A green shape is associated with a magenta marker if the marker's position
          aligns horizontally (marker's row is within the shape's bounding box row span)
          or vertically (marker's column is within the shape's bounding box column span).
          There might be multiple markers; the association dictates the filling behavior.

    actions:
      - name: identify_shapes
        input: grid
        output: list of green shapes and their bounding boxes
      - name: identify_markers
        input: grid
        output: list of magenta marker positions
      - name: determine_fill_area
        input: green_shape, associated_marker
        output: rectangular area to be filled
        logic: >
          If the marker is horizontally aligned and to the right, the fill area extends
          from the right edge of the shape's bounding box to the marker's column,
          covering the shape's original row span.
          If the marker is horizontally aligned and to the left, the fill area extends
          from the marker's column to the left edge of the shape's bounding box,
          covering the shape's original row span.
          If the marker is vertically aligned and below, the fill area extends
          from the bottom edge of the shape's bounding box to the marker's row,
          covering the shape's original column span.
          If the marker is vertically aligned and above, the fill area extends
          from the marker's row to the top edge of the shape's bounding box,
          covering the shape's original column span.
      - name: apply_fill
        input: grid, fill_area
        output: modified_grid
        logic: >
          Change all non-magenta pixels within the specified fill_area to green (3).
          Existing green pixels remain green. Magenta pixels are never overwritten.

    state_changes:
      - element: grid pixels
        change: >
          Pixels within the calculated fill areas adjacent to green shapes are changed
          to green (3), unless they are magenta (6).
      - element: green shapes
        change: >
          Effectively grow or extend in one direction (horizontal or vertical)
          based on the associated marker.
      - element: magenta markers
        change: Remain unchanged in the output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct contiguous green (3) shapes in the input grid. For each shape, determine its bounding box (minimum and maximum row and column).
    3.  Identify the locations (row, column) of all magenta (6) pixels in the input grid.
    4.  For each identified green shape:
        a.  Iterate through all identified magenta markers.
        b.  Check if a marker aligns horizontally with the shape (marker's row is within the shape's bounding box row range) or vertically (marker's column is within the shape's bounding box column range).
        c.  If a marker aligns horizontally and is to the right of the shape's bounding box: Define a fill area spanning from the column immediately right of the bounding box up to (but not including) the marker's column, and covering all rows within the shape's bounding box row range.
        d.  If a marker aligns horizontally and is to the left of the shape's bounding box: Define a fill area spanning from the column immediately right of the marker's column up to (but not including) the bounding box's starting column, and covering all rows within the shape's bounding box row range.
        e.  If a marker aligns vertically and is below the shape's bounding box: Define a fill area spanning from the row immediately below the bounding box up to (but not including) the marker's row, and covering all columns within the shape's bounding box column range.
        f.  If a marker aligns vertically and is above the shape's bounding box: Define a fill area spanning from the row immediately below the marker's row up to (but not including) the bounding box's starting row, and covering all columns within the shape's bounding box column range.
        g.  For the determined fill area(s) associated with this green shape, iterate through all pixels within that area in the output grid.
        h.  If a pixel in the fill area is not already magenta (6), change its color to green (3).
    5.  Return the modified output grid.