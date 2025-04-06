*   **Perception:** The input is a 2D grid containing the digits 0 and 8. The digit 8 appears to represent foreground objects or active pixels, while 0 represents the background. Within the input grid, the 8s form distinct connected clusters or groups. The output is also a 2D grid, significantly smaller than the input, containing 0s and 8s. The output grid's structure is consistently an identity matrix pattern where the diagonal elements are 8 and off-diagonal elements are 0. The size of the output grid correlates directly with the number of distinct connected groups of 8s found in the input grid. Connectivity between 8s seems to include diagonal adjacency (8-connectivity).

*   **Facts:**
    
```yaml
    task: grid_transformation
    input:
      type: 2D_grid
      elements:
        - value: 0
          role: background
        - value: 8
          role: object_pixel
      properties:
        - object_pixels form connected_components (clusters) based on 8-way adjacency (including diagonals).
    output:
      type: 2D_grid
      elements:
        - value: 0
          role: background
        - value: 8
          role: diagonal_element
      properties:
        - dimensions: NxN, where N is the number of connected_components in the input.
        - structure: Identity matrix pattern scaled by 8 (8 on the main diagonal, 0 elsewhere).
    transformation:
      action: identify_connected_components
      parameters:
        - element_value: 8
        - connectivity: 8-way (Moore neighborhood)
      action: count_components
      result: N
      action: generate_output_grid
      parameters:
        - dimensions: N x N
        - fill_diagonal: 8
        - fill_off_diagonal: 0
    relationship: The size of the output grid is determined by the count of distinct connected components of '8' pixels in the input grid. The output grid visualizes this count as an NxN diagonal matrix using the digit 8.

    ```


*   **Natural Language Program:**
    1.  Identify all pixels in the input grid with the value 8.
    2.  Find all distinct connected components formed by these '8' pixels, considering two '8' pixels connected if they touch horizontally, vertically, or diagonally (8-way connectivity).
    3.  Count the total number of distinct connected components found (let this count be N).
    4.  Create a new output grid with dimensions N rows by N columns.
    5.  Initialize all cells in the output grid to 0.
    6.  Iterate from i = 0 to N-1: set the cell at row i, column i (the main diagonal) of the output grid to 8.
    7.  Return the generated NxN grid as the output.