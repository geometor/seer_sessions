*   **Perception:** The task involves transforming an input grid of numbers into an output grid. The input grids contain blocks of non-zero numbers, primarily located in the lower portion, surrounded by zeros. The output grids appear to be constructed by manipulating the rows containing non-zero elements from the input. Specifically, the transformation seems to involve identifying the block of rows containing non-zero values, reflecting this block vertically, and then appending the original block below the reflection.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_grid
        type: 2D array of integers
        properties:
          - contains zeros and single-digit non-zero integers
          - non-zero elements form a contiguous block in the lower rows
      - object: output_grid
        type: 2D array of integers
        properties:
          - derived from the input_grid
          - same width as input_grid
          - height is twice the height of the non-zero block in the input
      - object: active_block
        type: subgrid of input_grid
        definition: The set of rows starting from the first row containing any non-zero element down to the last row of the input grid.
        properties:
          - contains all non-zero elements of the input grid
    actions:
      - identify: find the first row index containing a non-zero element in the input grid.
      - extract: select the rows from the identified index to the end of the input grid to form the 'active_block'.
      - reverse: create a new block by reversing the order of rows in the 'active_block'.
      - concatenate: combine the reversed block and the original 'active_block' vertically.
    relationships:
      - The output grid is formed by the vertical concatenation of the reversed 'active_block' and the original 'active_block'.
      - The top half of the output grid is a vertical reflection of the bottom half.
      - The bottom half of the output grid is identical to the 'active_block' from the input grid.
    ```


*   **Natural Language Program:**
    1.  Examine the input grid row by row from top to bottom.
    2.  Identify the index of the first row that contains at least one non-zero number.
    3.  Extract all rows from this first non-zero row down to the last row of the input grid. Call this extracted subgrid the "active block".
    4.  Create a new grid, initially empty.
    5.  Take the rows of the "active block" and reverse their order. Append these reversed rows to the new grid.
    6.  Append the original rows of the "active block" (in their original order) to the new grid, below the reversed rows.
    7.  The resulting grid is the output.