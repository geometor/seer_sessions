*   **Perception:** The input grids contain three distinct non-white pixels (Yellow - 4, Red - 2, Green - 3) scattered on a white background (0). The output grids retain these three pixels in their original positions but add gray (5) pixels. The added gray pixels form a rectangular path that connects the areas around the original three colored pixels.

*   **Analysis:** Upon closer inspection, the gray pixels consistently form the perimeter of the smallest rectangle (bounding box) that encloses the initial three non-white pixels. The original three colored pixels remain in their positions; if one of these pixels lies on the perimeter of the bounding box, that specific cell retains its original color, and the gray perimeter "skips" that cell.

*   **YAML Facts:**
    
```yaml
    task_description: Draw the perimeter of the bounding box containing the three non-white pixels.
    grid_properties:
      size: Variable, 13x13 in examples.
      background_color: white (0)
    objects:
      - type: pixel
        color: yellow (4)
        count: 1
        role: marker_point_1
      - type: pixel
        color: red (2)
        count: 1
        role: marker_point_2
      - type: pixel
        color: green (3)
        count: 1
        role: marker_point_3
    actions:
      - name: find_marker_pixels
        description: Identify the coordinates of the single yellow, red, and green pixels.
      - name: calculate_bounding_box
        description: Determine the minimum and maximum row and column indices that encompass the three marker pixels.
        inputs: coordinates of marker pixels
        outputs: min_row, max_row, min_col, max_col
      - name: draw_perimeter
        description: Iterate through the cells forming the perimeter of the calculated bounding box.
        inputs: min_row, max_row, min_col, max_col, input_grid
        outputs: modified_grid
        details:
          - For cells on the top edge (min_row, min_col to max_col), bottom edge (max_row, min_col to max_col), left edge (min_col, min_row+1 to max_row-1), and right edge (max_col, min_row+1 to max_row-1):
          - If the cell in the input grid is white (0), change it to gray (5).
          - If the cell in the input grid is one of the original marker pixels (yellow, red, or green), leave it unchanged.
    relationships:
      - The gray pixels form the perimeter of the bounding box defined by the three initial colored pixels.
      - The original colored pixels are preserved and are not overwritten by the gray perimeter.
    output_grid_generation:
      - Start with a copy of the input grid.
      - Perform the draw_perimeter action.
      - The result is the output grid.

    ```


*   **Natural Language Program:**
    1.  Identify the locations (row, column) of the unique yellow (4), red (2), and green (3) pixels in the input grid.
    2.  Determine the minimum and maximum row indices (`min_row`, `max_row`) and the minimum and maximum column indices (`min_col`, `max_col`) among these three locations. This defines the bounding box.
    3.  Create a copy of the input grid to serve as the output grid.
    4.  Iterate through the cells along the perimeter of the bounding box:
        *   Top edge: For `col` from `min_col` to `max_col`, consider the cell (`min_row`, `col`).
        *   Bottom edge: For `col` from `min_col` to `max_col`, consider the cell (`max_row`, `col`).
        *   Left edge: For `row` from `min_row + 1` to `max_row - 1`, consider the cell (`row`, `min_col`).
        *   Right edge: For `row` from `min_row + 1` to `max_row - 1`, consider the cell (`row`, `max_col`).
    5.  For each perimeter cell identified in step 4, check its color in the *original* input grid. If the cell's color is white (0), change its color in the *output* grid to gray (5). Otherwise (if it's one of the original yellow, red, or green pixels), leave the cell unchanged in the output grid.
    6.  Return the modified output grid.