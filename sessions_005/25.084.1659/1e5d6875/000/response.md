*   **Perception**:
    *   The input and output grids have the same dimensions (8x8 in the examples).
    *   The background color is orange (7).
    *   The input grids contain objects made of gray (5) and red (2) pixels.
    *   The output grids retain the original gray (5) and red (2) pixels in their exact locations.
    *   Some of the background orange (7) pixels in the input are changed to either yellow (4) or green (3) in the output.
    *   The changes seem related to the proximity of orange pixels to the gray and red pixels.
    *   Specifically, orange pixels adjacent (including diagonals) to gray pixels might change color, and orange pixels adjacent to red pixels might change color.
    *   In train\_1 output, yellow (4) appears next to the gray (5) object, and green (3) appears near both red (2) objects, and also in locations adjacent to both gray (5) and red (2).
    *   In train\_2 output, yellow (4) appears near the gray (5) objects, and green (3) appears near the red (2) objects, and also in locations adjacent to both gray (5) and red (2).
    *   It appears that adjacency to red (2) takes precedence or results in green (3), while adjacency *only* to gray (5) results in yellow (4).

*   **Facts**:
    
```yaml
    task_type: color_change_based_on_adjacency
    grid_properties:
      - background_color: 7  # orange
      - dimensions_preserved: true
    objects:
      - color: 5 # gray
        behavior: static
        role: influencer_1
      - color: 2 # red
        behavior: static
        role: influencer_2
    transformations:
      - type: conditional_color_change
        target_color: 7 # orange
        conditions:
          - name: near_red
            adjacency: 8_neighbors # includes diagonals
            adjacent_to_color: 2 # red
            output_color: 3 # green
          - name: near_gray_only
            adjacency: 8_neighbors # includes diagonals
            adjacent_to_color: 5 # gray
            not_adjacent_to_color: 2 # red
            output_color: 4 # yellow
        priority:
          - near_red # Condition 'near_red' takes precedence
          - near_gray_only
        default_color: 7 # orange (if no conditions met)
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each cell `(row, column)` of the input grid.
    3.  If the color of the cell `(row, column)` in the input grid is orange (7):
        a.  Check all 8 neighboring cells (including diagonals) of the current cell `(row, column)`.
        b.  Determine if any neighbor has the color red (2). Let this condition be `is_near_red`.
        c.  Determine if any neighbor has the color gray (5). Let this condition be `is_near_gray`.
        d.  If `is_near_red` is true, change the color of the cell `(row, column)` in the output grid to green (3).
        e.  Else if `is_near_gray` is true (meaning `is_near_red` must be false), change the color of the cell `(row, column)` in the output grid to yellow (4).
        f.  Otherwise (the cell is orange and is not near red or gray), the cell `(row, column)` in the output grid retains its original orange (7) color.
    4.  Leave all cells that were originally red (2) or gray (5) unchanged in the output grid.
    5.  Return the final output grid.