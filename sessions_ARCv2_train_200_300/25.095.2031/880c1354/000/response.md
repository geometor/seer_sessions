*   **Perception of Task Elements:**
    *   The task involves transforming an 8x8 input grid of digits into an 8x8 output grid of digits.
    *   The transformation operates on a cell-by-cell basis, where the output value of a cell depends solely on the input value of that same cell.
    *   A consistent value substitution rule is applied across the entire grid for each input-output pair.
    *   The digits '4' and '7' appear to be invariant; they always map to themselves in the output.
    *   Other digits present in the input grid undergo a specific substitution. The exact substitution rule changes between the different training examples, but follows a pattern within each example (e.g., swaps or cycles).
        *   Example 1: `1->3, 2->6, 3->2, 6->1`
        *   Example 2: `1->9, 6->1, 9->6`
        *   Example 3: `5->6, 6->5`

*   **Facts:**
    
```yaml
    objects:
      - input_grid: 
          type: grid (8x8 matrix)
          properties:
            cells: contain integer digits (0-9)
      - output_grid:
          type: grid (8x8 matrix)
          properties:
            cells: contain integer digits (0-9)
      - substitution_map:
          type: mapping (dictionary-like)
          properties:
            keys: input digit values
            values: output digit values
            constraints: 
              - specific map varies per example
              - always includes {4: 4, 7: 7}
    actions:
      - apply_substitution:
          actor: system
          input: input_grid, substitution_map
          output: output_grid
          description: Iterates through each cell of the input_grid, finds the corresponding output value using the substitution_map, and places it in the output_grid.
    relationships:
      - cell_wise_transformation: The value of each cell in the output_grid is determined exclusively by the value of the corresponding cell in the input_grid and the substitution_map.
      - global_rule: The same substitution_map applies to all cells within a single input-output grid pair.
    ```


*   **Natural Language Program:**
    1.  Define a specific value substitution map based on the observed transformation for the given input-output pair. This map details how each input digit value transforms into an output digit value. Ensure the map includes the rules that '4' maps to '4' and '7' maps to '7'.
    2.  Create a new output grid with the same dimensions as the input grid.
    3.  Iterate through each cell of the input grid.
    4.  For the current cell, retrieve its digit value.
    5.  Use the defined substitution map to find the corresponding output digit value for the retrieved input value.
    6.  Place this output digit value into the corresponding cell of the new output grid.
    7.  After processing all cells, return the completed output grid.