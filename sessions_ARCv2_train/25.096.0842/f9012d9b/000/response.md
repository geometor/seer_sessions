*   **Perception:** The task takes a square grid of single-digit integers as input and produces a smaller square grid of integers as output. The size of the output grid appears to depend on the size of the input grid. The content of the output grid seems related to a frequently occurring subgrid pattern within the input grid. Specifically, it looks like we need to find the most common square subgrid of a particular size, handle ties by location, and then potentially extract a portion of that subgrid based on the input grid's dimensions.

*   **Facts:**
    
```yaml
    task: find_most_frequent_subgrid_pattern
    
    objects:
      - input_grid:
          type: 2D array of integers
          properties:
            - dimension (Dim): size of one side (e.g., 4 for 4x4)
            - cells: contain single-digit integers
      - subgrid:
          type: 2D array of integers
          properties:
            - dimension (M): size determined by floor(sqrt(Dim))
            - pattern: the specific values within the subgrid
            - location: top-left (row, col) index within the input_grid
            - frequency: count of occurrences of the pattern in the input_grid
            - index_sum: sum of the row and column index of the location
      - output_grid:
          type: 2D array of integers
          properties:
            - dimension (N): size determined by M and Dim's parity (N=M//2 if Dim is even, N=M if Dim is odd)
            - content: derived from the selected most frequent subgrid pattern
    
    actions:
      - calculate_subgrid_dimension (M): compute floor(sqrt(input_grid.dimension))
      - extract_subgrids: find all M x M subgrids within the input_grid
      - count_frequencies: determine how many times each unique M x M pattern occurs
      - find_max_frequency: identify the highest frequency count
      - filter_most_frequent: select all subgrid patterns that have the max_frequency
      - select_target_pattern (P):
          if only one pattern has max_frequency: select it
          if multiple patterns have max_frequency:
              find all occurrences (locations) for these patterns
              calculate index_sum (row + col) for each occurrence
              select the pattern associated with the occurrence having the maximum index_sum
              (tie-break further using max row index, then max col index if necessary)
      - calculate_output_dimension (N):
          if input_grid.dimension is even: N = M // 2
          if input_grid.dimension is odd: N = M
      - extract_output: take the top-left N x N portion of the selected_target_pattern (P)
    
    relationships:
      - subgrids are parts of the input_grid
      - output_grid is derived from the selected_target_pattern (P)
      - output_grid.dimension depends on subgrid.dimension (M) and input_grid.dimension (Dim)
    ```


*   **Natural Language Program:**
    1.  Determine the dimension (`Dim`) of the input square grid.
    2.  Calculate the dimension (`M`) for the subgrid search window by taking the floor of the square root of `Dim`.
    3.  Identify all unique `M x M` subgrid patterns present in the input grid and count the frequency of each pattern. Record the top-left location(s) (row, col) for each occurrence of every pattern.
    4.  Find the maximum frequency among all patterns.
    5.  Select the pattern(s) that occur with this maximum frequency.
    6.  If only one pattern has the maximum frequency, designate this pattern as `P`.
    7.  If multiple patterns share the maximum frequency, examine all occurrences (locations) of these tied patterns. Calculate the sum of indices (row + col) for each occurrence. Select the pattern (`P`) corresponding to the occurrence with the highest index sum. (If there's still a tie in index sums, choose the one with the highest row index; if still tied, choose the one with the highest column index).
    8.  Determine the dimension (`N`) of the output grid: if `Dim` (the input dimension) is even, set `N = M // 2`; otherwise (if `Dim` is odd), set `N = M`.
    9.  Construct the output grid by taking the top-left `N x N` portion of the selected pattern `P`.