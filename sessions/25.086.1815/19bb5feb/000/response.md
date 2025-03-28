*   **Perception:** The input grids consist of a large white (0) background. Inside this background, there's a rectangular region primarily filled with azure (8) pixels. Embedded within this azure region are several distinct 2x2 squares, each made of a single color other than white (0) or azure (8). The output is a small 2x2 grid that represents the colors and relative positions of these embedded 2x2 squares.

*   **YAML Facts:**
    
```yaml
    task_description: Identify 2x2 colored squares within a larger azure region and map their relative quadrant positions to a 2x2 output grid.

    elements:
      - element: background
        color: white (0)
      - element: container
        color: azure (8)
        shape: rectangle
        description: Contains smaller colored squares. Its boundaries define the area of interest.
      - element: colored_squares
        shape: 2x2 square
        color: Any color except white (0) or azure (8)
        location: Embedded within the azure container.
        quantity: Variable (0 to 4 per input).

    relationships:
      - type: containment
        parent: container (azure rectangle)
        children: colored_squares
      - type: relative_position
        reference: center of the azure container
        objects: colored_squares
        description: Each colored square's position relative to the center determines its quadrant (top-left, top-right, bottom-left, bottom-right).

    transformation:
      input: grid with background, azure container, and embedded colored squares.
      output: 2x2 grid.
      mapping:
        - rule: Map the color of the colored square found in the top-left quadrant of the azure container to the top-left cell of the output grid. If no square exists in that quadrant, use white (0).
        - rule: Map the color of the colored square found in the top-right quadrant of the azure container to the top-right cell of the output grid. If no square exists in that quadrant, use white (0).
        - rule: Map the color of the colored square found in the bottom-left quadrant of the azure container to the bottom-left cell of the output grid. If no square exists in that quadrant, use white (0).
        - rule: Map the color of the colored square found in the bottom-right quadrant of the azure container to the bottom-right cell of the output grid. If no square exists in that quadrant, use white (0).
      ignored_elements:
        - background (white)
        - container (azure)

    output_grid:
      size: 2x2
      cell_values: Colors of the identified squares based on their quadrant, or white (0) if a quadrant is empty.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty 2x2 output grid, filled with white (0).
    2.  Identify the bounding box of the azure (8) colored region in the input grid. Determine its minimum and maximum row and column indices.
    3.  Calculate the center coordinates (center_row, center_col) of the azure bounding box.
    4.  Iterate through the input grid to find all distinct 2x2 squares composed of a single color, excluding white (0) and azure (8). Record the color and the top-left coordinate (r, c) of each found square.
    5.  For each found colored 2x2 square with top-left coordinate (r, c) and color `C`:
        a.  If `r < center_row` and `c < center_col` (Top-Left quadrant), set the output grid cell at `[0, 0]` to color `C`.
        b.  If `r < center_row` and `c >= center_col` (Top-Right quadrant), set the output grid cell at `[0, 1]` to color `C`.
        c.  If `r >= center_row` and `c < center_col` (Bottom-Left quadrant), set the output grid cell at `[1, 0]` to color `C`.
        d.  If `r >= center_row` and `c >= center_col` (Bottom-Right quadrant), set the output grid cell at `[1, 1]` to color `C`.
    6.  Return the final 2x2 output grid.