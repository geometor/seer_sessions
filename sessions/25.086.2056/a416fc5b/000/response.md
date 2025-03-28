*   **Perception:**
    *   The input grids are 11x11 and contain orange (7), magenta (6), and sometimes red (2) pixels.
    *   Magenta lines (color 6) form a grid structure, dividing the 11x11 grid into nine 3x3 areas separated by single rows/columns of magenta. The magenta lines are at rows 3 and 7, and columns 3 and 7.
    *   Within some of the 3x3 areas defined by the magenta lines, there are 'plus' shapes made of red (2) pixels centered in the 3x3 area. The plus shape is `[[7, 2, 7], [2, 7, 2], [7, 2, 7]]`. The remaining cells in these 3x3 areas are orange (7).
    *   The transformation rule appears to depend critically on the *number* of red plus shapes present in the input grid.
    *   In examples `train_1` and `train_2`, there are exactly two red plus shapes. The output grid is the same size (11x11). The magenta lines and the red plus shapes are preserved. Two of the 3x3 areas that originally contained only orange pixels are modified with new patterns involving gray (5) or azure (8) pixels, replacing the orange background. The specific locations modified and the patterns used (gray or azure) seem to depend on the locations of the initial two red plus shapes.
        *   The gray pattern is `[[7, 5, 7], [5, 7, 5], [7, 5, 7]]`.
        *   The azure pattern is `[[7, 8, 7], [8, 7, 8], [7, 8, 7]]`.
    *   In example `train_3`, there are four red plus shapes. The output grid is drastically different: it's a 16x16 grid filled entirely with orange (7). This suggests a conditional rule based on the count of red shapes.

*   **Facts:**
    
```yaml
    grid_structure:
      type: partition
      divider_color: magenta (6)
      divider_rows: [3, 7]
      divider_cols: [3, 7]
      resulting_elements: nine 3x3 subgrids
      subgrid_coordinates: # top-left corner row, col
        - [0, 0]
        - [0, 4]
        - [0, 8]
        - [4, 0]
        - [4, 4]
        - [4, 8]
        - [8, 0]
        - [8, 4]
        - [8, 8]

    objects:
      - type: red_plus_shape
        color: red (2)
        shape: [[7, 2, 7], [2, 7, 2], [7, 2, 7]] # relative to its 3x3 subgrid
        location: centered within a 3x3 subgrid
      - type: orange_subgrid
        color: orange (7)
        shape: [[7, 7, 7], [7, 7, 7], [7, 7, 7]]
        location: fills a 3x3 subgrid

    patterns:
      - name: gray_pattern
        color: gray (5)
        shape: [[7, 5, 7], [5, 7, 5], [7, 5, 7]]
      - name: azure_pattern
        color: azure (8)
        shape: [[7, 8, 7], [8, 7, 8], [7, 8, 7]]

    conditions:
      - variable: num_red_plus_shapes
        value: count of red_plus_shape objects in the input grid

    actions:
      - type: conditional_transformation
        condition: num_red_plus_shapes != 2
        effect: output is a 16x16 grid filled with orange (7)
      - type: conditional_transformation
        condition: num_red_plus_shapes == 2
        effect:
          - preserve input grid structure (magenta lines, red plus shapes)
          - identify the two 3x3 subgrids containing red plus shapes (R1, R2)
          - identify the two specific empty (orange) 3x3 subgrids to modify (M1, M2) based on the locations of R1 and R2
          - apply gray_pattern to one modified subgrid (e.g., M1)
          - apply azure_pattern to the other modified subgrid (e.g., M2)
          - the specific mapping from {R1, R2} to {M1: gray/azure, M2: azure/gray} is determined by the examples:
              - If red pluses are in subgrids 5 and 8, modify subgrid 0 with gray_pattern and subgrid 2 with azure_pattern.
              - If red pluses are in subgrids 2 and 4, modify subgrid 3 with azure_pattern and subgrid 7 with gray_pattern.
              (Note: Subgrid indices 0-8, row-major starting top-left)
    ```


*   **Natural Language Program:**
    1.  Analyze the input 11x11 grid. Identify the nine 3x3 subgrids demarcated by the magenta (6) lines at rows 3, 7 and columns 3, 7.
    2.  Count the number of 3x3 subgrids that contain a centered red (2) plus shape. Let this count be `N`.
    3.  **If `N` is not equal to 2:**
        *   Construct a new 16x16 grid.
        *   Fill all cells of this new grid with orange (7).
        *   Return this 16x16 grid as the output.
    4.  **If `N` is equal to 2:**
        *   Create a copy of the input 11x11 grid; this will be the basis for the output grid.
        *   Identify the locations (indices 0-8, row-major) of the two subgrids containing the red plus shapes. Let this set of indices be `R`.
        *   Define the modification patterns: `P_gray = [[7, 5, 7], [5, 7, 5], [7, 5, 7]]` and `P_azure = [[7, 8, 7], [8, 7, 8], [7, 8, 7]]`.
        *   Determine the target subgrid indices and their patterns based on the set `R`:
            *   If `R` is `{5, 8}` (corresponding to subgrids at row 4, col 8 and row 8, col 8), then:
                *   Modify the subgrid at index 0 (row 0, col 0) by replacing its contents with `P_gray`.
                *   Modify the subgrid at index 2 (row 0, col 8) by replacing its contents with `P_azure`.
            *   If `R` is `{2, 4}` (corresponding to subgrids at row 0, col 8 and row 4, col 4), then:
                *   Modify the subgrid at index 3 (row 4, col 0) by replacing its contents with `P_azure`.
                *   Modify the subgrid at index 7 (row 8, col 4) by replacing its contents with `P_gray`.
        *   Return the modified 11x11 grid as the output.