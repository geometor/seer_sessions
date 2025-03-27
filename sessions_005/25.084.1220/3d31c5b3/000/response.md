*   **Perception:**
    *   The input grid is always 12 rows by 6 columns.
    *   The output grid is always 3 rows by 6 columns.
    *   The input grid appears to be composed of four distinct 3x6 subgrids stacked vertically.
    *   The top subgrid (rows 0-2) contains primarily Gray (5) pixels mixed with White (0).
    *   The second subgrid (rows 3-5) contains primarily Yellow (4) pixels mixed with White (0).
    *   The third subgrid (rows 6-8) contains primarily Red (2) pixels mixed with White (0).
    *   The bottom subgrid (rows 9-11) contains primarily Azure (8) pixels mixed with White (0).
    *   The output grid seems to be a composite or overlay of these four input subgrids.
    *   For any given position (row, col) in the output grid, the color appears to be determined by the color found at the corresponding positions in the input subgrids: (row, col), (row+3, col), (row+6, col), and (row+9, col).
    *   The rule for combining seems to be based on priority: the color from the highest subgrid (topmost) takes precedence if it is not white. If the color in the top subgrid is white, the color from the second subgrid is checked, and so on, moving downwards. If all corresponding cells in the four subgrids are white, the output cell is white.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensions:
      input:
        height: 12
        width: 6
      output:
        height: 3
        width: 6
    input_structure:
      type: composite
      components:
        - subgrid_1:
            rows: 0-2
            cols: 0-5
            primary_color: 5 (Gray)
            background_color: 0 (White)
        - subgrid_2:
            rows: 3-5
            cols: 0-5
            primary_color: 4 (Yellow)
            background_color: 0 (White)
        - subgrid_3:
            rows: 6-8
            cols: 0-5
            primary_color: 2 (Red)
            background_color: 0 (White)
        - subgrid_4:
            rows: 9-11
            cols: 0-5
            primary_color: 8 (Azure)
            background_color: 0 (White)
    transformation:
      type: overlay_with_priority
      priority_order: top_to_bottom
      background_ignore: 0 (White)
      process: For each output cell at (row, col), determine its color by checking the corresponding input cells in sequence: input[row, col], input[row+3, col], input[row+6, col], input[row+9, col]. The output color is the color of the first non-white cell encountered in this sequence. If all four cells are white, the output color is white.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the dimensions 3x6, filled with a default color (e.g., white/0).
    2.  Iterate through each cell of the output grid using its row index `r` (from 0 to 2) and column index `c` (from 0 to 5).
    3.  For the current output cell (`r`, `c`), examine the corresponding cell in the first input subgrid at `input[r, c]`.
    4.  If the color at `input[r, c]` is not white (0), set the output cell `output[r, c]` to this color and proceed to the next output cell.
    5.  If the color at `input[r, c]` is white (0), examine the corresponding cell in the second input subgrid at `input[r + 3, c]`.
    6.  If the color at `input[r + 3, c]` is not white (0), set the output cell `output[r, c]` to this color and proceed to the next output cell.
    7.  If the color at `input[r + 3, c]` is white (0), examine the corresponding cell in the third input subgrid at `input[r + 6, c]`.
    8.  If the color at `input[r + 6, c]` is not white (0), set the output cell `output[r, c]` to this color and proceed to the next output cell.
    9.  If the color at `input[r + 6, c]` is white (0), examine the corresponding cell in the fourth input subgrid at `input[r + 9, c]`.
    10. Set the output cell `output[r, c]` to the color found at `input[r + 9, c]` (this color will be used whether it's white or not, as it's the last option).
    11. After iterating through all output cells, return the completed output grid.