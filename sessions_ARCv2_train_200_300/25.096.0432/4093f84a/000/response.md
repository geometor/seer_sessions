Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Grid Structure:** The input and output are 2D grids of the same dimensions (14x14 in the examples).
2.  **Cell Values (Colors):** The grids contain integer values representing different colors: 0 (background), 5 (a solid block/area), and 1, 2, 3 (active 'trigger' colors).
3.  **Core Transformation:** The transformation modifies the grid based on the locations of the trigger colors (1, 2, or 3) relative to the block(s) of color 5. The trigger colors themselves are removed (effectively turned to 0) in the output unless they are transformed into 5s based on specific rules. The existing 5s generally remain unchanged.
4.  **Two Transformation Patterns:**
    *   **Expansion (Trigger Color 3):** As seen in `train_1`, cells with color 3 change to color 5 *if* they are orthogonally adjacent (sharing an edge) to a cell with color 5 in the input grid. If a cell with color 3 is not adjacent to any cell with color 5, it becomes 0.
    *   **Projection (Trigger Colors 1 and 2):** As seen in `train_2` (color 2) and `train_3` (color 1), the trigger colors act as sources that project the color 5 onto specific target rows.
        *   A contiguous horizontal block of color 5 exists.
        *   Trigger cells located in rows *above* this block project color 5 vertically downwards onto the row immediately *above* the block, in the same column as the trigger cell.
        *   Trigger cells located in rows *below* this block project color 5 vertically upwards onto the row immediately *below* the block, in the same column as the trigger cell.
        *   The original trigger cells become 0 in the output.
5.  **Rule Selection:** The specific transformation rule (Expansion or Projection) is determined by the trigger color present in the input (3 for Expansion, 1 or 2 for Projection). It's assumed only one type of trigger color (1, 2, or 3) will be present in a given input, besides 0 and 5.

## Facts


```yaml
elements:
  - object: grid
    properties:
      - type: 2D array
      - dimensions: variable (14x14 in examples)
      - cells: contains integer values representing colors
  - object: cell
    properties:
      - position: (row, column)
      - color: integer (0, 1, 2, 3, 5)
      - role: based on color
          - 0: background
          - 5: stable block/area
          - 1, 2, 3: trigger/source
relationships:
  - type: adjacency
    between: cells
    definition: Orthogonal neighbors (up, down, left, right)
  - type: relative_position
    between: trigger cell (1, 2, 3) and the block of 5s
    definition: Above, below, or adjacent to the block.
actions:
  - name: identify_trigger_color
    input: input_grid
    output: color (1, 2, or 3) or None
  - name: identify_5_block_rows
    input: input_grid
    output: min_row, max_row (for horizontal block)
    condition: Trigger color is 1 or 2.
  - name: transform_cell_color
    based_on: rules dependent on trigger color and relationship to 5s.
    rules:
      - rule_name: expansion
        trigger_color: 3
        condition: Input cell color is 3.
        effect:
          - If cell is orthogonally adjacent to a 5, output cell color becomes 5.
          - Otherwise, output cell color becomes 0.
      - rule_name: projection
        trigger_color: 1 or 2
        condition: Input cell color is 1 or 2 at position (r, c).
        effect:
          - Initialize output grid by copying input and setting all trigger cells to 0.
          - If r < min_row_5, set output cell (min_row_5 - 1, c) to 5.
          - If r > max_row_5, set output cell (max_row_5 + 1, c) to 5.
      - rule_name: preserve_color
        condition: Input cell color is 0 or 5 and not modified by other rules.
        effect: Output cell color is the same as input cell color.

```


## Natural Language Program

1.  **Analyze Input:** Examine the input grid to identify the predominant non-zero, non-5 'trigger' color (which will be 1, 2, or 3). Assume only one such trigger color exists per grid.
2.  **Select Rule:**
    *   If the trigger color is 3, apply the "Expansion Rule".
    *   If the trigger color is 1 or 2, apply the "Projection Rule".
3.  **Apply Expansion Rule (if trigger is 3):**
    *   Create an output grid initialized with the same values as the input grid.
    *   Iterate through each cell `(r, c)` of the input grid.
    *   If the input cell `(r, c)` contains color 3:
        *   Check its orthogonal neighbors (up, down, left, right) in the *input* grid.
        *   If any neighbor contains color 5, set the output grid cell `(r, c)` to 5.
        *   If no neighbor contains color 5, set the output grid cell `(r, c)` to 0.
    *   Leave all other cells (originally 0 or 5) unchanged in the output grid.
4.  **Apply Projection Rule (if trigger is 1 or 2):**
    *   Identify the minimum row (`min_row_5`) and maximum row (`max_row_5`) containing the contiguous horizontal block of color 5 in the input grid.
    *   Create an output grid initialized with the same values as the input grid, *except* change all cells containing the trigger color (1 or 2) to 0.
    *   Iterate through each cell `(r, c)` of the *input* grid.
    *   If the input cell `(r, c)` contains the trigger color (1 or 2):
        *   If the row `r` is less than `min_row_5`, set the output grid cell at `(min_row_5 - 1, c)` to 5.
        *   If the row `r` is greater than `max_row_5`, set the output grid cell at `(max_row_5 + 1, c)` to 5.
5.  **Final Output:** The resulting grid after applying the selected rule is the final output.