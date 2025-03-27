*   **Perception**
    *   The input grids contain a white background (0) and one or more simple, monochromatic, horizontally oriented shapes (rectangles or lines) made of colors like green (3), yellow (4), or orange (7).
    *   The output grids retain the shapes from the input but shifted one column to the left.
    *   Any part of a shape that would shift beyond the left edge (column index < 0) is removed.
    *   All pixels in the output grid that are not part of a shifted shape become gray (5). This includes pixels that were originally white and pixels that were part of a shape before the shift but are now empty due to the shift.
    *   The dimensions of the output grid are identical to the input grid.

*   **Facts**
    
```yaml
    elements:
      - type: grid
        description: Input and output are 2D grids of pixels with integer values representing colors.
      - type: background
        input_color: white (0)
        output_color: gray (5)
        description: The background color changes from white in the input to gray in the output, filling any space not occupied by the shifted foreground objects.
      - type: object
        description: Contiguous pixels of any color other than white (0). In the examples, these are horizontal rectangles/lines.
        properties:
          - color: The specific color of the object (e.g., green, yellow, orange).
          - position: Coordinates (row, column) of each pixel constituting the object.
    actions:
      - name: shift_left
        target: object
        parameter: 1 column
        description: Each non-white pixel's column index is decremented by 1.
      - name: clip_boundary
        target: object
        condition: If a shifted pixel's column index becomes less than 0.
        effect: The pixel is removed from the output grid (not drawn).
      - name: fill_background
        target: grid cells
        condition: Cells in the output grid not occupied by a shifted object pixel.
        effect: Set the cell's color to gray (5).
    relationships:
      - The position of objects in the output depends directly on their position in the input via the left shift.
      - The final color of any pixel in the output grid is determined by whether a non-white pixel from the input shifts into that position; otherwise, it becomes gray.
    ```


*   **Natural Language Program**
    1.  Create a new output grid with the same dimensions as the input grid, initialized entirely with gray (5) pixels.
    2.  Iterate through each pixel (cell) of the input grid at `(row, column)` with color `C`.
    3.  If the color `C` is *not* white (0):
        a.  Calculate the target column index: `target_column = column - 1`.
        b.  If `target_column` is greater than or equal to 0 (i.e., within the grid's left boundary):
            i.  Set the pixel at `(row, target_column)` in the output grid to color `C`.
    4.  Return the completed output grid.