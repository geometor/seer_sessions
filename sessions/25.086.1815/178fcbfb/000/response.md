*   **Perception:**
    *   The input grids are sparsely populated with colored pixels (Blue, Red, Green) on a white background.
    *   The output grids have the same dimensions as the corresponding input grids.
    *   The output grids consist of solid horizontal or vertical lines of color on a white background.
    *   The color and position of the lines in the output seem directly related to the color and position of the pixels in the input.
    *   Specifically, Red pixels in the input correspond to vertical Red lines in the output, positioned at the same column index.
    *   Blue and Green pixels in the input correspond to horizontal lines of their respective colors in the output, positioned at the same row index.
    *   Lines extend across the full width or height of the grid.
    *   If multiple input pixels specify the same line (e.g., two green pixels in the same row), only one line appears in the output.

*   **Facts:**
    
```yaml
    task_type: drawing
    input_features:
      - Sparse colored pixels (objects) on a white background.
      - Colors observed: Blue (1), Red (2), Green (3).
      - Position (row, column) of each colored pixel is significant.
    output_features:
      - Dense colored lines (horizontal or vertical) on a white background.
      - Colors observed: Blue (1), Red (2), Green (3).
      - Position (row or column) of each line is significant.
      - Lines span the entire grid dimension (width for horizontal, height for vertical).
    transformation:
      - Each non-white pixel in the input grid acts as a specification for a line in the output grid.
      - The color of the input pixel determines the color of the output line.
      - The color of the input pixel determines the orientation of the output line:
          - Red (2) -> Vertical line
          - Blue (1) -> Horizontal line
          - Green (3) -> Horizontal line
      - The position of the input pixel determines the position of the output line:
          - For Red pixels: The column index of the input pixel determines the column index of the vertical output line.
          - For Blue/Green pixels: The row index of the input pixel determines the row index of the horizontal output line.
      - The output grid is initialized as all white.
      - Lines are drawn based on the identified input pixel specifications. Overlapping specifications (multiple pixels defining the same line) result in a single line.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
    2.  Iterate through each pixel in the input grid.
    3.  If an input pixel is Red (2):
        *   Identify its column index.
        *   Draw a vertical line of Red pixels (2) in the output grid at that column index, spanning the entire height of the grid.
    4.  If an input pixel is Blue (1):
        *   Identify its row index.
        *   Draw a horizontal line of Blue pixels (1) in the output grid at that row index, spanning the entire width of the grid.
    5.  If an input pixel is Green (3):
        *   Identify its row index.
        *   Draw a horizontal line of Green pixels (3) in the output grid at that row index, spanning the entire width of the grid.
    6.  Return the modified output grid.