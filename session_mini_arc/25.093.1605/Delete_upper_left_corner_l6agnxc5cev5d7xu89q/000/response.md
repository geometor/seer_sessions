*   **Perception of Task Elements:**
    *   The task involves transforming a 5x5 grid of numbers.
    *   The grids contain two distinct numbers: 0 and 4.
    *   The number 4 appears to form shapes or clusters within the grid, while 0 represents the background.
    *   The transformation modifies the shapes formed by the number 4 by changing some 4s to 0s.
    *   The change seems localized, depending on the immediate neighborhood of each cell containing a 4.
    *   Specifically, cells with the value 4 that have a 0 to their North (above) and a 0 to their West (left) are changed to 0. Cells outside the grid boundaries are treated as 0.

*   **YAML Facts:**
    
```yaml
    grid_dimensions: 5x5
    cell_values:
      - 0 (background)
      - 4 (object)
    transformation: selective_removal
    objects:
      - type: cluster
        value: 4
        property: modified by transformation
    relationships:
      - type: adjacency
        direction: North (N)
        relevance: determines if a '4' cell changes
      - type: adjacency
        direction: West (W)
        relevance: determines if a '4' cell changes
    action:
      - type: conditional_change
        input_value: 4
        output_value: 0
        condition:
          - description: North neighbor is 0
          - description: West neighbor is 0
    boundary_condition: Cells outside the grid are treated as having a value of 0.
    ```


*   **Natural Language Program:**
    1.  Iterate through each cell of the input grid.
    2.  For each cell containing the value 4:
        a.  Check the value of the cell directly North (above). Treat cells outside the top boundary as 0.
        b.  Check the value of the cell directly West (left). Treat cells outside the left boundary as 0.
        c.  If *both* the North neighbor and the West neighbor have the value 0, change the current cell's value to 0 in the output grid.
        d.  Otherwise, keep the current cell's value as 4 in the output grid.
    3.  For each cell containing the value 0 in the input grid, keep its value as 0 in the output grid.
    4.  The resulting grid is the final output.