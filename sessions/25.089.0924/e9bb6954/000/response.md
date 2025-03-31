*   **Perception of task elements:**
    *   The input and output grids have the same dimensions.
    *   The input grid contains scattered pixels and distinct objects (contiguous blocks of the same color, excluding white).
    *   The output grid is the input grid modified by adding horizontal and vertical lines.
    *   The colors and positions of these lines seem related to the properties (color, size, position) of the largest object(s) in the input grid.
    *   Specifically, horizontal and vertical lines are drawn through the "center" of the largest objects.
    *   If multiple objects share the largest size, lines are drawn for each of them using their respective colors and centers.
    *   The lines only fill cells that were originally white (color 0) in the input grid; they do not overwrite existing non-white pixels.

*   **YAML facts:**
    
```yaml
    task_description: Modifies the input grid by adding horizontal and vertical lines based on the largest objects found within it.
    elements:
      - type: grid
        properties:
          - dimensions remain constant between input and output.
          - contains background pixels (white, 0).
          - contains objects (contiguous blocks of non-white pixels).
      - type: object
        properties:
          - color (non-white)
          - shape (contiguous pixels)
          - size (number of pixels)
          - location (coordinates)
          - bounding_box (min_row, min_col, max_row, max_col)
          - center (center_row, center_col based on bounding box)
    actions:
      - identify_objects: Find all contiguous blocks of non-white pixels (using 8-way adjacency).
      - calculate_size: Determine the area (pixel count) for each object.
      - find_max_size: Determine the maximum size among all identified objects.
      - filter_largest_objects: Select all objects whose size equals the maximum size.
      - calculate_center: For each largest object, calculate its center row and column based on its bounding box: center_row = floor((min_row + max_row) / 2), center_col = floor((min_col + max_col) / 2).
      - draw_lines: For each largest object:
          - Draw a horizontal line of the object's color across the grid at its center row.
          - Draw a vertical line of the object's color down the grid at its center column.
          - Important constraint: Lines only color cells that are white (0) in the grid. They do not overwrite existing non-white cells from the input or previously drawn lines.
    relationships:
      - The color of the drawn lines matches the color of the corresponding largest object.
      - The position (row/column) of the drawn lines corresponds to the calculated center of the corresponding largest object.
      - The modification (drawing lines) applies only to white background pixels.
    ```


*   **Natural language program:**
    1.  Start with a copy of the input grid.
    2.  Identify all distinct objects in the input grid. An object is a contiguous group of pixels of the same non-white color (using diagonal and cardinal adjacency). Ignore the white background (color 0).
    3.  Calculate the size (number of pixels) of each identified object.
    4.  Find the maximum size among all objects.
    5.  Identify all objects that have this maximum size. There might be one or more such objects.
    6.  For each object identified in step 5:
        a.  Note the object's color.
        b.  Determine the object's bounding box (the smallest rectangle containing all its pixels). Find the minimum row (`min_row`), maximum row (`max_row`), minimum column (`min_col`), and maximum column (`max_col`).
        c.  Calculate the center row index as `floor((min_row + max_row) / 2)`.
        d.  Calculate the center column index as `floor((min_col + max_col) / 2)`.
        e.  Iterate through all columns `c` from 0 to the grid width - 1. If the pixel at `(center_row, c)` in the current grid is white (0), change its color to the object's color.
        f.  Iterate through all rows `r` from 0 to the grid height - 1. If the pixel at `(r, center_col)` in the current grid is white (0), change its color to the object's color.
    7.  The resulting grid after processing all largest objects is the final output.