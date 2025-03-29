*   **Perception:**
    *   The input grids contain a white background and exactly two identical non-white pixels (red in the examples).
    *   The output grids maintain the same dimensions as the input.
    *   The output grids feature a frame or bounding box constructed using the color of the input pixels.
    *   The frame is defined by the rows and columns of the two input pixels. Specifically, horizontal lines are drawn at the rows of the input pixels, and vertical lines are drawn at the columns of the input pixels.
    *   The rectangular area strictly *inside* this frame is filled with a different color (blue in the examples).
    *   The corners where the frame lines intersect retain the frame color.

*   **YAML Facts:**
    
```yaml
    task_description: Draw a frame based on the coordinates of two marker pixels and fill the interior.
    
    elements:
      - element: background
        color: white (0)
        role: static backdrop
      - element: marker_pixels
        count: 2
        color: non-white (red/2 in examples)
        role: define bounding box coordinates
      - element: frame_lines
        color: same as marker_pixels (red/2 in examples)
        role: form the boundary in the output
        location:
          horizontal: at the rows of the marker_pixels
          vertical: at the columns of the marker_pixels
      - element: fill_area
        color: blue (1)
        shape: rectangle
        role: fill the interior of the frame
        location: bounded by frame_lines (exclusive)
    
    relationships:
      - The locations (row, column) of the two marker_pixels in the input define the minimum and maximum rows and columns for the frame_lines in the output.
      - The color of the marker_pixels determines the color of the frame_lines.
      - The fill_area is always blue (1) and occupies the grid cells strictly between the minimum and maximum rows and columns defined by the marker_pixels.
    
    transformation:
      - Identify the coordinates (r1, c1) and (r2, c2) and color (marker_color) of the two non-white pixels in the input.
      - Determine min_row, max_row, min_col, max_col from these coordinates.
      - Create an output grid of the same size, initialized to white (0).
      - Draw horizontal lines with marker_color at min_row and max_row across the full grid width.
      - Draw vertical lines with marker_color at min_col and max_col across the full grid height.
      - Fill the rectangle from (min_row + 1, min_col + 1) to (max_row - 1, max_col - 1) with blue (1).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, but set all pixel values to white (0).
    2.  Find the row and column coordinates of the two non-white pixels in the input grid. Let these coordinates be (row1, col1) and (row2, col2). Record the color of these pixels (marker\_color).
    3.  Determine the minimum row (`min_row`), maximum row (`max_row`), minimum column (`min_col`), and maximum column (`max_col`) from these two coordinates.
    4.  In the output grid, draw a horizontal line using `marker_color` across the entire width at row `min_row`.
    5.  In the output grid, draw a horizontal line using `marker_color` across the entire width at row `max_row`.
    6.  In the output grid, draw a vertical line using `marker_color` down the entire height at column `min_col`.
    7.  In the output grid, draw a vertical line using `marker_color` down the entire height at column `max_col`.
    8.  Fill the rectangular region within the output grid, starting from row `min_row + 1` up to (but not including) `max_row`, and starting from column `min_col + 1` up to (but not including) `max_col`, with the color blue (1). Ensure the frame lines drawn in steps 4-7 are not overwritten by this fill.