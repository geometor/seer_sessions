*   **Perception:**
    *   The task operates on 2D grids containing numerical values (colors). The background is typically color 0.
    *   Each input grid contains, besides the background color 0, two other distinct non-zero colors.
    *   One non-zero color appears significantly more frequently than the other in the input grid. This suggests identifying a 'dominant' non-zero color based on count.
    *   The other non-zero color(s) act as 'minority' colors.
    *   The transformation rule involves filtering the grid based on color dominance and spatial relationships (connectivity).
    *   Specifically, all minority colors are removed (replaced by 0).
    *   The dominant color is kept only if a cell containing it is orthogonally adjacent (shares a side - up, down, left, or right) to at least one other cell also containing the dominant color. Isolated cells of the dominant color are also removed (replaced by 0).

*   **Facts:**
    
```yaml
    task_elements:
      - item: grid
        properties:
          - type: 2D array of integers (colors)
          - background_color: 0
          - contains_multiple_non_zero_colors
      - item: cell
        properties:
          - location: (row, column)
          - value: integer (color)
      - item: color
        properties:
          - value: integer
          - frequency: count in the grid
          - role: [dominant, minority, background]
      - item: dominant_color
        derivation: the non-zero color with the highest frequency in the input grid
      - item: minority_color
        derivation: any non-zero color that is not the dominant color
      - item: orthogonal_adjacency
        definition: Two cells share an edge (not just a corner).
      - item: isolated_cell
        definition: A cell containing the dominant color with no orthogonally adjacent neighbors also containing the dominant color.
    
    transformation:
      - action: identify_colors
        inputs: input_grid
        outputs: set_of_non_zero_colors
      - action: count_frequencies
        inputs: input_grid, set_of_non_zero_colors
        outputs: color_frequencies
      - action: determine_dominant_color
        inputs: color_frequencies
        outputs: dominant_color
      - action: initialize_output_grid
        properties: same dimensions as input_grid, filled with background_color (0)
      - action: filter_grid
        steps:
          - iterate through each cell (r, c) of the input_grid
          - get current_color = input_grid[r, c]
          - if current_color == dominant_color:
            - check orthogonal neighbors (r-1, c), (r+1, c), (r, c-1), (r, c+1) within grid bounds
            - if any orthogonal neighbor also contains dominant_color:
              - set output_grid[r, c] = dominant_color
          # Implicitly, all other cells (minority colors, isolated dominant colors, background) remain 0 in the output grid
    ```


*   **Natural Language Program:**
    1.  Analyze the input grid to identify all unique non-zero colors present.
    2.  Count the frequency of occurrence for each unique non-zero color.
    3.  Determine the 'dominant' color, which is the non-zero color with the highest frequency. All other non-zero colors are 'minority' colors.
    4.  Create a new output grid of the same dimensions as the input grid, initially filled entirely with the background color (0).
    5.  Iterate through each cell of the input grid at location (row, column).
    6.  Let the color in the current input cell be `current_color`.
    7.  If `current_color` is the identified dominant color:
        a.  Examine its orthogonal neighbors (up, down, left, right).
        b.  Check if at least one of these orthogonal neighbors in the *input* grid also contains the dominant color.
        c.  If such a neighbor exists (i.e., the current cell is not isolated), set the cell at (row, column) in the *output* grid to the dominant color.
    8.  If the `current_color` is not the dominant color (i.e., it's a minority color or the background color 0), or if it is the dominant color but is isolated (no orthogonal neighbors with the dominant color), the corresponding cell in the output grid retains its initial background color (0).
    9.  Return the completed output grid.