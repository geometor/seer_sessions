*   **Perception of task elements:**
    *   The input is a grid (2D array) of single-digit integers. The grid dimensions vary across examples (4x4, 3x3, 5x5).
    *   The output is consistently a 2x2 grid of single-digit integers.
    *   The output grid appears to be a subgrid extracted from the input grid.
    *   The specific 2x2 subgrid selected seems to depend on the dimensions of the input grid. In examples 2 and 3 (3x3 and 5x5 inputs), the output is the top-left 2x2 corner. In example 1 (4x4 input), the output is the 2x2 subgrid formed by the first two rows and the last two columns.

*   **Facts YAML:**
    
```yaml
    task_description: Extract a specific 2x2 subgrid from an input grid, where the location of the subgrid depends on the input grid's dimensions.
    input:
      type: grid
      description: A 2D array of single-digit integers.
      properties:
        rows: variable integer (e.g., 3, 4, 5)
        columns: variable integer (e.g., 3, 4, 5)
        elements: single-digit integers (0-9)
    output:
      type: grid
      description: A 2x2 subgrid extracted from the input grid.
      properties:
        rows: 2
        columns: 2
        elements: single-digit integers from the input grid.
    transformation:
      process: Subgrid extraction based on input dimensions.
      steps:
        - step: Determine input grid dimensions (num_rows, num_cols).
        - step: Check if num_rows == 4 and num_cols == 4.
        - step:
            condition: If dimensions are 4x4.
            action: Extract the subgrid using row indices [0, 1] and column indices [2, 3].
        - step:
            condition: If dimensions are not 4x4.
            action: Extract the subgrid using row indices [0, 1] and column indices [0, 1].
      relationships:
        - The output grid elements are a subset of the input grid elements.
        - The output grid always consists of elements from the first two rows of the input grid.
        - The selected columns depend specifically on whether the input grid is 4x4 or not.
    ```


*   **Natural Language Program:**
    1.  Read the input grid and determine its dimensions (number of rows R and columns C).
    2.  If the input grid dimensions are R=4 and C=4:
        a.  Select the subgrid corresponding to rows 0 and 1, and columns 2 and 3.
    3.  Otherwise (if the input grid dimensions are not 4x4):
        a.  Select the subgrid corresponding to rows 0 and 1, and columns 0 and 1 (the top-left 2x2 corner).
    4.  Output the selected 2x2 subgrid.