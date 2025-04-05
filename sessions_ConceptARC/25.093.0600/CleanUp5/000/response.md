Okay, I will analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) containing single-digit non-negative integers.
2.  **Grid Size:** The grid dimensions can vary between examples (6x21 in train\_1, 6x24 in train\_2), but the output grid always has the same dimensions as the corresponding input grid.
3.  **Values:** The grids contain the value 0 and other non-zero digits (2, 3 in train\_1; 4 in train\_2).
4.  **Transformation:** The core transformation involves selectively changing some non-zero digits in the input grid to 0 in the output grid. Other digits (including existing 0s and some non-zero digits) remain unchanged.
5.  **Pattern:**
    *   In `train_1`, all instances of the digit '3' are changed to '0', while all instances of '2' remain unchanged.
    *   In `train_2`, *some* instances of the digit '4' are changed to '0', while others remain '4'.
    *   Observing the positions, the non-zero digits that are changed to 0 appear to be those that do not have any adjacent cells (including diagonals - Moore neighborhood) containing the *same* non-zero digit. Conversely, non-zero digits that *do* have at least one neighbor with the same value are preserved in the output.

**YAML Facts:**


```yaml
task_description: "Filter a 2D grid of digits, setting non-zero digits to zero if they lack neighbors of the same value."
elements:
  - object: grid
    properties:
      - type: 2D array (matrix)
      - content: non-negative single digits
      - dimensionality: [rows, columns] (variable)
  - object: cell
    properties:
      - value: integer (0-9)
      - position: [row_index, column_index]
      - neighbors: set of 8 adjacent cells (Moore neighborhood)
relationships:
  - type: adjacency
    between: cell
    details: A cell is adjacent to up to 8 other cells (horizontally, vertically, diagonally). Boundary cells have fewer neighbors.
actions:
  - action: process_grid
    actor: system
    input: input_grid
    output: output_grid
    rule: "Iterate through each cell of the input grid."
  - action: evaluate_cell
    actor: system
    input: current_cell (value, position), input_grid
    output: output_cell_value
    rule: |
      1. Get the value (v) and position of the current cell.
      2. If v is 0, the output_cell_value is 0.
      3. If v is non-zero:
         a. Examine the values of the 8 neighboring cells (Moore neighborhood) in the input_grid. Handle boundary conditions (ignore non-existent neighbors).
         b. Check if any neighbor has the same value v.
         c. If at least one neighbor has value v, the output_cell_value is v.
         d. If no neighbor has value v, the output_cell_value is 0.
  - action: construct_output
    actor: system
    input: results of evaluate_cell for all cells
    output: output_grid
    rule: "Assemble the output_cell_values into a new grid with the same dimensions as the input grid."

```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Iterate through each cell `(r, c)` of the input grid. Let the value of the input cell be `v`.
3.  If `v` is 0, set the corresponding cell `(r, c)` in the output grid to 0.
4.  If `v` is not 0:
    a.  Check all 8 neighboring cells (including diagonals) of `(r, c)` within the bounds of the input grid.
    b.  Determine if any of these neighboring cells in the *input* grid has the same value `v`.
    c.  If at least one neighbor has the value `v`, set the corresponding cell `(r, c)` in the output grid to `v`.
    d.  If *none* of the neighbors have the value `v`, set the corresponding cell `(r, c)` in the output grid to 0.
5.  Return the completed output grid.