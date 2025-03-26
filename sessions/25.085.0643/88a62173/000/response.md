*   **Perception:**
    *   The input is always a 5x5 grid.
    *   The output is always a 2x2 grid.
    *   The input grids contain a central cross (row 2 and column 2) composed entirely of white pixels (0).
    *   This central cross divides the input grid into four distinct 2x2 quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR).
    *   Each input grid features one primary color besides white.
    *   The output grid is a direct copy of one of the four 2x2 quadrants from the input grid.
    *   The selection of which quadrant to copy seems based on the number of non-white pixels within each quadrant.

*   **Facts:**
    
```yaml
    task_structure:
      input_size: 5x5
      output_size: 2x2
      input_features:
        - type: grid_division
          description: A central white cross (row 2, column 2) divides the grid.
          resulting_elements:
            - name: Top-Left Quadrant (TL)
              location: rows 0-1, columns 0-1
              size: 2x2
            - name: Top-Right Quadrant (TR)
              location: rows 0-1, columns 3-4
              size: 2x2
            - name: Bottom-Left Quadrant (BL)
              location: rows 3-4, columns 0-1
              size: 2x2
            - name: Bottom-Right Quadrant (BR)
              location: rows 3-4, columns 3-4
              size: 2x2
        - type: color_composition
          description: Contains white pixels (0) and one other dominant color.
      output_derivation:
        source: One of the four input quadrants.
        selection_rule: Based on non-white pixel counts within quadrants.

    selection_logic:
      - step: 1
        action: count_non_white_pixels
        target: Each of the four quadrants (TL, TR, BL, BR).
        output: Four counts (C_TL, C_TR, C_BL, C_BR).
      - step: 2
        action: find_maximum_count
        input: The four counts.
        output: Maximum count value (max_c).
      - step: 3
        action: check_uniqueness
        input: max_c and the four counts.
        condition: If exactly one quadrant's count equals max_c.
        result_if_true: Select that quadrant as the output.
      - step: 4
        action: find_minimum_count
        input: The four counts.
        condition: If maximum count was not unique (step 3 failed).
        output: Minimum count value (min_c).
      - step: 5
        action: check_uniqueness
        input: min_c and the four counts.
        condition: If exactly one quadrant's count equals min_c.
        result_if_true: Select that quadrant as the output.
      - step: 6
        action: default_selection
        condition: If both maximum and minimum counts were not unique (implies all counts are equal).
        result: Select the Bottom-Right (BR) quadrant as the output.

    output_generation:
      action: copy_selected_quadrant
      description: The 2x2 output grid is a direct copy of the quadrant selected by the logic above.
    ```


*   **Natural Language Program:**
    1.  Identify the four 2x2 quadrants in the 5x5 input grid, separated by the central white row (row index 2) and central white column (column index 2). These quadrants are Top-Left (rows 0-1, cols 0-1), Top-Right (rows 0-1, cols 3-4), Bottom-Left (rows 3-4, cols 0-1), and Bottom-Right (rows 3-4, cols 3-4).
    2.  For each of the four quadrants, count the number of pixels that are not white (value is not 0).
    3.  Determine the maximum count among the four quadrants. If only one quadrant has this maximum count, select that quadrant.
    4.  If more than one quadrant shares the maximum count, then determine the minimum count among the four quadrants. If only one quadrant has this minimum count, select that quadrant.
    5.  If the counts are the same across all four quadrants (meaning neither the maximum nor the minimum count was unique), select the Bottom-Right quadrant.
    6.  The output grid is a 2x2 grid that is an exact copy of the selected quadrant.