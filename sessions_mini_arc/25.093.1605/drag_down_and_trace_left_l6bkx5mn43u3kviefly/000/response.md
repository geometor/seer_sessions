Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
Okay, analyzing the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids of integers, representing colored cells. The grid dimensions appear constant within each example pair (5x5 in all provided examples).
2.  **Colors Involved:** The grids use integers 0 (often black), 4 (often blue), and 5 (often red). 0 and 4 appear in the input, while 0, 4, and 5 appear in the output.
3.  **Core Change Trigger:** The presence of the number 0 in the input grid seems to be the trigger for changes in the output grid.
4.  **Transformation Pattern:**
    *   Cells that are 0 in the input are changed to 5 in the output.
    *   Cells that are directly below a 0 in the input are changed to 0 in the output, *regardless* of their original value in the input.
    *   This "change below to 0" rule seems to take precedence. If a cell is 0 (changed to 5) and the cell below it is also 0 (changed to 5), the effect from the *upper* 0 cell forces the *lower* cell to become 0 in the final output.
    *   Cells that are not 0 and are not directly below a 0 remain unchanged.

**Facts:**


```yaml
Grid:
  type: 2D array of integers
  properties:
    - height: integer
    - width: integer
    - cells: contain integer values (0, 4, 5)
Objects:
  - name: Cell
    properties:
      - value: Integer (0, 4, 5)
      - location: tuple (row_index, column_index)
      - is_zero_in_input: boolean
      - is_below_zero_in_input: boolean
Relationships:
  - type: Positional
    description: A cell at (r, c) has a cell 'below' it at (r+1, c), provided r+1 is within the grid bounds.
Actions:
  - name: FindZeroes
    input: input_grid
    output: list_of_zero_locations [(r, c), ...]
    description: Identify all coordinates where the input grid value is 0.
  - name: ApplyColorChange
    input: coordinate (r, c), output_grid
    output: modified_output_grid
    description: Change the value at output_grid[r, c] to 5.
  - name: ApplyBelowEffect
    input: coordinate (r, c), output_grid
    output: modified_output_grid
    description: If r+1 is a valid row index, change the value at output_grid[r+1, c] to 0.
RulePriority:
  description: The 'ApplyBelowEffect' (changing to 0) overrides the 'ApplyColorChange' (changing to 5) if a cell is both initially 0 and also below another 0.
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a direct copy of the `input_grid`.
2.  Create a list, `zero_locations`, containing the `(row, column)` coordinates of every cell in the `input_grid` that has a value of 
---
