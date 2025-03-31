*   **Perception:**
    *   The input is a square grid (5x5 in the examples).
    *   The output is a square grid with double the dimensions of the input (10x10 in the examples).
    *   The output grid is composed of four quadrants, each the size of the original input grid.
    *   The top-left and bottom-left quadrants of the output are identical copies of the input grid.
    *   The top-right and bottom-right quadrants of the output are modified versions of the input grid.
    *   The modification involves swapping two specific colors within the input grid pattern.
    *   To determine which colors are swapped, analyze the frequency of colors in the input grid. Identify the two colors that appear most frequently. These two colors are swapped in the modified quadrants. The color(s) with lower frequencies remain in their original positions in the modified quadrants.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      input_size: NxN (e.g., 5x5)
      output_size: 2Nx2N (e.g., 10x10)
    components:
      - input_grid: The original NxN grid.
      - output_grid: The resulting 2Nx2N grid.
      - output_quadrants: The output grid is divided into four NxN quadrants.
        - top_left_quadrant: (rows 0 to N-1, cols 0 to N-1)
        - top_right_quadrant: (rows 0 to N-1, cols N to 2N-1)
        - bottom_left_quadrant: (rows N to 2N-1, cols 0 to N-1)
        - bottom_right_quadrant: (rows N to 2N-1, cols N to 2N-1)
    transformation_rules:
      - rule_1:
          action: copy
          source: input_grid
          target: output_quadrants
          quadrants: [top_left_quadrant, bottom_left_quadrant]
          condition: none
      - rule_2:
          action: modify_and_copy
          source: input_grid
          target: output_quadrants
          quadrants: [top_right_quadrant, bottom_right_quadrant]
          modification:
            type: color_swap
            details:
              - step: count color frequencies in the input_grid.
              - step: identify the two colors with the highest frequencies (color_A, color_B).
              - step: create a modified grid by iterating through the input_grid. If a pixel is color_A, change it to color_B. If a pixel is color_B, change it to color_A. Keep all other colors the same.
              - result: Use this modified grid for the specified quadrants.
    relationships:
      - The output grid size is determined by doubling the input grid dimensions.
      - The content of the output quadrants depends on the input grid and a color frequency analysis.
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height H, width W) of the input grid.
    2.  Create a new output grid with dimensions 2H x 2W.
    3.  Copy the input grid directly into the top-left quadrant (rows 0 to H-1, columns 0 to W-1) of the output grid.
    4.  Copy the input grid directly into the bottom-left quadrant (rows H to 2H-1, columns 0 to W-1) of the output grid.
    5.  Analyze the input grid to count the occurrences of each color.
    6.  Identify the two colors with the highest frequencies. Let these be `color1` and `color2`.
    7.  Create a modified version of the input grid: Iterate through each pixel of the input grid. If the pixel's color is `color1`, set the corresponding pixel in the modified grid to `color2`. If the pixel's color is `color2`, set the corresponding pixel to `color1`. Otherwise, keep the original color.
    8.  Copy this modified grid into the top-right quadrant (rows 0 to H-1, columns W to 2W-1) of the output grid.
    9.  Copy this modified grid into the bottom-right quadrant (rows H to 2H-1, columns W to 2W-1) of the output grid.
    10. Return the completed output grid.