**Perception:**

1.  **Input/Output Size:** The input is an H x W grid. The output is always a 2H x 2W grid. In the examples, the input is 5x5 and the output is 10x10.
2.  **Output Structure:** The output grid appears to be composed of four quadrants, each the size of the input grid (H x W).
3.  **Top-Left Quadrant:** This quadrant is an identical copy of the input grid.
4.  **Other Quadrants:** The remaining three quadrants (Top-Right, Bottom-Left, Bottom-Right) are filled based on derived properties of the input grid's rows and columns.
5.  **Row/Column Property:** For each row and column in the input grid, a single "characteristic color" is determined. This color seems to be the most frequent non-white (non-zero) color within that row or column.
6.  **Tie-Breaking:** If multiple non-white colors share the highest frequency in a row or column, the characteristic color is the one that appears first (at the lowest index) in that row or column.
7.  **All-White Case:** If a row or column contains only white (zero) pixels, its characteristic color defaults to the characteristic color of the *first* row (for rows) or the *first* column (for columns).
8.  **Top-Right Quadrant Filling:** Each column `j` in the Top-Right quadrant is filled entirely with the characteristic color `C_j` derived from the corresponding column `j` of the input grid.
9.  **Bottom-Left Quadrant Filling:** Each row `i` in the Bottom-Left quadrant is filled entirely with the characteristic color `R_i` derived from the corresponding row `i` of the input grid.
10. **Bottom-Right Quadrant Filling:** The color of a cell at relative coordinates `(i, j)` within the Bottom-Right quadrant depends on the characteristic row color `R_i` and the characteristic column color `C_j`. Specifically, the cell color is `R_i` if the row index `i` is greater than or equal to the column index `j` (`i >= j`), and it is `C_j` otherwise (`i < j`).

**Facts YAML:**


```yaml
input_grid:
  type: 2D array of integers (colors)
  properties:
    height: H
    width: W
output_grid:
  type: 2D array of integers (colors)
  properties:
    height: 2 * H
    width: 2 * W
    structure: Composed of 4 quadrants (TL, TR, BL, BR), each H x W.
transformation:
  - step: Define Quadrants
    description: Divide the output grid into four HxW quadrants.
  - step: Populate Top-Left (TL) Quadrant
    action: Copy
    source: input_grid
    target: output_grid[0:H, 0:W]
  - step: Calculate Characteristic Colors
    description: Determine a characteristic color for each row and column of the input_grid.
    variables:
      R: list of H characteristic row colors
      C: list of W characteristic column colors
    logic:
      for_each: row i in input_grid
        non_white_colors: Filter out white (0) pixels.
        if non_white_colors is empty:
          R[i] = R[0] # Default to first row's characteristic color
        else:
          frequencies: Count occurrences of each non_white_color.
          max_frequency: Find the maximum count.
          candidates: List colors with max_frequency.
          if candidates count is 1:
            R[i] = the single candidate color
          else: # Tie-breaking
            R[i] = the candidate color that appears first (lowest index) in the original row i.
      for_each: column j in input_grid
        non_white_colors: Filter out white (0) pixels.
        if non_white_colors is empty:
          C[j] = C[0] # Default to first column's characteristic color
        else:
          frequencies: Count occurrences of each non_white_color.
          max_frequency: Find the maximum count.
          candidates: List colors with max_frequency.
          if candidates count is 1:
            C[j] = the single candidate color
          else: # Tie-breaking
            C[j] = the candidate color that appears first (lowest index) in the original column j.
    dependencies: R[0] and C[0] must be calculated first or handled during iteration.
  - step: Populate Top-Right (TR) Quadrant
    target: output_grid[0:H, W:2*W]
    logic:
      for_each: column j (0 to W-1)
        fill column j of TR quadrant with color C[j]
  - step: Populate Bottom-Left (BL) Quadrant
    target: output_grid[H:2*H, 0:W]
    logic:
      for_each: row i (0 to H-1)
        fill row i of BL quadrant with color R[i]
  - step: Populate Bottom-Right (BR) Quadrant
    target: output_grid[H:2*H, W:2*W]
    logic:
      for_each: cell at relative coordinates (i, j) within the BR quadrant (0 <= i < H, 0 <= j < W)
        if i >= j:
          set cell color to R[i]
        else:
          set cell color to C[j]

```


**Natural Language Program:**

1.  Create a new grid (the output) that is twice the height and twice the width of the input grid.
2.  Copy the input grid directly into the top-left quadrant of the output grid.
3.  Determine the characteristic color for each row of the input grid:
    a.  For a given row, identify all non-white pixels.
    b.  Count the occurrences of each non-white color.
    c.  Find the color(s) that occur most frequently.
    d.  If one color is most frequent, that is the characteristic color for the row.
    e.  If there's a tie for the most frequent color, the characteristic color is the tied color that appears earliest (leftmost) in the row.
    f.  If a row contains only white pixels, its characteristic color is the same as the characteristic color calculated for the first row. Store these row characteristic colors (e.g., in a list `R`).
4.  Determine the characteristic color for each column of the input grid using the same logic as in step 3, but applied to columns: check frequencies, break ties by choosing the topmost color, and default to the first column's characteristic color if a column is all white. Store these column characteristic colors (e.g., in a list `C`).
5.  Fill the top-right quadrant of the output grid: For each column index `j` (from 0 to width-1), fill the entire corresponding column in the top-right quadrant with the characteristic color `C[j]`.
6.  Fill the bottom-left quadrant of the output grid: For each row index `i` (from 0 to height-1), fill the entire corresponding row in the bottom-left quadrant with the characteristic color `R[i]`.
7.  Fill the bottom-right quadrant of the output grid: For each cell in this quadrant, let its row index within the quadrant be `i` and its column index be `j`. If `i` is greater than or equal to `j`, set the cell's color to `R[i]`. Otherwise (if `i` is less than `j`), set the cell's color to `C[j]`.